import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import warnings
import matplotlib as plt

class DatasetLoader:
    def __init__(self, config_path: str = "datasets.json"):
        """
        A friendly dataset loader that makes data exploration easy and enjoyable.
        Handles both local and remote datasets with care.
        """
        self.config = self._load_config(config_path)
        self._verify_data_sources()
        print("🌟 DatasetLoader ready! Loaded", len(self.config), "datasets")

    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load configuration with gentle error handling"""
        try:
            with open(Path(__file__).parent / path) as f:
                config = json.load(f)
                print(f"🌱 Loaded configuration from {path}")
                return self._convert_legacy_format(config['datasets'])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            warnings.warn(f"Using built-in datasets (couldn't load {path}: {str(e)})")
            return self._default_config()

    def _convert_legacy_format(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Convert metadata with kindness - preserving all original info"""
        return {
            name: {
                "url": config["source"],
                "difficulty": config.get("difficulty", "medium"),
                "key_columns": list(config["columns"].keys()),
                "quick_tasks": [
                    f"{task['title']}: {'; '.join(task['tasks'])}"
                    for task in config.get("starter_exercises", [])
                ],
                "preprocessing": "",
                "metadata": {
                    k: v for k, v in config.items() 
                    if k not in ["source", "columns"]
                }
            }
            for name, config in metadata.items()
        }

    def _default_config(self) -> Dict[str, Any]:
        """Our carefully curated default datasets"""
        return {
            "avengers": {
                "url": "https://raw.githubusercontent.com/fivethirtyeight/data/master/avengers/avengers.csv",
                "difficulty": "easy",
                "key_columns": ["Name", "Death1", "Gender", "Year"],
                "quick_tasks": [
                    "df[df['Gender'] == 'Female'].shape[0]  # Count female characters",
                    "df.groupby('Year')['Death1'].sum().plot()  # Deaths by year"
                ],
                "preprocessing": "",
                "metadata": {
                    "title": "Marvel Avengers",
                    "description": "Explore character deaths and resurrections in Marvel comics",
                    "tags": ["comics", "entertainment"],
                    "fun_fact": "Did you know? Spider-Man has died 8 times in the comics!"
                }
            },
            "majors": {
                "url": "https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/majors-list.csv",
                "difficulty": "medium",
                "key_columns": ["Major", "Major_category", "Total"],
                "quick_tasks": [
                    "df.nlargest(10, 'Total')  # Top 10 most popular majors",
                    "df['Major_category'].value_counts().plot.pie()  # Major categories"
                ],
                "preprocessing": "",
                "metadata": {
                    "title": "College Majors",
                    "description": "Discover salary trends across different college degrees",
                    "tags": ["education", "economics"],
                    "fun_fact": "Petroleum engineering majors earn the highest starting salaries!"
                }
            },
            "lyrics": {
                "url": "https://raw.githubusercontent.com/fivethirtyeight/data/master/hip-hop-candidate-lyrics/genius_hip_hop_lyrics.csv",
                "difficulty": "medium",
                "key_columns": ["artist", "album", "candidate", "sentiment"],
                "quick_tasks": [
                    "df['candidate'].value_counts().plot(kind='bar')  # Candidate mentions",
                    "df.groupby('artist')['sentiment'].mean().sort_values()  # Sentiment by artist"
                ],
                "preprocessing": """
# Clean sentiment scores with care
df['sentiment'] = pd.to_numeric(df['sentiment'], errors='coerce')""",
                "metadata": {
                    "title": "Hip-Hop Lyrics",
                    "description": "Analyze political candidate mentions in hip-hop songs",
                    "tags": ["music", "politics"],
                    "fun_fact": "Trump was mentioned more than Clinton in 2016 hip-hop lyrics"
                }
            },
            "masculinity": {
                "url": "https://raw.githubusercontent.com/fivethirtyeight/data/master/masculinity-survey/masculinity-survey.csv",
                "difficulty": "hard",
                "key_columns": ["question", "response", "count", "percentage"],
                "quick_tasks": [
                    "df[df['question'].str.contains('important')]  # Filter questions about importance",
                    "df.pivot(index='question', columns='response', values='count').plot.barh(stacked=True)  # Stacked responses"
                ],
                "preprocessing": """
# Convert percentages with precision
df['percentage'] = df['percentage'].str.rstrip('%').astype('float')""",
                "metadata": {
                    "title": "Masculinity Survey",
                    "description": "Explore American men's views on modern masculinity",
                    "tags": ["sociology", "gender"],
                    "fun_fact": "48% of men believe society puts pressure on them to behave in a certain way"
                }
            }
        }

    def _verify_data_sources(self):
        """Check if sources are accessible with friendly warnings"""
        for name, config in self.config.items():
            if not config["url"].startswith("http"):
                if not Path(config["url"]).exists():
                    warnings.warn(f"🧐 Dataset '{name}' points to a local file that doesn't exist: {config['url']}")
            # TODO: Add actual remote URL checking

    def load(self, name: str, sample_frac: Optional[float] = None) -> Optional[pd.DataFrame]:
        """
        Load a dataset with love and care.
        
        Args:
            name: The name of your chosen dataset
            sample_frac: Optional fraction to sample (0.1 = 10%)
            
        Returns:
            A pandas DataFrame wrapped in a warm blanket of metadata
        """
        if name not in self.config:
            available = list(self.config.keys())
            raise ValueError(f"🤷‍♂️ Dataset '{name}' not found. Available datasets: {', '.join(available)}")

        config = self.config[name]
        
        try:
            print(f"📦 Loading {name} dataset...")
            df = pd.read_csv(
                config["url"],
                encoding='latin-1',
                on_bad_lines='warn'
            )
            
            # Apply preprocessing
            if config["preprocessing"]:
                print(f"✨ Applying preprocessing to {name}")
                exec(config["preprocessing"], globals(), {'df': df})
            
            # Sampling
            if sample_frac:
                print(f"🔍 Sampling {sample_frac*100}% of {name}")
                df = df.sample(frac=sample_frac, random_state=42)
            
            # Wrap in metadata
            df.attrs = {
                **config.get("metadata", {}),
                "difficulty": config["difficulty"],
                "key_columns": config["key_columns"],
                "quick_tasks": config["quick_tasks"],
                "dataset_name": name,
                "colab_url": self.get_colab_url(name)
            }
            
            print(f"✅ Successfully loaded {name} with {len(df)} rows")
            return df
            
        except Exception as e:
            raise RuntimeError(f"❌ Oh no! Couldn't load {name}: {str(e)}")

    def get_datasets_by_difficulty(self, level: str) -> List[str]:
        """Find datasets matching your comfort level"""
        return [name for name, config in self.config.items() 
                if config["difficulty"] == level]

    def get_quick_task(self, dataset_name: str, index: int = 0) -> str:
        """Get a friendly exercise suggestion"""
        return self.config.get(dataset_name, {}).get("quick_tasks", [""])[index]

    def search_datasets(self, query: str) -> Dict[str, Any]:
        """Helpful search across datasets"""
        results = {}
        query = query.lower()
        
        for name, config in self.config.items():
            matches = []
            
            # Search name and description
            if query in name.lower():
                matches.append("name")
            if query in config.get("metadata", {}).get("description", "").lower():
                matches.append("description")
            
            # Search tags
            if any(query in tag.lower() 
                   for tag in config.get("metadata", {}).get("tags", [])):
                matches.append("tag")
            
            if matches:
                results[name] = {
                    "title": config.get("metadata", {}).get("title", name),
                    "matches": matches,
                    "description": config.get("metadata", {}).get("description", "")
                }
        
        return results

    def get_colab_url(self, name: str) -> Optional[str]:
        """Generate a Google Colab playground link"""
        if name in self.config and self.config[name]["url"].startswith("http"):
            return self.config[name]["url"].replace(
                "raw.githubusercontent.com",
                "colab.research.google.com/github"
            )
        return None

    def get_dataset_info(self, name: str) -> Dict[str, Any]:
        """Get all the details about a dataset"""
        if name not in self.config:
            raise ValueError(f"Dataset '{name}' not found")
        return {
            **self.config[name],
            "colab_url": self.get_colab_url(name)
        }


# easy test
if __name__ == "__main__":
    print("\n=== miniDataDev Dataset Loader ===\n")
    loader = DatasetLoader()
    
    # Try loading a dataset
    try:
        df = loader.load("avengers")
        print("\nHere's a peek at the Avengers data:")
        print(df.head())
        
        print("\nMetadata:", df.attrs)
        
        print("\nSearch results for 'music':")
        print(loader.search_datasets("music"))
        
    except Exception as e:
        print(f"\n⚠️ Something went wrong: {e}")