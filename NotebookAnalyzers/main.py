from fastapi import FastAPI, HTTPException
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


@app.get('/linters/{linter_id}')
def get_linter(linter_id: str):
    if linter_id in linters_dict:
        return {
            'data': {
                "id": linters_dict[linter_id].id,
                "description": linters_dict[linter_id].description
                }
            }
    else:
        raise HTTPException(status_code=400, detail="Bad request")

