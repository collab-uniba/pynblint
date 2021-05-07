from fastapi import FastAPI
import pynblint

app = FastAPI()

nb_linter_descr = {"id": "nb-linter", "description": "Lints Python Jupyter notebooks, one at a time."}
repo_linter_descr = {"id": "repo-linter", "description": "Lints all Jupyter notebooks in a Python project."}


@app.get('/')
def index():
    return {'data': {'name': 'This is a notebook linter API'}}


@app.get('/linters')
def linters_descr():
    return {"data": [nb_linter_descr, repo_linter_descr]}


#@app.get('/notebook/{id}/empty_cells') #analyze_noteboo #analyze_repository
#def empty_cells(id: str):
#    nb_dict = pynblint.notebook_to_dict(id)
#    return {'data': pynblint.count_empty_cells(nb_dict)}
