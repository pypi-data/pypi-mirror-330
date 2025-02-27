import io
import json
import logging
import os
import queue
import socket
import subprocess
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from queue import Queue
from typing import Any, Iterator, List, Optional, Set, Literal

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class ServerResponse:
    headers: dict
    status_code: int
    body: dict | Any


class ServerStatus(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"
    STOPPING = "stopping"


@dataclass
class ServerConfig:
    server_bin_path: Optional[str] = None
    # Required parameters
    server_host: str = "127.0.0.1"
    server_port: int = 0

    # Optional parameters with defaults
    debug: bool = False
    model_hf_repo: str = "ggml-org/models"
    model_hf_file: str = "tinyllamas/stories260K.gguf"
    model_alias: str = "tinyllama-2"
    temperature: float = 0.8
    seed: int = 42

    # Optional parameters
    model_url: Optional[str] = None
    """model download url (default: unused, env: LLAMA_ARG_MODEL_URL)"""

    model_file: Optional[str] = None
    model_draft: Optional[str] = None
    threads: Optional[int] = None
    """number of threads to use during generation (default: -1)(env: LLAMA_ARG_THREADS)"""
    n_gpu_layers: Optional[int] = None
    """number of layers to store in VRAM(env: LLAMA_ARG_N_GPU_LAYERS), set 1000000000 to use all layers"""
    batch_size: Optional[int] = None
    """logical maximum batch size (default: 2048) (env: LLAMA_ARG_BATCH)"""
    ubatch_size: Optional[int] = None
    """physical maximum batch size (default: 512) (env: LLAMA_ARG_UBATCH)"""

    ctx_size: Optional[int] = None
    """size of the prompt context (default: 4096, 0 = loaded from model) (env: LLAMA_ARG_CTX_SIZE)"""
    grp_attn_n: Optional[int] = None
    """group-attention factor (default: 1)"""
    grp_attn_w: Optional[int] = None
    """group-attention width (default: 512)"""
    n_predict: Optional[int] = None
    """number of tokens to predict (default: -1, -1 = infinity, -2 = until context filled) (env: LLAMA_ARG_N_PREDICT)"""
    slot_save_path: Optional[str] = None
    """path to save slot kv cache (default: disabled)"""
    n_slots: Optional[int] = None
    cont_batching: bool | None = False
    """enable continuous batching (a.k.a dynamic batching)"""
    embedding: bool = False
    """restrict to only support embedding use case; use only with dedicated embedding models (default: disabled) 
    (env: LLAMA_ARG_EMBEDDINGS)"""
    reranking: bool = False
    """enable reranking endpoint on server (default: disabled)(env: LLAMA_ARG_RERANKING)"""
    metrics: bool = False
    """enable prometheus compatible metrics endpoint (default: disabled)(env: LLAMA_ARG_ENDPOINT_METRICS)"""
    slots: bool = False
    """enable slots monitoring endpoint (default: disabled)(env: LLAMA_ARG_ENDPOINT_SLOTS)"""
    draft: Optional[int] = None
    """number of tokens to draft for speculative decoding (default: 16)(env: LLAMA_ARG_DRAFT_MAX)"""
    draft_max: Optional[int] = None
    """Same as draft."""
    draft_min: Optional[int] = None
    """minimum number of draft tokens to use for speculative decoding(default: 5)"""
    api_key: Optional[str] = None
    """API key to use for authentication (default: none)(env: LLAMA_API_KEY)"""
    lora_files: List[str] = field(default_factory=list)
    """path to LoRA adapter (can be repeated to use multiple adapters)"""
    no_context_shift: bool = False
    """disables context shift on inifinite text generation (default: disabled)"""
    no_webui: Optional[bool] = None
    """disables web UI (default: enabled)"""
    jinja: bool | None = None
    """enable jinja templating for chat templates (default: disabled)"""
    reasoning_format: Literal['deepseek', 'none'] | None = None
    """
    reasoning format (default: deepseek; allowed values: deepseek, none)
        controls whether thought tags are extracted from the response, and in
        which format they're returned. 'none' leaves thoughts unparsed in
        `message.content`, 'deepseek' puts them in `message.reasoning_content`
        (for DeepSeek R1 & Command R7B only).
        only supported for non-streamed responses
        (env: LLAMA_ARG_THINK)
    """
    chat_template: str | None = None
    """
    set custom jinja chat template (default: template taken from model's
        metadata)
        if suffix/prefix are specified, template will be disabled
        only commonly used templates are accepted (unless --jinja is set
        before this flag):
        list of built-in templates:
        chatglm3, chatglm4, chatml, command-r, deepseek, deepseek2, deepseek3,
        exaone3, falcon3, gemma, gigachat, glmedge, granite, llama2,
        llama2-sys, llama2-sys-bos, llama2-sys-strip, llama3, megrez, minicpm,
        mistral-v1, mistral-v3, mistral-v3-tekken, mistral-v7, monarch,
        openchat, orion, phi3, phi4, rwkv-world, vicuna, vicuna-orca, zephyr
        (env: LLAMA_ARG_CHAT_TEMPLATE)
    """
    chat_template_file: str | None = None
    """
    set custom jinja chat template file (default: template taken from
        model's metadata)
        if suffix/prefix are specified, template will be disabled
        only commonly used templates are accepted (unless --jinja is set
        before this flag):
        list of built-in templates:
        chatglm3, chatglm4, chatml, command-r, deepseek, deepseek2, deepseek3,
        exaone3, falcon3, gemma, gigachat, glmedge, granite, llama2,
        llama2-sys, llama2-sys-bos, llama2-sys-strip, llama3, megrez, minicpm,
        mistral-v1, mistral-v3, mistral-v3-tekken, mistral-v7, monarch,
        openchat, orion, phi3, phi4, rwkv-world, vicuna, vicuna-orca, zephyr
        (env: LLAMA_ARG_CHAT_TEMPLATE_FILE)
    """



class ServerRetryStrategy:
    def __init__(
        self,
        retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: Optional[List[int]] = None,
    ):
        if status_forcelist is None:
            status_forcelist = [413, 429, 500, 502, 503, 504]
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist

    def get_retry_config(self) -> Retry:
        return Retry(
            total=self.retries,
            connect=self.retries,
            read=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )


class ServerProcess:
    def __init__(
        self, config: ServerConfig, retry_strategy: Optional[ServerRetryStrategy] = None
    ):
        self.config = config
        self.status = ServerStatus.STOPPED
        self.process: Optional[subprocess.Popen] = None
        self.output_queue: Queue = Queue()
        self.health_check_thread: Optional[threading.Thread] = None
        self.output_thread: Optional[threading.Thread] = None
        self.ready = False

        # Load environment variables
        self._load_environment_vars()
        # Retry strategy for server requests
        self.retry_strategy = retry_strategy or ServerRetryStrategy()
        self._setup_session()

    def _load_environment_vars(self) -> None:
        """Load configuration from environment variables"""
        if "N_GPU_LAYERS" in os.environ:
            self.config.n_gpu_layers = int(os.environ["N_GPU_LAYERS"])
        if "DEBUG" in os.environ:
            self.config.debug = True
        if "PORT" in os.environ:
            self.config.server_port = int(os.environ["PORT"])
        if self.config.server_port == 0:
            self.config.server_port = _find_available_port()
            logger.info(f"Randomly selected available port: {self.config.server_port}")

    def _output_monitor(self) -> None:
        """Monitor process output and log it appropriately

        This implementation:
        1. Distinguishes between stdout and stderr
        2. Buffers consecutive non-error lines to reduce log volume
        3. Immediately logs error lines
        4. Uses appropriate log levels (info for stdout, error for stderr)
        """
        try:
            buffer = []
            last_log_time = 0
            BUFFER_FLUSH_INTERVAL = 1.0  # Flush buffer every second

            while self.process and self.status != ServerStatus.STOPPED:
                try:
                    output, is_stderr = self.output_queue.get(timeout=0.5)
                    if output is None:
                        break

                    current_time = time.time()

                    if is_stderr:
                        # Flush any buffered stdout first
                        if buffer:
                            logger.info("\n".join(buffer))
                            buffer.clear()
                        # Log stderr immediately with error level
                        logger.error(f"[stderr] {output}")
                    else:
                        # Buffer stdout lines
                        buffer.append(output)

                        # Flush buffer if it's been too long or buffer is large
                        if (
                            current_time - last_log_time > BUFFER_FLUSH_INTERVAL
                            or len(buffer) > 10
                        ):
                            if buffer:
                                str_log = "\n".join(buffer)
                                if "request: GET /health" not in str_log or self.config.debug:
                                    logger.info(str_log)
                                buffer.clear()
                                last_log_time = current_time

                except queue.Empty:
                    # Flush buffer on timeout
                    if buffer:
                        logger.info("\n".join(buffer))
                        buffer.clear()
                        last_log_time = time.time()

        except Exception as e:
            logger.error(f"Error in output monitor: {e}", exc_info=True)
        finally:
            # Flush any remaining buffered output
            if buffer:
                logger.info("\n".join(buffer))

    def _setup_session(self):
        """设置 session 和连接池"""
        self.session = requests.Session()

        # Connection pool settings
        adapter = HTTPAdapter(
            pool_connections=100,  # Connection pool size
            pool_maxsize=100,  # Max pool size
            max_retries=self.retry_strategy.get_retry_config(),
            pool_block=False,  # No blocking when pool is full
        )

        # Mount the adapter for both http and https
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # If an API key is provided, set the default headers
        if self.config.api_key:
            self.session.headers.update(
                {"Authorization": f"Bearer {self.config.api_key}"}
            )

    def _handle_request_error(self, method: str, path: str, error: Exception) -> None:
        """Handle request errors"""
        if isinstance(error, (requests.exceptions.ConnectionError, socket.error)):
            logger.error(f"Connection error in {method} {path}: {str(error)}")
            if self.status == ServerStatus.RUNNING:
                self.status = ServerStatus.ERROR
                self._handle_connection_error()
        elif isinstance(error, requests.exceptions.Timeout):
            logger.error(f"Timeout in {method} {path}: {str(error)}")
        else:
            logger.error(f"Unexpected error in {method} {path}: {str(error)}")

    def _handle_connection_error(self):
        """Handle connection errors"""
        if self.health_check_thread and not self.health_check_thread.is_alive():
            self.health_check_thread = threading.Thread(
                target=self._health_check, daemon=True
            )
            self.health_check_thread.start()

    def _health_check(self) -> None:
        """Monitor the health of the server"""
        consecutive_failures = 0
        max_failures = 3

        while self.status in [ServerStatus.STARTING, ServerStatus.RUNNING]:
            try:
                response = self.make_request("GET", "/health", timeout=5)

                if response.status_code == 200:
                    consecutive_failures = 0
                    if self.status == ServerStatus.STARTING:
                        self.status = ServerStatus.RUNNING
                        self.ready = True
                        logger.info("Server is now running and healthy")
                else:
                    consecutive_failures += 1
                    logger.warning(
                        f"Health check failed with status code: {response.status_code}"
                    )

            except Exception as e:
                consecutive_failures += 1
                logger.error(f"Health check failed: {str(e)}")

            if (
                consecutive_failures >= max_failures
                and self.status == ServerStatus.RUNNING
            ):
                self.status = ServerStatus.ERROR
                logger.error(
                    f"Server health check failed {max_failures} times consecutively"
                )

            time.sleep(5)

    def _enqueue_output(self, pipe: Any, queue: Queue, is_stderr: bool = False) -> None:
        """Helper function to enqueue output from a pipe

        Args:
            pipe: The pipe to read from (stdout or stderr)
            queue: The queue to write output to
            is_stderr: Whether this pipe is stderr (for log level differentiation)
        """
        try:
            text_pipe = io.TextIOWrapper(
                pipe,
                encoding="utf-8",  # We can safely use utf-8 for server output
                errors="replace",
                newline=None,  # auto-detect and normalize line endings
            )

            # Read and enqueue lines
            for line in text_pipe:
                queue.put((line.rstrip("\r\n"), is_stderr))

        except Exception as e:
            logger.error(f"Error in output thread: {e}", exc_info=True)
            queue.put((None, is_stderr))
        finally:
            try:
                text_pipe.close()
            except:
                pass
            try:
                pipe.close()
            except:
                pass

    def start(self, timeout_seconds: int = 60, fast_check_timeout: int = 2) -> None:
        """Start the server process with monitoring"""
        if self.status != ServerStatus.STOPPED:
            logger.warning("Server is already running or starting")
            return

        self.status = ServerStatus.STARTING
        server_path = self._get_server_path()
        server_args = self._build_server_args()

        envs = {**os.environ, "LLAMA_CACHE": "tmp"}
        if "LD_LIBRARY_PATH" not in envs:
            envs["LD_LIBRARY_PATH"] = os.path.dirname(server_path)

        try:
            # Start process with pipe for output
            logger.info(f"Starting server process, start command: {server_args}")
            self.process = subprocess.Popen(
                server_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=self._get_creation_flags(),
                env=envs,
                bufsize=1,  # Line buffered
            )
            server_instances.add(self)
            logger.info(
                f"Started server process with PID {self.process.pid}, current process: {os.getpid()}"
            )

            # Start output monitoring thread
            self.output_thread = threading.Thread(
                target=self._enqueue_output,
                args=(self.process.stdout, self.output_queue),
                daemon=True,
                name="stdout-monitor",
            )
            self.output_thread.start()

            # Start error monitoring thread
            error_thread = threading.Thread(
                target=self._enqueue_output,
                args=(self.process.stderr, self.output_queue),
                daemon=True,
                name="stderr-monitor",
            )
            error_thread.start()

            # Start logging thread
            log_thread = threading.Thread(
                target=self._output_monitor, daemon=True, name="log-monitor"
            )
            log_thread.start()

            # Start health check thread
            self.health_check_thread = threading.Thread(
                target=self._health_check, daemon=True
            )
            self.health_check_thread.start()

            # Wait for server to start with periodic status checks
            start_time = time.time()
            check_interval = 0.5  # Check every 0.5 seconds
            
            while time.time() - start_time < timeout_seconds:
                # Check process status
                if self.process.poll() is not None:
                    exit_code = self.process.poll()
                    if exit_code == 0:
                        return
                    error_output = b""
                    try:
                        error_output = self.process.stderr.read()
                    except:
                        pass
                    raise RuntimeError(
                        f"Server process terminated unexpectedly (exit code: {exit_code}). "
                        f"Error output: {error_output.decode('utf-8', errors='replace')}"
                    )
                    
                # Check server status
                if self.status == ServerStatus.RUNNING:
                    return
                elif self.status == ServerStatus.ERROR:
                    raise RuntimeError("Server failed to start properly")
                    
                time.sleep(check_interval)

            raise TimeoutError(f"Server did not start within {timeout_seconds} seconds")

        except Exception as e:
            self.status = ServerStatus.ERROR
            logger.error(f"Failed to start server: {str(e)}")
            self.stop()
            raise

    def _get_server_path(self) -> str:
        """Get the server binary path"""
        if self.config.server_bin_path:
            return self.config.server_bin_path
        if "LLAMA_SERVER_BIN_PATH" in os.environ:
            return os.environ["LLAMA_SERVER_BIN_PATH"]
        from . import get_server_binary_path

        return get_server_binary_path()

    def _get_creation_flags(self) -> int:
        """Get creation flags for the process based on OS"""
        flags = 0
        if os.name == "nt":
            flags |= subprocess.DETACHED_PROCESS
            flags |= subprocess.CREATE_NEW_PROCESS_GROUP
            flags |= subprocess.CREATE_NO_WINDOW
        return flags

    def _build_server_args(self) -> List[str]:
        """Build command line arguments for the server"""
        server_path = self._get_server_path()
        args = [
            server_path,
            "--host",
            self.config.server_host,
            "--port",
            str(self.config.server_port),
            "--temp",
            str(self.config.temperature),
            "--seed",
            str(self.config.seed),
        ]

        # Add optional arguments
        optional_args = {
            "--model": self.config.model_file,
            "--model-url": self.config.model_url,
            "--model-draft": self.config.model_draft,
            "--hf-repo": self.config.model_hf_repo,
            "--hf-file": self.config.model_hf_file,
            "--batch-size": self.config.batch_size,
            "--ubatch-size": self.config.ubatch_size,
            "--threads": self.config.threads,
            "--n-gpu-layers": self.config.n_gpu_layers,
            "--draft": self.config.draft,
            "--alias": self.config.model_alias,
            "--ctx-size": self.config.ctx_size,
            "--parallel": self.config.n_slots,
            "--n-predict": self.config.n_predict,
            "--slot-save-path": self.config.slot_save_path,
            "--grp-attn-n": self.config.grp_attn_n,
            "--grp-attn-w": self.config.grp_attn_w,
            "--api-key": self.config.api_key,
            "--draft-max": self.config.draft_max,
            "--draft-min": self.config.draft_min,
        }

        for flag, value in optional_args.items():
            if value is not None:
                args.extend([flag, str(value)])

        # Add boolean flags
        if self.config.cont_batching:
            args.append("--cont-batching")
        if self.config.embedding:
            args.append("--embedding")
        if self.config.reranking:
            args.append("--reranking")
        if self.config.metrics:
            args.append("--metrics")
        if self.config.slots:
            args.append("--slots")
        if self.config.debug:
            args.append("--verbose")
        if self.config.no_context_shift:
            args.append("--no-context-shift")
        if self.config.no_webui:
            args.append("--no-webui")
        if self.config.jinja:
            args.append("--jinja")
        if self.config.reasoning_format is not None:
            args.extend(("--reasoning-format", self.config.reasoning_format))
        if self.config.chat_template:
            args.extend(["--chat-template", self.config.chat_template])
        if self.config.chat_template_file:
            args.extend(["--chat-template-file", self.config.chat_template_file])


        # Add LoRA files
        for lora_file in self.config.lora_files:
            args.extend(["--lora", lora_file])

        return [str(arg) for arg in args]

    def stop(self) -> None:
        """Stop the server process and clean up resources"""
        if self.status == ServerStatus.STOPPED:
            return

        if self in server_instances:
            server_instances.remove(self)

        self.status = ServerStatus.STOPPING
        logger.info("Stopping server process...")

        if self.process:
            self.process.kill()
            self.process.wait()
            self.process = None

        # Signal threads to stop
        self.output_queue.put((None, False))

        if self.output_thread:
            self.output_thread.join(timeout=5)
        if self.health_check_thread:
            self.health_check_thread.join(timeout=5)

        # Close the session and connection pool
        if hasattr(self, "session"):
            self.session.close()

        self.status = ServerStatus.STOPPED
        self.ready = False
        logger.info("Server process stopped")

    @property
    def real_server_host(self) -> str:
        """Get the real server host

        Returns:
            str: The actual host address to use for connections

        This method handles special cases for different IP address formats:
        - "::" or "::0" -> "127.0.0.1" (for loopback)
        - "0.0.0.0" -> "127.0.0.1" (for loopback)
        - "::1" -> "127.0.0.1" (for IPv6 loopback)
        - Other addresses are returned as-is
        """
        server_host = self.config.server_host or "127.0.0.1"

        # Handle special IPv6 cases
        if server_host in ["::0", "::"]:
            return "127.0.0.1"

        # Handle IPv4 all interfaces
        if server_host == "0.0.0.0":
            return "127.0.0.1"

        # Handle IPv6 loopback
        if server_host == "::1":
            return "127.0.0.1"

        return server_host

    def get_request_url(self, path: str) -> str:
        """Get the full URL for a request path"""
        return f"http://{self.real_server_host}:{self.config.server_port}{path}"

    def make_request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
    ) -> ServerResponse:
        """Make a request to the server."""
        url = self.get_request_url(path)
        request_headers = {}
        if headers:
            request_headers.update(headers)

        try:
            parse_body = False
            if method == "GET":
                response = self.session.get(
                    url, headers=request_headers, timeout=timeout
                )
                parse_body = True
            elif method == "POST":
                response = self.session.post(
                    url, headers=request_headers, json=data, timeout=timeout
                )
                parse_body = True
            elif method == "OPTIONS":
                response = self.session.options(
                    url, headers=request_headers, timeout=timeout
                )
            else:
                raise ValueError(f"Unimplemented method: {method}")

            result = ServerResponse()
            result.headers = dict(response.headers)
            result.status_code = response.status_code
            result.body = response.json() if parse_body else None
            logger.debug(f"Received response: {json.dumps(result.body, indent=2)}")
            return result

        except Exception as e:
            self._handle_request_error(method, path, e)
            raise

    def make_stream_request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[int] = None,
    ) -> Iterator[dict]:
        """Make a streaming request to the server"""
        url = self.get_request_url(path)
        request_headers = {}
        if headers:
            request_headers.update(headers)

        try:
            if method != "POST":
                raise ValueError(f"Streaming only supported for POST method")

            with self.session.post(
                url, headers=request_headers, json=data, stream=True, timeout=timeout
            ) as response:
                if response.status_code not in [200, 201]:
                    error_message = response.text
                    raise ValueError(
                        f"SSE request failed with status code {response.status_code}: {error_message}"
                    )

                for line in response.iter_lines():
                    if not line:
                        continue

                    line_str = line.decode("utf-8")
                    if line_str.strip() == "[DONE]":
                        break

                    if line_str.startswith("data: "):
                        logger.debug(f"Received streaming data: {line_str}")
                        json_data = line_str[6:]
                        if json_data.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(json_data)
                            logger.debug(
                                f"Received streaming data: {json.dumps(data, indent=2)}"
                            )
                            yield data
                        except json.JSONDecodeError as e:
                            logger.error(f"Error decoding streaming data: {json_data}")
                            raise

        except Exception as e:
            self._handle_request_error(method, path, e)
            raise


# Global set to track server instances
server_instances: Set[ServerProcess] = set()


def _is_port_available(port: int) -> bool:
    """Check if a port is available for binding

    Args:
        port: The port number to check

    Returns:
        bool: True if the port is available, False otherwise
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", port))
            return True
    except socket.error:
        return False


def _find_available_port() -> int:
    """Find an available port for the server to bind to

    Returns:
        int: The available port number
    """
    import random

    while True:
        # Choose a random port between 10000 and 65535
        port = random.randint(10000, 65535)
        if _is_port_available(port):
            return port
