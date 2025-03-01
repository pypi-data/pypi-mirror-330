import ext_llm as xllm

#read config yaml file
config : str = open("ext_llm_config.yaml").read()

#initialize extllm library
extllm = xllm.init(config)

print(extllm.list_available_models())
llm_client = extllm.get_model("aws")
llm_client.generate_text("You're an helpful assistant", "Say hello world", 10, 0.5)