# chatbot/colab_generator.py
import json
from pathlib import Path
from datetime import datetime

class ColabGenerator:
    @staticmethod
    def generate_notebook(dataset_name: str, loader: DatasetLoader) -> str:
        """Generate Google Colab notebook JSON structure"""
        try:
            dataset = loader.load_dataset(dataset_name)
            attrs = dataset.attrs
            
            notebook = {
                "cells": [
                    self._create_markdown_cell(f"# {attrs.get('title', dataset_name)} Practice Notebook"),
                    self._create_markdown_cell(f"Generated on {datetime.now().strftime('%Y-%m-%d')}"),
                    self._create_code_cell("# Install required packages\n!pip install pandas matplotlib"),
                    self._create_code_cell("# Load dataset\nimport pandas as pd\n"
                                         f"df = pd.read_csv('{dataset_name}.csv')"),
                    self._create_markdown_cell("## Basic Exploration"),
                    self._create_code_cell("df.head()\ndf.info()"),
                    self._create_markdown_cell("## Suggested Exercise"),
                    self._create_code_cell(attrs.get('sample_exercise_code', 
                                                   "# Try analyzing the data\n# df.describe()\n# df['column'].value_counts()"))
                ],
                "metadata": {
                    "colab": {"name": f"{dataset_name}_practice.ipynb"},
                    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
                }
            }
            
            return json.dumps(notebook, indent=2)
        except Exception as e:
            return f"Error generating notebook: {str(e)}"
    
    @staticmethod
    def _create_markdown_cell(source: str) -> dict:
        return {"cell_type": "markdown", "metadata": {}, "source": [source]}
    
    @staticmethod
    def _create_code_cell(source: str) -> dict:
        return {"cell_type": "code", "metadata": {}, "source": [source], "execution_count": None, "outputs": []}