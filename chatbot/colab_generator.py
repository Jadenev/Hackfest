import os
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from pathlib import Path

class ColabGenerator:
    def __init__(self, save_dir: str = "notebooks"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def build_notebook(self, dataset_name: str) -> str:
        """Create a starter Colab notebook for a dataset"""
        nb = new_notebook()
        
        # Add header
        nb.cells.append(new_markdown_cell(f"# {dataset_name} Analysis Notebook"))
        nb.cells.append(new_markdown_cell("## Dataset Overview"))
        nb.cells.append(new_code_cell(
            f"import pandas as pd\n"
            f"df = pd.read_csv('../data/{dataset_name}.csv')\n"
            f"df.head()"
        ))
        
        # Add analysis section
        nb.cells.append(new_markdown_cell("## Basic Analysis"))
        nb.cells.append(new_code_cell(
            "df.describe()\n"
            "df.info()\n"
            "df.isna().sum()"
        ))
        
        # Save notebook
        notebook_path = self.save_dir / f"{dataset_name}_analysis.ipynb"
        nbformat.write(nb, notebook_path)
        
        return str(notebook_path)