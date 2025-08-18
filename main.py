from config import Config
from git_tracker import GitTracker
from main.docs_generator import DocsGenerator
from main.docs_manager import DocsManager
from llm.cerebras import CerebrasLlm
from llm.llm import Llm
from dotenv import load_dotenv


if __name__ == "__main__":
    # TODO: use fabrics to create right type of each manager based on the env or input flags
    load_dotenv()
    docs_manager = DocsManager()
    gitapi = GitTracker()
    llm = Llm(CerebrasLlm())
    config = Config()
    docs_generator = DocsGenerator(docs_manager, gitapi, llm, config)

    docs_generator.update_docs()
