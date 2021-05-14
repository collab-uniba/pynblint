from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import Optional
import os
import pynblint
import shutil
import config
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


@app.post("/linters/nb-linter/")
async def nb_lint(notebook: UploadFile = File(...), bottom_size: int = Form(4)):
    with open(config.data_path+notebook.filename, "wb") as buffer:
        shutil.copyfileobj(notebook.file, buffer)
    script = pynblint.notebook_to_script(notebook.filename)
    nb_dict = pynblint.notebook_to_dict(notebook.filename)
    response = {
        "data": {
            "notebookName": notebook.filename,
            "notebookStats": {
                "numberOfCells": pynblint.count_cells(nb_dict),
                "numberOfMDCells": pynblint.count_md_cells(nb_dict),
                "numberOfCodeCells": pynblint.count_code_cells(nb_dict),
                "numberOfRawCells": pynblint.count_raw_cells(nb_dict)
            }
        },
        "lintingResults": {
            "linearExecutionOrder": pynblint.has_linear_execution_order(nb_dict),
            "numberOfClassDefinitions": pynblint.count_class_defs(script),
            "numberOfFunctionDefinitions": pynblint.count_func_defs(script),
            "allImportsInFirstCell": pynblint.are_imports_in_first_cell(script),
            "numberOfMarkdownLines": pynblint.count_md_lines(nb_dict),
            "numberOfMarkdownTitles": pynblint.count_md_titles(nb_dict),
            "bottomMarkdownLinesRatio": pynblint.get_bottom_md_lines_ratio(nb_dict),
            "nonExecutedCells": pynblint.count_non_executed_cells(nb_dict),
            "emptyCells: ": pynblint.count_empty_cells(nb_dict),
            "bottomNonExecutedCells": pynblint.count_bottom_non_executed_cells(nb_dict, bottom_size),
            "bottomEmptyCells": pynblint.count_bottom_empty_cells(nb_dict, bottom_size)

        }
    }
    os.remove(config.data_path+notebook.filename)
    os.remove(notebook.filename[:-5] + "py")
    return response


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
    return {"data": [{"id": linter_id, "description": linters_dict[linter_id].description} for linter_id in linters_dict]}
