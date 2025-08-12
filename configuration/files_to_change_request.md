Now you'll be given a complete list of existing documents, their template type and a difference between previous program version and a next one.
Documents list will be given in the following format:
```json
{
  "services/service_0/logic_part_1/api": "api",
  "services/service_0/logic_part_1/model": "model"
}
```
Based on the difference decide which documents has to be changed, what documents to add and what documents to delete if there is need to do so. Also decide which type of template must be used for new documents.
Documentation might not need to be changed, for example, if bug was fixed.

Write your decision in the following .json format (aliases are used instead of actual file names):
```json
{
  "file_name_one.md": ["create", "api"]
  "project/file_name_two.md": "update",
  "file_name_tree.md": "delete"
}
```

