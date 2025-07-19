# pulse

Configure Intellij IDEA

1. 
```shell
cd backend && mkdir .venv && poetry config virtualenvs.in-project true && poetry install
```

2.
⚙️ -> Project Structure... -> 
Project -> Project Settings -> SDK -> Add Python SDK from disk... ->
Virtual Environment -> Existing environment ->
Interpreter: {PROJECT_PATH}/backend/.venv/bin/python3
-> OK

Start
```shell
make up
```
