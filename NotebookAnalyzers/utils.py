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

def markdownLines(notebook):
    """The function takes a dict representing a notebook and returns the number of markdown lines"""
    markdowns=0
    for cell in notebook["cells"]:
        if cell["cell_type"]=='markdown':
            rows=len(cell['source'])
            markdowns=markdowns+rows
    return markdowns

def markdownTitles(notebook):
    """The function takes a dict representing a notebook and returns the number of markdown titles"""
    titles=0
    for cell in notebook["cells"]:
        if cell["cell_type"]=='markdown':
            for row in cell['source']:
                if row.lstrip().startswith('#'):
                       titles=titles+1
    return titles

def markdownDistribution(notebook):
    """The function takes a dict representing a notebook and, dividing the notebook in four sections, 
    returns the percentage of markdown rows in each section out of the totalt markdown rows"""
    n_md_cells=0
    markdown_fir=0
    markdown_sec=0
    markdown_thi=0
    markdown_fou=0
    cells_number = len(notebook["cells"])
    cells_per_portion= int(cells_number/4)
    cell_count=0
    cell_portion=1
    for cell in notebook["cells"]:
        if cell["cell_type"]=='markdown':
            n_md_cells=n_md_cells+1
            if cell_portion==1:
                markdown_fir=markdown_fir+len(cell['source'])
            elif cell_portion==2:
                markdown_sec=markdown_sec+len(cell['source'])
            elif cell_portion==3:
                markdown_thi=markdown_thi+len(cell['source'])
            else:
                markdown_fou=markdown_fou+len(cell['source'])
        cell_count=cell_count+1 
        if cell_count >= cells_per_portion:
            if cell_portion<4:
                cell_count=0
                cell_portion=cell_portion+1
            else:
                break
    total_md_rows= markdown_fir+markdown_sec+markdown_thi+markdown_fou
    if(n_md_cells<4):
        return None
    else:
        return markdown_fir/total_md_rows,markdown_sec/total_md_rows,markdown_thi/total_md_rows,markdown_fou/total_md_rows