from llm.llmagent import LlmAgent


class Llm:
    def __init__(self, agent: LlmAgent):
        self.agent = agent

    def get_files_to_change(
        self,
        ruleset: str,
        request: str,
        diff: str,
        existing_files: str,
    ):
        prompt = f"""
        {ruleset}\n\n
        {request}\n\n
        Current documentation has following files:\n
        {existing_files}\n\n
        Project has been changed in the following order:\n
        {diff}
        """
        return self.agent.answer(prompt)

    def update_docs(
        self,
        ruleset: str,
        request: str,
        diff: str,
        templates: str,
        docs_to_change: str,
        language: str,
    ):
        prompt = f"""
        {ruleset}\n\n
        {request}\n\n
        Docs to be changed:\n
        {docs_to_change}\n\n
        Templates you'll need:\n
        {templates}\n\n
        Difference has been made:\n
        {diff}\n\n
        Write documentatioin in the {language} language.
        """
        return self.agent.answer(prompt)
