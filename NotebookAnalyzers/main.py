from fastapi import FastAPI
import pynblint

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Vincenzo'}}


@app.get('/notebook/{id}/empty_cells') #analyze_noteboo #analyze_repository
def empty_cells(id: str):
    nb_dict = pynblint.notebook_to_dict(id)
    return {'data': pynblint.count_empty_cells(nb_dict)}
