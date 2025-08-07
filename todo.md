TODO list:
- main
- templates
- instalation script


Docs must be tracked by git and only applied on merge into main, this way I will not need to setup changes tracking system for the docs api. Only main branch docs must be sent to the docs server. Therefore, it is a post merge CI/CD process.
So system has to track commit of the main branch on which docs sync was on, collect the changes of all the commits up to the HEAD and generate docs based on changes that has been applied.
