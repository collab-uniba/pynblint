import json
def notebookToCode(filename):
    """The function takes the name of the desired .ipynb file in the target notebooks folder and return a python code string"""
    f=open("../TargetNotebooks/"+(filename),)
    data = json.load(f)
    code=[]
    for cell in data["cells"]:
        if cell["cell_type"] == 'code':
            code.append(''.join(cell["source"]))
    code = ''.join(code)
    return code

def functionsNumber(code):
    """The function takes the a python code string and return the number of declared functions in it"""
    return code.count("def ")