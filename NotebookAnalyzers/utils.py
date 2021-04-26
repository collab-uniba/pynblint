import json
import ast
from notebooktoall.transform import transform_notebook


def notebook_to_json(filename):
    """
       Turns a notebook into a dictionary object

       Args:
           filename(str): name of the notebook file in the TargetNotebooks folder
       Returns:
           data: dictionary object representing the notebook

       A way you might use me is

       data = notebook_to_json("file.ipynb")
    """
    f = open("../TargetNotebooks/" + filename, )
    data = json.load(f)
    f.close()
    return data


def notebook_to_code(filename):
    """
       Extracts the code from a jupyter notebook in the TargetNotebooks folder

       Args:
           filename(str): name of the notebook file in the TargetNotebook folder
       Returns:
           py_code: string containing the python code from the jupyter notebook

       A way you might use me is

       py_code = notebook_to_code("file.ipynb")
    """
    transform_notebook(ipynb_file="../TargetNotebooks/" + filename, export_list=["py"])
    f = open(filename.replace(".ipynb", ".py"), 'r')
    py_code = f.read()
    f.close()
    return py_code


def functions_number(code):
    """
       Extracts the number of function definitions from a string of code

       Args:
           code(str): string of python code
       Returns:
           f_num: integer representing the number of function definitions in the code

       A way you might use me is

       f_num = functions_number(code)
    """
    tree = ast.parse(code)
    f_num = sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)
    return f_num


def not_executed_cells(notebook):
    """
        Number of non-executed cells from a dictionary representing the notebook

        Args:
            notebook(dic): python dictionary object representing the jupyter notebook
        Returns:
            not_exec_cells: integer representing the number of non-executed cells in the notebook

        A way you might use me is

        not_exec_cells = not_executed_cells(notebook_dict)
    """
    not_exec_cells = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] == 'code':
            if cell['execution_count'] is None and cell['source'] != []:
                not_exec_cells = not_exec_cells + 1  # This is a not executed Python Cell containing actual code
    return not_exec_cells


def empty_cells(notebook):
    """
        Number of empty cells from a dictionary representing the notebook

        Args:
            notebook(dic): python dictionary object representing the jupyter notebook
        Returns:
            empty_cells: integer representing the number of empty cells in the notebook

        A way you might use me is

        empty_cells = empty_cells(notebook_dict)
    """
    empty_cell = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] == 'code':
            if cell['execution_count'] is None and cell['source'] == []:
                empty_cell = empty_cell + 1  # This is an empty Python Cell
    return empty_cell


def markdown_lines(notebook):
    """
        Number of markdown rows from a dictionary representing the notebook

        Args:
            notebook(dic): python dictionary object representing the jupyter notebook
        Returns:
            markdowns: integer representing the number of markdown rows in the notebook

        A way you might use me is

        markdowns = markdowns(notebook_dict)
    """
    markdowns = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] == 'markdown':
            rows = len(cell['source'])
            markdowns = markdowns + rows
    return markdowns


def markdown_titles(notebook):
    """
        Number of markdown title rows from a dictionary representing the notebook

        Args:
            notebook(dic): python dictionary object representing the jupyter notebook
        Returns:
            titles: integer representing the number of markdown title rows in the notebook

        A way you might use me is

        titles = markdown_titles(notebook_dict)
    """
    titles = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] == 'markdown':
            for row in cell['source']:
                if row.lstrip().startswith('#'):
                    titles = titles + 1
    return titles


