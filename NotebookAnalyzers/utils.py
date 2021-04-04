import json
import ast
from notebooktoall.transform import transform_notebook

def notebookToCode(filename):
    """The function takes the name of the desired .ipynb file in the target notebooks folder and return a python code string"""
    f=open("../TargetNotebooks/"+(filename),)
    data = json.load(f)
    code=[]
    for cell in data["cells"]:
        if cell["cell_type"] == 'code':
            code.append(''.join(cell["source"]))
    code = '\n'.join(code)
    return code

def notebookToPyFile(filename):
    #The function takes the name of the desired .ipynb file in the target notebooks folder, converts it into a .py file,
    #and returns the name of the .py file
    transform_notebook(ipynb_file="../TargetNotebooks/"+(filename), export_list=["py"])
    return filename.replace(".ipynb",".py")

def functionsNumber(filename):
    #The function takes a .py file and returns the number of function definitions thanks to the parse tree of the .py file
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())
        f_num=sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
    return f_num