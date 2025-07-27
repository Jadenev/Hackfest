import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional

class KaggleDatasetFetcher:
    def __init__(self, api_key: Optional[str] = None, download_dir: str = "data"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.api_key = api_key or os.getenv('KAGGLE_API_KEY')
        self._configure_kaggle()

    def _configure_kaggle(self):
        """Set up Kaggle API credentials"""
        if self.api_key:
            kaggle_dir = Path.home() / '.kaggle'
            kaggle_dir.mkdir(exist_ok=True)
            (kaggle_dir / 'kaggle.json').write_text(
                f'{{"username":"kaggle","key":"{self.api_key}"}}'
            )
            os.chmod(kaggle_dir / 'kaggle.json', 0o600)

    def search_datasets(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for datasets on Kaggle"""
        cmd = ["kaggle", "datasets", "list", "-s", query, "--csv"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return self._parse_search_results(result.stdout, max_results)
        except subprocess.CalledProcessError as e:
            return [{"error": e.stderr.strip()}]

    def _parse_search_results(self, csv_output: str, max_results: int) -> List[Dict]:
        """Parse Kaggle's CSV output"""
        lines = [line for line in csv_output.split('\n') if line.strip()][1:]  # Skip header
        return [
            {
                "title": line.split(',')[0].strip('"'),
                "ref": line.split(',')[1].strip('"'),
                "size": line.split(',')[2].strip('"'),
                "lastUpdated": line.split(',')[3].strip('"')
            }
            for line in lines[:max_results]
        ]

    def download_dataset(self, dataset_ref: str) -> str:
        """Download a dataset from Kaggle"""
        dataset_name = dataset_ref.split('/')[-1]
        dest_path = self.download_dir / dataset_name
        
        if dest_path.exists():
            shutil.rmtree(dest_path)
        
        cmd = [
            "kaggle", "datasets", "download",
            "-d", dataset_ref,
            "-p", str(self.download_dir),
            "--unzip"
        ]
        
        subprocess.run(cmd, check=True)
        return str(dest_path)