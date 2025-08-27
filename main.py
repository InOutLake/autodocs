import argparse
from git_tracker import GitTracker
from main.docs_generator import DocsGenerator
from main.docs_manager import DocsManager
from main.logging.logging import setup_logging
from llm.cerebras import CerebrasLlm
from llm.llm import Llm
from dotenv import load_dotenv


if __name__ == "__main__":
    # TODO: decide whether use flags or .env configuration. It is probably better to add git tracker options to the flags section.
    # What configuration for git do I need to pass? Probably last commit, and the way documentation will be changed, whether it is a new branch or autoapply.
    # Also it looks like iterative changing based on several user requests might be handy.
    # TODO: It might be benefitial to store docs change commit history, so user and system could track down changes and versions.
    # TODO: Think on changing documentation in the work branches, not master.
    # TODO: Rethink documentation changing logic. It might be benefitial if one responsible for the changes would make chnages for the documentation, but it may be synced on the main branch.
    # TODO: Think on docs synchronization. It have to be tracked by git then. In theory merge collisions must be a rare occasion. And how do I keep track on multiple documentation commits added to the history?
    # Maybe I need to reference to the branch start commit (parent commit). But then what if I want to change docs on the halfway and then relate to the changes made from that point?

    parser = argparse.ArgumentParser(
        description="Generate documentation for the project"
    )
    parser.add_argument(
        "--custom_request",
        "-cr",
        type=str,
        help="Add custom request for document generation. Use this flag if you want to change documents without diff.",
    )
    parser.add_argument(
        "--no_save",
        action="store_true",
        help="Changes will not be saved but simply stdout instead.",
    )
    parser.add_argument(
        "--force_sync",
        action="store_true",
        help="Docs will be synced even if they are not the master branch.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Changes will be applied in one commit and instantly synced with the remote.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase verbosity (use -v, -vv, or -vvv)",
    )
    load_dotenv()
    args = parser.parse_args()
    setup_logging(args.verbose)
    custom_request = None
    if args.custom_request:
        custom_request = args.custom_request

    docs_manager = DocsManager()
    gitapi = GitTracker()
    llm = Llm(CerebrasLlm())
    docs_generator = DocsGenerator(docs_manager, gitapi, llm)
    docs_generator.update_docs(custom_request)
