# **Input Format**
You will receive:
1. A file and its content
2. Template of the documentation applied to this file
3. Code diff showing changes between program versions

#### **Update Process**

1. **Template Analysis**
   - Review the template structure file type
   - Understand required sections and formatting

2. **Change Mapping**
   - Identify specific changes from the diff that affect each document
   - Focus on:
     - New parameters or fields
     - Modified function signatures
     - Changed return values
     - Updated endpoint paths
  
  - Only changes related to the end result must be shown in the documentation. All internal that does not affect end result must not be included in the documentation unless it is asked otherwise.

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

   - **Library Documentation Updates**:
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
[
  {
    "line_start": 4,
    "line_end": 7,
    "content": "## GET /v2/adjust_position\nAdjusts position of an object\nV2 has additional fields:"

  },
  {
    "line_start": 5,
    "line_end": 5,
    "content": "Column info: String"

  }
]
```

**Notes about output:**
- Output must be a valid json with provided fields.
- `line_start` value means first line to be edited in the range.
- `line_end` value means last line to be edited in the range.
- `content` will replace all the content in those lines.
- You also can add rows by replacing less ranges with greater quantity of lines (for example, replace rows 4 to 5 with "\n\n\n\n\n\n")
- You also can delete rows by replacing greater range with less quantity of lines (for example, replace 5 to 10 with "\n")

