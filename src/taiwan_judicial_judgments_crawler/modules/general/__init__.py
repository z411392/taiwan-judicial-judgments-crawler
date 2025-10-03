from injector import Module, Binder, InstanceProvider
from langchain_ollama import ChatOllama
from os import getenv


class GeneralModule(Module):
    def configure(self, binder: Binder):
        binder.bind(
            ChatOllama,
            InstanceProvider(
                ChatOllama(
                    model=getenv("LLM_MODEL"),
                    base_url=getenv("LLM_URL"),
                ),
            ),
        )


general_module = GeneralModule()
