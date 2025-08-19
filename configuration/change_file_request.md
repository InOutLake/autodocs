Following the main ruleset, your task is to update documentation content based on code changes.

1. TASK EXPLANATION:
   Update the provided documentation file by analyzing the diff and applying necessary changes to keep documentation accurate and useful for end users. Use the template as structural guidance but prioritize clarity and completeness.

2. INPUTS ANALYSIS:
   - Diff: Identify what changed in the code that affects user-facing functionality
   - Document content: Understand current documentation structure and content with line numbers
   - Template content: Use as structural reference but adapt as needed for clarity. Note that both documents and templates start with a tag <<template_type>> indicating their type. Tags has to stay persistent, do not erase or edit it.

3. UPDATE RULES:
   - Focus ONLY on changes that affect end users (APIs, interfaces, usage patterns)
   - Add new documentation for new functionality
   - Update existing documentation when functionality changes
   - Remove outdated information when features are deprecated/removed
   - Enhance clarity with examples, notes, and comprehensive explanations when beneficial
   - Maintain user-focused perspective - document what users need to know, not implementation details

4. OUTPUT FORMAT:
   {
     "1": "## GET /v2/adjust_position",
     "7": "**Args**",
     "8": "User: AuthenticatedUser"
   }
   - Keys: Line numbers (strings) corresponding to input document line numbers
   - Values: Updated content for those lines
   - To add new lines: Include \n in the content (e.g., "Line1\nLine2\nLine3")
   - To delete lines: Provide empty string ""
   - Only include lines that need changes
   - All keys must be strings enclosed in double quotes
   - All values must be strings enclosed in double quotes
   - No trailing commas
   - Pure JSON only - no markdown code blocks, no extra text

5. CONTENT GUIDELINES:
   - Write clear, concise, user-focused documentation
   - Include practical examples when they enhance understanding
   - Add notes and explanations that help users avoid common pitfalls
   - Structure content logically following template guidance where appropriate
   - Ensure all updated information accurately reflects current code behavior

Analyze the provided information and generate the JSON object of line updates.
