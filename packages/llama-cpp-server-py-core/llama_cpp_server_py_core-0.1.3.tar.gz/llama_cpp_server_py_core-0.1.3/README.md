# llama-cpp-server-py-core

Describe your project here.


## Some tools

### Convert huggingface model to gguf model

```bash
rye run hf2gguf /opt/models/llm/qwen/Qwen2.5-Coder-14B-Instruct --outfile /opt/models/llm/qwen/Qwen2.5-Coder-14B-Instruct-f16.gguf
```

### Quantize gguf model

```bash
rye run quantize /opt/models/llm/qwen/Qwen2.5-Coder-14B-Instruct-f16.gguf /opt/models/llm/qwen/Qwen2.5-Coder-14B-Instruct-Q4_k_m.gguf Q4_k_m
```