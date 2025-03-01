from ext_llm import Llm


class AwsLlm(Llm):

    def __init__(self):
        super().__init__()

    def generate_text(self, system_prompt : str, prompt : str, max_tokens: int, temperature: float) -> str :
        return "Hello AwsLlm"