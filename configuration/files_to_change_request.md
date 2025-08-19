Following the main ruleset, your task is to analyze documentation needs based on code changes.

1. TASK EXPLANATION:
   Analyze the provided diff, existing documents, and available templates to determine which documentation files need to be created, updated, or deleted. Make decisions based on what content changes require documentation updates.

2. INPUTS ANALYSIS:
   - Review the diff to identify changed/added/removed code that affects end-user functionality
   - Examine existing documents to understand current documentation coverage
   - Check available templates to determine appropriate documentation structure
   - Focus on user-facing changes: APIs, interfaces, public methods, configuration changes

3. DECISION LOGIC:
   CREATE: When new functionality is added that requires user documentation and no existing document covers it appropriately
   UPDATE: When existing functionality changes and current documentation needs modification to remain accurate
   DELETE: When functionality is removed and corresponding documentation is no longer relevant

4. OUTPUT FORMAT:
   {
     "service/document1.md": ["create", "template_type"],
     "another_service/other_part.md": "update",
     "general_document.md": "delete"
   }
   - Keys: Full file paths with .md extension
   - Values: Either ["create", "template_type"] or "update" or "delete"
   - Only include files that actually need changes
   - Choose appropriate template type for new documents based on content nature

Analyze the provided information and generate the JSON list of documentation changes.
