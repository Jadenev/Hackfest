from typing import Optional
import pandas as pd
from data_loader.loader import DatasetLoader

class Explainer:
    def __init__(self, loader: DatasetLoader):
        self.loader = loader

    def explain_dataset(self, dataset_name: str) -> str:
        """Generate comprehensive dataset explanation"""
        try:
            dataset = self.loader.load_dataset(dataset_name)
            attrs = getattr(dataset, 'attrs', {})
            
            explanation = [
                f"# {attrs.get('title', dataset_name)}",
                f"**Description**: {attrs.get('description', 'No description available')}",
                "",
                "## Dataset Structure",
                f"- Rows: {len(dataset):,}",
                f"- Columns: {len(dataset.columns):,}",
                "",
                "### Key Columns",
                *[f"- {col}: {dataset[col].dtype}" for col in dataset.columns[:5]],
                *(["", "... (truncated)"] if len(dataset.columns) > 5 else [])
            ]
            return "\n".join(explanation)
        except Exception as e:
            return f"❌ Error explaining dataset: {str(e)}"

    def suggest_exercise(self, dataset_name: str) -> str:
        """Generate practical exercises for the dataset"""
        try:
            dataset = self.loader.load_dataset(dataset_name)
            attrs = getattr(dataset, 'attrs', {})
            
            exercise = [
                f"# {attrs.get('title', dataset_name)} Practice",
                "## Suggested Exercises",
                "1. **Basic Analysis**",
                "   - Calculate summary statistics",
                "   - Check for missing values",
                "",
                "2. **Visualization**",
                "   - Plot distributions of numerical columns",
                "   - Create correlation heatmap",
                "",
                "3. **Advanced**",
                "   - Build a simple predictive model",
                "   - Perform feature engineering"
            ]
            return "\n".join(exercise)
        except Exception as e:
            return f"❌ Error generating exercise: {str(e)}"