from fastapi import FastAPI, File, UploadFile
from typing import Optional
import os
import pynblint
import shutil
import config

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'message': 'Welcome to the pynblint API'}}

@app.post("/linters/nb-linter/")
async def nb_lint(notebook: UploadFile = File(...), bottom_size: Optional[int] = 4):
    with open(config.data_path+notebook.filename, "wb") as buffer:
        shutil.copyfileobj(notebook.file, buffer)
    script = pynblint.notebook_to_script(notebook.filename)
    nb_dict = pynblint.notebook_to_dict(notebook.filename)
    response = {
        "data": {
            "fileName": notebook.filename,
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
