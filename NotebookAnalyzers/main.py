from fastapi import FastAPI
import pynblint
import linters

app = FastAPI()
nb_linter = linters.NbLinter()
repo_linter = linters.RepoLinter()

linters_dict = {
    'nb-linter': nb_linter,
    'repo-linter': repo_linter
}


@app.get('/')
def index():
    return {'data': {'message': 'Welcome to the pynblint API'}}


@app.get('/linters')
def get_linters_list():
    return {"data": [{"id": linter_id, "description": linters_dict[linter_id].description} for linter_id in linters_dict]}
