from fastapi import FastAPI
import pynblint
import linters

app = FastAPI()
nb_linter = linters.NbLinter()
repo_linter = linters.RepoLinter()


@app.get('/')
def index():
    return {'data': {'message': 'Welcome to the pynblint API'}}


@app.get('/linters')
def get_linters_list():
    return {"data": [{"id": nb_linter.id, "description": nb_linter.description}, {"id": repo_linter.id, "description": repo_linter.description}]}

# @app.get('/notebook/{id}/empty_cells') #analyze_noteboo #analyze_repository
# def empty_cells(id: str):
#    nb_dict = pynblint.notebook_to_dict(id)
#    return {'data': pynblint.count_empty_cells(nb_dict)}
