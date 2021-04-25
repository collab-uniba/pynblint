# JupyterNotebooksQuality
This repository contains the experimental work for the Bachelor Thesis by Vincenzo Romito.
## Description
The **utils.py** module contains all the functions representing the operationalization of the main best practices that you should keep in mind when writing a jupyter notebook.
As shown in the NotebookAnalysisResults notebook it is possible to call these functions in order to determine the quality degree of the target notebooks.
## Prerequisites
As a prerequisite you should have an installation of Anaconda or MiniConda on you device, check this link for more details https://docs.conda.io/projects/conda/en/latest/
## Installation
Use the terminal or an Anaconda Prompt for the following steps:
1. Create the environment from the environment.yml file:
```c
conda env create -f environment.yml
```
2. Activate the new environment: 
```c
conda activate myenv
```
3. Verify that the new environment was installed correctly:
```c
conda env list
```
At this point you should have succesfully created the virtual environment with the right dependencies<br>
Now it is time to create the kernel on which your notebook will run, open the terminal and type:
```c
python -m ipykernel install --user --name myenv
```
Now just select this kernel you created when running the NotebookAnalysisResults notebook.
## Reference paper
["A large-scale study about quality and reproducibility of jupyter notebooks."](http://www2.ic.uff.br/~leomurta/papers/pimentel2019a.pdf)
