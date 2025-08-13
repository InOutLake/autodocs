import os
from llm.llmagent import LlmAgent


class CelebraLlm(LlmAgent):
    def __init__(self):
        self.apikey = os.environ["CEREBRAS_API_KEY"]

    def answer(self, ):
        
