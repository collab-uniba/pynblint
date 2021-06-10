from pynblint.notebook import Notebook
from pathlib import Path

if __name__ == '__main__':
    nb = Notebook(Path('../fixtures') / Path('my-attempt-at-analytics-vidhya-job-a-thon.ipynb'))
    print(nb.get_pynblint_results())
