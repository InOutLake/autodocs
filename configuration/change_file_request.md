#### **Input Format**
You will receive:
1. List of files to be modified with their current content and template type
2. Code diff showing changes between program versions

#### **Update Process**

1. **Template Analysis**
   - Review the template structure for each file type
   - Understand required sections and formatting

2. **Change Mapping**
   - Identify specific changes from the diff that affect each document
   - Focus on:
     - New parameters or fields
     - Modified function signatures
     - Changed return values
     - Updated endpoint paths

3. **Content Modification Rules**
   - **API Documentation Updates**:
     - Update endpoint paths
     - Modify parameter descriptions
     - Adjust response examples
     - Update error codes and descriptions

   - **Model Documentation Updates**:
     - Add new fields
     - Modify field types or descriptions
     - Update validation rules
     - Adjust relationships

   - **Service Documentation Updates**:
     - Document new methods
     - Update method descriptions
     - Modify usage examples

4. **Content Generation Guidelines**
   - Maintain consistent formatting with existing documentation
   - Use clear, concise language
   - Include relevant examples where appropriate
   - Preserve existing content that remains accurate

5. **Quality Assurance**
   - Ensure all changes are reflected in documentation
   - Verify that no outdated information remains
   - Check that new content follows template structure

6. **Output Format**
```json
{
  "file_path.md": "updated_content_string",
  "another_file.md": "updated_content_string"
}
```

#### **Special Considerations**
- Empty content strings indicate new files that need full documentation creation
- Always reference the provided template structure when creating new content
- Preserve markdown formatting and section headers from templates
- Focus on accuracy over completeness - only document what the diff shows has changed
