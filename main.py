import argparse
from git_tracker import GitTracker
from main.docs_generator import DocsGenerator
from main.docs_manager import DocsManager
from llm.cerebras import CerebrasLlm
from llm.llm import Llm
from dotenv import load_dotenv


if __name__ == "__main__":
    # TODO: add other llm interfaces. !DONE!
    # TODO: decide whether use flags or .env configuration. It is probably better to add git tracker options to the flags section.
    # What configuration for git do I need to pass? Probably last commit, and the way documentation will be changed, whether it is a new branch or autoapply.
    # Also it looks like iterative changing based on several user requests might be handy.
    # TODO: Think on changing documentation in the work branches, not master.
    # TODO: add interfaces to make reuqests to llm to change certain parts of configuration based on the additional request. !DONE!
    parser = argparse.ArgumentParser(
        description="Generate documentation for the project"
    )

    parser.add_argument(
        "--custom_request",
        "-cr",
        action="store",
        help="Add custom request for document generation. Use this flag if you want to change documents without diff",
    )
    parser.add_argument(
        "--no_save",
    )
    load_dotenv()
    docs_manager = DocsManager()
    gitapi = GitTracker()
    llm = Llm(CerebrasLlm())
    docs_generator = DocsGenerator(docs_manager, gitapi, llm)

    docs_generator.update_docs()
