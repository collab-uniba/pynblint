from fastapi import FastAPI, HTTPException
import pynblint
import linters

app = FastAPI()
nb_linter = linters.NbLinter()
repo_linter = linters.RepoLinter()

linters_dict = {nb_linter.id: nb_linter.description, repo_linter.id: repo_linter.description}


@app.get('/')
def index():
    return {'data': {'message': 'Welcome to the pynblint API'}}


@app.get('/linters/{linter_id}')
def get_linter(linter_id: str):
    if linter_id in linters_dict:
        return {'data': {'id': linter_id, 'description': linters_dict[linter_id]}}
        #return {
        #    'data': {
        #        "id": linters_dict[linter_id].id,
        #        "description": linters_dict[linter_id].description
        #        }
        #    }
    else:
        raise HTTPException(status_code=400, detail="Bad request")

