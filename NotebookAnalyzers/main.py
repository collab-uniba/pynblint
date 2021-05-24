from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import Optional
import os
import pynblint
import shutil
import config
import linters
from entities import Notebook, GitHubRepository, LocalRepository
from pathlib import Path

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


@app.post("/linters/nb-linter/")
async def nb_lint(notebook: UploadFile = File(...), bottom_size: int = Form(4)):
    with open( Path(config.data_path) / notebook.filename, "wb") as buffer:
        shutil.copyfileobj(notebook.file, buffer)
    nb = Notebook(Path(config.data_path) / notebook.filename)
    os.remove(Path(config.data_path) / notebook.filename)
    return nb.get_pynblint_results()

@app.post("/linters/repo-linter/")
async def nb_lint(local_project: UploadFile = File(...), bottom_size: int = Form(4)):
    with open( Path(config.data_path) / local_project.filename, "wb") as buffer:
        shutil.copyfileobj(local_project.file, buffer)
    try:
        project = LocalRepository(Path(config.data_path) / local_project.filename)
        os.remove(Path(config.data_path) / local_project.filename)
        return project.get_pynblint_results()
    except Exception:
        os.remove(Path(config.data_path) / local_project.filename)
        raise HTTPException(status_code=400, detail="Bad request")

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


@app.get('/linters')
def get_linters_list():
    return {
        "data": [{"id": linter_id, "description": linters_dict[linter_id].description} for linter_id in linters_dict]}
