import json
import ast
from notebooktoall.transform import transform_notebook

def notebookToJson(filename):
    """The function takes the .ipynb file and returns it as a dictionary python object"""
    f=open("../TargetNotebooks/"+(filename),)
    data = json.load(f)
    return data

#def notebookToCode(data):
#    """The function takes the JSON of the target notebook and returns a python code string"""
#    code=[]
#    for cell in data["cells"]:
#        if cell["cell_type"] == 'code':
#            code.append(''.join(cell["source"]))
#    code = '\n'.join(code)
#    return code

def notebookToCode(filename):
    """The function takes the name of the desired .ipynb file in the target notebooks folder, and returns the python code sintax tree"""
    transform_notebook(ipynb_file="../TargetNotebooks/"+(filename), export_list=["py"])
    f = open(filename.replace(".ipynb",".py"),'r')
    py_code = f.read()
    return py_code

def functionsNumber(code):
    """The function takes a python code sintax tree and returns the number of function definitions"""
    tree = ast.parse(code)
    f_num=sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
    return f_num