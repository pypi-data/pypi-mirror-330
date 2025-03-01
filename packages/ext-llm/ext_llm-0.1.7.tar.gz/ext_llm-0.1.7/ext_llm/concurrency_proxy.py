import concurrent.futures
from concurrent.futures import Future

from ext_llm import Llm

class LlmConcurrencyProxy(Llm):

    def __init__(self, llm: Llm):
        super().__init__()
        self.llm = llm
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def generate_text(self, system_prompt: str, prompt: str, max_tokens: int, temperature: float) -> Future:
        future = self.executor.submit(self.llm.generate_text, system_prompt, prompt, max_tokens, temperature)
        return future