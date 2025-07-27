from typing import Dict, List
import pandas as pd

class DataDevChatbot:
    def __init__(self, loader, explainer, notebook_builder, kaggle_fetcher):
        self.loader = loader
        self.explainer = explainer
        self.notebook_builder = notebook_builder
        self.kaggle_fetcher = kaggle_fetcher
        self.current_dataset = None

    def respond(self, query: str) -> str:
        """Handle user queries with contextual responses"""
        query = query.lower().strip()
        
        # Greeting responses
        if any(word in query for word in ['hi', 'hello', 'hey']):
            return "Hello! I'm your data analysis assistant. How can I help you today?"
        
        # Dataset-related questions
        elif 'dataset' in query or 'data' in query:
            datasets = self.loader.list_datasets()
            return f"I can help analyze these datasets: {', '.join(datasets)}\n\nTry asking: 'Explain the [dataset name] dataset' or 'Show me exercises for [dataset name]'"
        
        # Explanation requests
        elif 'explain' in query:
            dataset_name = self._extract_dataset_name(query)
            if dataset_name:
                return self.explainer.explain_dataset(dataset_name)
            return "Please specify which dataset to explain. Example: 'Explain the college_majors dataset'"
        
        # Exercise requests
        elif 'exercise' in query or 'practice' in query:
            dataset_name = self._extract_dataset_name(query)
            if dataset_name:
                return self.explainer.suggest_exercise(dataset_name)
            return "Please specify which dataset you want exercises for. Example: 'Give me exercises for avengers dataset'"
        
        # Statistical questions
        elif any(term in query for term in ['statistic', 'summary', 'describe', 'mean', 'median']):
            return self._handle_stats_question(query)
        
        # Visualization questions
        elif any(word in query for word in ['plot', 'visualize', 'graph', 'chart']):
            return self._handle_viz_question(query)
        
        # Default response
        return self._handle_unknown_query(query)

    def _extract_dataset_name(self, query: str) -> str:
        """Extract dataset name from query"""
        datasets = self.loader.list_datasets()
        for dataset in datasets:
            if dataset.lower() in query.lower():
                return dataset
        return None

    def _handle_stats_question(self, query: str) -> str:
        """Generate response for statistical questions"""
        dataset_name = self._extract_dataset_name(query)
        if dataset_name:
            return (
                f"For {dataset_name}, calculate summary statistics using:\n\n"
                "```python\n"
                f"df = pd.read_csv('data/{dataset_name}.csv')\n"
                "# For basic statistics:\n"
                "df.describe()\n\n"
                "# For specific columns:\n"
                "df['column_name'].mean()  # or .median(), .std() etc.\n"
                "```"
            )
        return (
            "To calculate summary statistics:\n\n"
            "```python\n"
            "df.describe()  # Basic stats for all numeric columns\n"
            "df['column'].mean()  # Average\n"
            "df['column'].median()  # Middle value\n"
            "df['column'].std()  # Standard deviation\n"
            "```"
        )

    def _handle_viz_question(self, query: str) -> str:
        """Generate response for visualization questions"""
        return (
            "You can create visualizations using:\n\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n\n"
            "# For a histogram:\n"
            "df['column'].plot(kind='hist')\n\n"
            "# For a scatter plot:\n"
            "df.plot.scatter(x='col1', y='col2')\n\n"
            "# For a correlation heatmap:\n"
            "sns.heatmap(df.corr(), annot=True)\n"
            "```"
        )

    def _handle_unknown_query(self, query: str) -> str:
        """Handle unrecognized queries"""
        return (
            f"I understand you're asking about: '{query}'\n\n"
            "I can help with:\n"
            "- Explaining datasets\n"
            "- Suggesting analysis exercises\n"
            "- Creating Jupyter notebooks\n"
            "- Calculating statistics\n"
            "- Data visualization\n\n"
            "Try asking:\n"
            "- 'How do I analyze the avengers dataset?'\n"
            "- 'Show me visualization examples'\n"
            "- 'Create a notebook for college_majors'"
        )