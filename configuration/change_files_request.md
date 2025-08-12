Now you'll be given a list of documents that were decided to be edited, their content and the difference between previous program version and a next one.
Content will be given in the following .json format (aliases are used instead of actual file names):
```json
{
  "file_name_one.md": {"template": "api", "content": ""},
  "project/file_name_two.md": {"template": "api", "content": "#Templates api documentation.\n ##Templates creation\n *Route* `post api/template`\n ...",
  "file_name_tree.md": {"template": "model", "content": ""}
}
```
Empty value means files does not have any content yet.

Based on the difference and accordingly to given templates change content of the files and write it in the following .json format (aliases are used instead of actual file names, example content used instead of the actual changed content):
```json
{
  "file_name_one.md": "#Some logic api documentation\n ...",
  "project/file_name_two.md": "#Templates api documentation\n ##Templates creation\n *Route* `post api/create_template`\n...",
  "file_name_tree.md": "#New logic api documentation\n ..."
}
```

