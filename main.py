from config import Config
from git_tracker import GitTracker
from main.docs_generator import DocsGenerator
from main.docs_manager import DocsManager
from llm.ollama import OllamaLLM
from llm.llm import Llm


if __name__ == "__main__":
    docs_manager = DocsManager()
    gitapi = GitTracker()
    llm = Llm(OllamaLLM())
    config = Config()
    docs_generator = DocsGenerator(docs_manager, gitapi, llm, config)

    docs_generator.update_docs()
