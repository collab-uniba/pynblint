import json
import ast
from notebooktoall.transform import transform_notebook

def notebookToJson(filename):
    """The function takes the .ipynb file and returns it as a dictionary python object"""
    f=open("../TargetNotebooks/"+(filename),)
    data = json.load(f)
    f.close()
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
    f.close() 
    return py_code

def functionsNumber(code):
    """The function takes a python code and returns the number of function definitions"""
    tree = ast.parse(code)
    f_num=sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
    return f_num

def cellsCorrectOrder(notebook):
    """The function takes the notebook dictionary, it returns True if the cells are executed in the correct orded and False otherwise"""
    correct_exec=True
    counter=1
    for cell in notebook["cells"]:
        if cell["cell_type"] == 'code':
            if counter==cell['execution_count']:
                counter=counter+1
            else:
                if cell['source']!=[]:
                    correct_exec=False
    return correct_exec