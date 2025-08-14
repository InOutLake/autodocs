#### **Input Format**
You will receive:
1. A list of existing documentation files with their template types
2. Available templates for documents
3. A diff showing changes between last and current program versions

#### **Analysis Process**

1. **Identify Affected Components**
   - Scan the diff for:
     - New files or modules
     - Modified functions, classes, or endpoints
     - Deleted components

2. **Map Changes to Documentation Needs**
   - For each change, determine if it affects existing documentation or requires new documentation
   - Consider the scope of changes:
     - Structural changes → Update documentation
     - New features → Create new documentation
     - Removed features → Delete documentation

3. **Decision Rules**
   - **Create**: When new functionality is added that lacks documentation
   - **Update**: When existing functionality is modified
   - **Delete**: When functionality is removed entirely
   - **No Change**: When changes are purely bug fixes or internal refactoring

4. **Template Selection**
   - Match new documentation to appropriate template based on component type

5. **Output Format**
```json
{
  "file_path.md": ["action", "template_type"],
  "another_file.md": "action"
}
```
Where `action` is one of: `create`, `update`, `delete`