def markdown_distribution(notebook):
    """
        Distribution of markdown rows in the 4 sections of the notebook

        Args:
            notebook(dic): python dictionary object representing the jupyter notebook
        Returns:
            distributions: array of 4 elements, each number representing, for each quarter, the percentage of markdown rows out of the total rows
                           distributions[0] = percentage of markdown rows in the first 25% of the notebook
                           distributions[1] = percentage of markdown rows in the second quarter of the notebook
                           ...
        A way you might use me is

        distributions = markdown_distribution(notebook_dict)
    """
    n_md_cells = 0
    markdown_fir = 0
    markdown_sec = 0
    markdown_thi = 0
    markdown_fou = 0
    cells_number = len(notebook["cells"])
    cells_per_portion = int(cells_number / 4)
    cell_count = 0
    cell_portion = 1
    for cell in notebook["cells"]:
        if cell["cell_type"] == 'markdown':
            n_md_cells = n_md_cells + 1
            if cell_portion == 1:
                markdown_fir = markdown_fir + len(cell['source'])
            elif cell_portion == 2:
                markdown_sec = markdown_sec + len(cell['source'])
            elif cell_portion == 3:
                markdown_thi = markdown_thi + len(cell['source'])
            else:
                markdown_fou = markdown_fou + len(cell['source'])
        cell_count = cell_count + 1
        if cell_count >= cells_per_portion:
            if cell_portion < 4:
                cell_count = 0
                cell_portion = cell_portion + 1
            else:
                break
    total_md_rows = markdown_fir + markdown_sec + markdown_thi + markdown_fou
    if n_md_cells < 4:
        return None
    else:
        return markdown_fir/total_md_rows, markdown_sec/total_md_rows, \
               markdown_thi/total_md_rows, markdown_fou/total_md_rows


def imports_correct_position(code):
    """
        Verifies if there are no import statements in cells that are not the first one

        Args:
            code(str): string of python code
        Returns:
            correct_position: boolean value that is True if there are no imports other than those in the first cell of code and False otherwise

        A way you might use me is

        correct_position = imports_correct_position(code)
    """
    found_first_cell = False  # when True it means we found the first cell of code that has to be ignored
    second_cell_not_reached = True
    # when set to False we are actually reading instructions from the second cell of
    # code, from now on we need to analyze all the cells looking for import statements
    correct_position = True
    cell = ''
    program = code.split('\n')
    for line in program:
        if not found_first_cell:
            # it ignores all the lines before the first cell generated by nbconvert(python# version ecc.)
            if line[0:5] == '# In[':
                found_first_cell = True
        elif not second_cell_not_reached:
            # starting from the second cell it saves all the instructions until it find a new cell
            if line[0:5] != '# In[':
                cell = cell + '\n' + line
            else:
                tree = ast.parse(cell)
                # once it finds a new cell it verifies if there are any imports statement in the previous cell
                if sum(isinstance(exp, ast.Import) for exp in tree.body) > 0:
                    correct_position = False
                    break
        else:
            if line[0:5] == '# In[':
                # following instructions are from the second cell of code, the first one we have to analyze
                second_cell_not_reached = False
    return correct_position


def cells_correct_order(notebook):
    """The function takes a dict representing notebook dictionary, it returns True if the cells are executed in
    sequential order,starting from 1, and False otherwise """
    """
        Verifies if the notebook has been run in sequential order, starting from 1

        Args:
            notebook(dic): python dictionary object representing the jupyter notebook
        Returns:
            correct_exec: boolean value that is True if notebook cells have been sequentially run top to bottom

        A way you might use me is

        correct_exec = cells_correct_order(notebook_dict)
    """
    correct_exec = True
    counter = 1
    for cell in notebook["cells"]:
        if cell["cell_type"] == 'code':
            if counter == cell['execution_count']:
                counter = counter + 1
            else:
                if cell['source']:
                    correct_exec = False
    return correct_exec


def classes_number(code):
    """The function takes a python code string and returns the number of class definitions"""
    """
        Extract the number of class definitions from a python code

        Args:
            code(str): string of python code
        Returns:
            class_def_num: interger value representing the number of class definitions in the python code

        A way you might use me is

        class_def_num = classes_number(code)
    """
    tree = ast.parse(code)
    class_def_num = sum(isinstance(exp, ast.ClassDef) for exp in tree.body)
    return class_def_num
