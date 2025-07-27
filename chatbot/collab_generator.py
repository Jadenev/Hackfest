import json
from datetime import datetime
from typing import Dict, Any

class ColabGenerator:
    @staticmethod
    def generate_notebook(dataset_name: str, loader) -> str:
        """Generate Google Colab notebook JSON structure"""
        try:
            dataset = loader.load_dataset(dataset_name)
            attrs = dataset.attrs
            
            notebook = {
                "cells": [
                    ColabGenerator._create_markdown_cell(f"# {attrs.get('title', dataset_name)} Practice Notebook"),
                    ColabGenerator._create_markdown_cell(f"Generated on {datetime.now().strftime('%Y-%m-%d')}"),
                    ColabGenerator._create_code_cell("# Install required packages\n!pip install pandas matplotlib"),
                    ColabGenerator._create_code_cell(f"# Load dataset\nimport pandas as pd\n"
                                                   f"df = pd.read_csv('{dataset_name}.csv')"),
                    ColabGenerator._create_markdown_cell("## Basic Exploration"),
                    ColabGenerator._create_code_cell("df.head()\ndf.info()"),
                    ColabGenerator._create_markdown_cell("## Suggested Exercise"),
                    ColabGenerator._create_code_cell(attrs.get('sample_exercise_code', 
                                                             "# Try analyzing the data\n# df.describe()\n# df['column'].value_counts()"))
                ],
                "metadata": {
                    "colab": {"name": f"{dataset_name}_practice.ipynb"},
                    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
                },
                "nbformat": 4,
                "nbformat_minor": 0
            }
            
            return json.dumps(notebook, indent=2)
        except Exception as e:
            return f"Error generating notebook: {str(e)}"
    
    @staticmethod
    def _create_markdown_cell(source: str) -> Dict[str, Any]:
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": [source]
        }
    
    @staticmethod
    def _create_code_cell(source: str) -> Dict[str, Any]:
        return {
            "cell_type": "code",
            "metadata": {},
            "source": [source],
            "execution_count": None,
            "outputs": []
        }