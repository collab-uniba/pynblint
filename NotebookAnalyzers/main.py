from fastapi import FastAPI
import pynblint
import linters

app = FastAPI()
nb_linter = linters.NbLinter()
repo_linter = linters.RepoLinter()


@app.get('/')
def index():
    return {'data': {'message': 'Welcome to the pynblint API'}}


@app.get('/linters/{linter_id}')
def linters_descr(linter_id: str):
    if linter_id == getattr(nb_linter, 'id'):
        return {'data': getattr(nb_linter, 'description')}
    elif linter_id == getattr(repo_linter, 'id'):
        return {'data': getattr(repo_linter, 'description')}
    else:
        return {'data': 'No linter found!'}


#@app.get('/notebook/{id}/empty_cells') #analyze_noteboo #analyze_repository
#def empty_cells(id: str):
#    nb_dict = pynblint.notebook_to_dict(id)
#    return {'data': pynblint.count_empty_cells(nb_dict)}
