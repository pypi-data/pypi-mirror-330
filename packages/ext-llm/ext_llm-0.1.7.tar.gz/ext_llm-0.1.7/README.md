# ext_llm - a wrapper library for common LLMs (WIP)
## Installation
```bash pip install ext_llm```
## Usage
```python
import ext_llm as xllm
#read config yaml file
config : str = open("ext_llm_config.yaml").read()
#initialize extllm library
extllm = xllm.init(config)

extllm.list_available_models()

llm_client = extllm.get_model("aws")
llm_client1 = extllm.get_model("groq")

# non blocking calls
future1 = llm_client.generate_text("You're an helpful assistant", "Say hello world", 10, 0.5)
future2 = llm_client1.generate_text("You're an helpful assistant", "Say hello world", 10, 0.5)

# blocking calls waiting for the result
print(future2.result())
print(future1.result())

