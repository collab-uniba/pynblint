from fastapi import FastAPI
import pynblint

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Vincenzo'}}


@app.get('/notebook/{id}/empty_cells')
def empty_cells(filename: str):
    nb_dict = pynblint.notebook_to_dict(filename)
    return {'data': pynblint.count_empty_cells(nb_dict)}
