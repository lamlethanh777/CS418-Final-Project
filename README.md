# CS418-Final-Project

## 1. Folder structure:

- `src`:
  - `main`: Python code for submission.
  - `experiment`: Jupyter notebook for experiment, just like Google Colab, you can see the [installation guide below](#3-running-in-jupyter-notebook).
- `raw`: Prof Dinh Dien's provided data.
- `crawled`: data crawled from [VI-NA-UY-KI](http://www.hannom-rcv.org/wi/index.php) in json format.
- `extracted`: data extracted from raw data provided in json format.

## 2. Setup:

0. Have Python installed.
1. `` Ctrl + ` `` for terminal.
2. `python -m venv venv` for Windows, `python3 -m venv .venv` for other.
3. `venv/Scripts/activate` for Windows, `./venv/bin/activate` for other to activate the virtual.environment, remember to run the script inside this virtual environment.
4. Upgrade pip with `python -m pip install --upgrade pip`.
5. Install all the required library with `pip install --upgrade -r requirements.txt`.
6. Run the script by `python [file_name].py`.

## 3. Running in Jupyter Notebook:

1. Install Jupyter extension pack in VSCode: Jupyter, Jupyter Cell Tags, Jupyter Keymap, Jupyter Notebook, Jupyter Slide Show.

2. Install ipython, ipykernel:

   `pip install ipython ipykernel`

3. Running the following command will create a kernel that can be used to run jupyter notebook commands inside the virtual environment:

   `ipython kernel install --user --name=venv`

4. Open the corresponding notebook, choose the kernel `venv` and run the cells.

## 4. Branch conventions:

1. **No direct push** to the main branch, except **emergency case**.
2. Create a branch from the main branch whenever you want to add something new, with the corresponding name:
   **`[type_of_branch]/[name_of_task]-[additional_information]`**
   - `type_of_branch`: `feat` for something new, `fix` for bug-fixing.
   - `name_of_task`: `crawl`, `extract`, or `align`.
   - `additional_information`: optional
     For example: `feat/crawl`, `feat/extract-sinonom-from-pdf`, or `fix/align-levenshtein`.
3. After completing the task on that branch, open a Pull Request and call for other members to review.

## 5. Commit message convention:

A concise commit message should include: **`[action]: [objective]`**.
For example: `add: commit and branch conventions`, `fix: incorrect levenshtein implementation`.
