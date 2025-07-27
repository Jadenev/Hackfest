import json
import os
import pandas as pd
import warnings
from typing import Dict, Any

class DatasetLoader:
    def __init__(self, config_path: str = "datasets.json"):
        """
        Initialize the dataset loader with configuration
        
        Args:
            config_path: Path to datasets.json configuration file
        """
        self.config = self._load_config(config_path)
        self.data_dir = os.path.dirname(os.path.abspath(config_path))
        
        # Validate all dataset paths on startup
        self._validate_datasets()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load and validate the configuration file"""
        try:
            with open(config_path) as f:
                config = json.load(f)
            
            if "datasets" not in config:
                raise ValueError("Missing 'datasets' key in configuration")
                
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file: {config_path}")

    def _validate_datasets(self):
        """Check that all dataset files exist"""
        for name, config in self.config["datasets"].items():
            if "file_path" not in config:
                warnings.warn(f"⚠️ Dataset '{name}' missing 'file_path' in config")
                continue
                
            full_path = os.path.join(self.data_dir, config["file_path"])
            if not os.path.exists(full_path):
                warnings.warn(f"🧐 Dataset file not found: {full_path}")

    def list_datasets(self) -> list:
        """Return list of available dataset names"""
        return list(self.config["datasets"].keys())

    def load_dataset(self, name: str) -> pd.DataFrame:
        """
        Load a dataset by name
        
        Args:
            name: Name of the dataset to load
            
        Returns:
            pandas.DataFrame: Loaded dataset with metadata in .attrs
        """
        if name not in self.config["datasets"]:
            raise ValueError(f"Unknown dataset: {name}")
            
        config = self.config["datasets"][name]
        file_path = os.path.join(self.data_dir, config["file_path"])
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file not found: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            
            # Attach all non-path metadata to the dataframe
            df.attrs = {
                k: v for k, v in config.items() 
                if k != "file_path"
            }
            
            return df
            
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset '{name}': {str(e)}")

    def search_datasets(self, query: str) -> Dict[str, str]:
        """
        Search datasets by keyword
        
        Args:
            query: Search term
            
        Returns:
            Dict of matching datasets {name: description}
        """
        results = {}
        query = query.lower()
        
        for name, config in self.config["datasets"].items():
            if (query in name.lower() or 
                query in config.get("description", "").lower() or
                query in config.get("title", "").lower()):
                
                results[name] = config.get("description", "")
                
        return results

    def get_quick_task(self, dataset_name: str) -> Dict[str, Any]:
        """
        Get a quick analysis task for a dataset
        
        Args:
            dataset_name: Name of the dataset
            
        Returns:
            Dict with task details
        """
        if dataset_name not in self.config["datasets"]:
            raise ValueError(f"Unknown dataset: {dataset_name}")
            
        config = self.config["datasets"][dataset_name]
        
        return {
            "description": f"Analyze {config.get('title', dataset_name)} dataset",
            "steps": [
                f"Explore {config.get('columns', [])[:3]} columns",
                "Calculate summary statistics",
                "Visualize key relationships"
            ],
            "sample_code": config.get("sample_exercise_code", ""),
            "difficulty": config.get("difficulty", "intermediate")
        }

# Example usage
if __name__ == "__main__":
    loader = DatasetLoader()
    print("Available datasets:", loader.list_datasets())
    print("Avengers description:", loader.load_dataset("avengers").attrs.get("description"))