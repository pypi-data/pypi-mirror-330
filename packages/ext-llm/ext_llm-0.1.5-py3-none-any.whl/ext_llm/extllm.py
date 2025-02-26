from ext_llm import ExtLlmContext
import ext_llm

class ExtLlm:

    def __init__(self, context: ExtLlmContext):
        self.context = context

    def list_available_models(self):
        return self.context.get_configs()["models"]

    def get_model(self, model_name: str) -> ext_llm.llm.Llm:
        class_name = self.context.get_configs()["models"][model_name]["class_name"]
        module_name = "ext_llm.llm"
        module = __import__(module_name, fromlist=[class_name])
        if hasattr(module, class_name):
            return getattr(module, class_name)()
        else:
            raise Exception("Class not found")