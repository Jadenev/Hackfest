import os
import pandas as pd
from typing import Dict, List
from pathlib import Path

class DatasetLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.datasets = self._discover_datasets()

    def _discover_datasets(self) -> Dict[str, Path]:
        """Find all available datasets in data directory"""
        return {
            f.stem: f for f in self.data_dir.glob("*.csv")
            if f.is_file()
        }

    def list_datasets(self) -> List[str]:
        """List names of available datasets"""
        return list(self.datasets.keys())

    def load_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Load a dataset by name"""
        if dataset_name not in self.datasets:
            raise ValueError(f"Dataset '{dataset_name}' not found")
        
        df = pd.read_csv(self.datasets[dataset_name])
        
        # Add basic metadata as attributes
        df.attrs = {
            'title': dataset_name.replace('_', ' ').title(),
            'description': f"Dataset with {len(df)} rows and {len(df.columns)} columns",
            'columns': list(df.columns)
        }
        
        return df