from injector import Module, Binder, InstanceProvider
from langchain_openai import ChatOpenAI
from os import getenv


class GeneralModule(Module):
    def configure(self, binder: Binder):
        binder.bind(
            ChatOpenAI,
            InstanceProvider(
                ChatOpenAI(
                    model=getenv("LLM_MODEL"),
                    openai_api_key=getenv("LLM_KEY"),
                    openai_api_base=getenv("LLM_URL"),
                ),
            ),
        )


general_module = GeneralModule()
