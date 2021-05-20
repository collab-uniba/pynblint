# pynblint
This repository contains the experimental work for the Bachelor Thesis by Vincenzo Romito.
## Description
In [1], Pimentel et al. report the results a large-scale study on the quality and reproducibility of Jupyter notebooks. At the end of the paper, in the light of their findings, the authors recommend a set of 8 best practices for Jupyter notebooks writing. 

We operationalized some of these best practices and built a little library of functions (contained in the `pynblint.py` module) that enable the quantitative assessment of their adoption in a dataset of Jupyter notebooks.
As shown in `NotebookAnalysisResults.ipynb`, the functions from our library can be easily adopted to collect data about specific aspects of notebooks quality (e.g., the length of markdown descriptions or the evidence of linear execution order of cells).
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
## Run the web API
Use the terminal or an Anaconda Prompt for the following steps:
1. Move to the folder containing the main.py fastAPI module
2. Run it with the following command:
```c
uvicorn main:app --reload
```
The reload command makes the server restart after code changes. Only do this for development.<br>
3. You will get a response with address and port on which the server is running, otherwise you will get some kind of error
## Reference paper
[1] [Pimentel et al., "A large-scale study about quality and reproducibility of jupyter notebooks."](http://www2.ic.uff.br/~leomurta/papers/pimentel2019a.pdf)
