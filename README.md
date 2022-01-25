# Pynblint

[![CI](https://github.com/collab-uniba/pynblint/actions/workflows/CI.yml/badge.svg)](https://github.com/collab-uniba/pynblint/actions/workflows/CI.yml)
[![codecov](https://codecov.io/gh/collab-uniba/pynblint/branch/master/graph/badge.svg?token=CSX10BJ1CU)](https://codecov.io/gh/collab-uniba/pynblint)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Description
In [1], Pimentel et al. report the results a large-scale study on the quality and reproducibility of Jupyter notebooks. At the end of the paper, in the light of their findings, the authors recommend a set of 8 best practices for Jupyter notebooks writing.

We operationalized some of these best practices and built a little library of functions (contained in the `pynblint` package) that enable the quantitative assessment of their adoption in a dataset of Jupyter notebooks.
As shown in `Using pynblint.ipynb`, the functions from our library can be easily adopted to collect data about specific aspects of notebooks quality (e.g., the length of markdown descriptions or the evidence of linear execution order of cells) and repository quality(e.g., duplicate notebooks' filenames, untitled notebooks).
## Prerequisites
It is recommanded to have an installation of a virtual environment tool on your device, such as Conda, Pipenv, VirtualEnv.
## Installation
Use the terminal or a virtual environment prompt to perform the following steps:
1. Install the dependencies using the `requirements.txt` file:
- Windows:
```bash
py -m pip install -r requirements.txt
```
- Unix/MacOS:
```bash
python -m pip install -r requirements.txt
```
2. At this point you should have succesfully created the virtual environment with the right dependencies<br>
Now it is time to create the kernel on which your notebook will run, for example, in a Conda environment, open the terminal and type:
```bash
python -m ipykernel install --user --name myenv
```
for more help on this matter, check this link: https://ipython.readthedocs.io/en/stable/install/kernel_install.html<br>
Now just select this kernel you created when running the `Using pynblint.ipynb` notebook.<br><br>
`pynblint` is a distributable package, it is installable thanks to its `setup.py` file:<br>
1. cd into the root directory where setup.py is located
2. Enter:
```bash
python setup.py install
```
## Generate the documentation
In order to build the docs for the first time - e.g., to generate a documentation in the HTML format - type:
```bash
sphinx-build -b html <source_directory> <builddir>
```
and then:
```bash
make html
```
This will build HTML docs in the build directory you chose. Execute `make` without an argument to see which targets are available.<br>
Check Sphinx documentation for more info about documentation generation: https://www.sphinx-doc.org/en/master/usage/quickstart.html

## Reference paper
[1] [Pimentel et al., "A large-scale study about quality and reproducibility of jupyter notebooks."](http://www2.ic.uff.br/~leomurta/papers/pimentel2019a.pdf)
