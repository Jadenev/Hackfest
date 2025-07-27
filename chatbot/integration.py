from loader import DatasetLoader
import streamlit as st
import pandas as pd

class DataDevChatbot:
    def __init__(self, loader: DatasetLoader):
        self.loader = loader
        self._initialize_flows()
    
    def _initialize_flows(self):
        """Initialize conversation handlers"""
        self.flows = {
            'explanation': self._explain_dataset,
            'exercise': self._suggest_exercise,
            'search': self._search_datasets,
            'colab': self._generate_colab_notebook
        }
    
    def respond(self, user_input: str, current_dataset: str = None) -> str:
        """Main response generator"""
        input_lower = user_input.lower()
        
        if any(x in input_lower for x in ['explain', 'tell me about']):
            return self.flows['explanation'](current_dataset)
        elif any(x in input_lower for x in ['exercise', 'practice']):
            return self.flows['exercise'](current_dataset)
        elif any(x in input_lower for x in ['find', 'search']):
            return self.flows['search'](user_input)
        elif any(x in input_lower for x in ['colab', 'notebook']):
            return self.flows['colab'](current_dataset)
        else:
            return self._get_help_message()

    # ===== CORE METHODS =====
    
    def _explain_dataset(self, dataset_name: str) -> str:
        """Explain the selected dataset"""
        if not dataset_name:
            return "Please select a dataset first from the sidebar."
        
        try:
            dataset = self.loader.load_dataset(dataset_name)
            attrs = dataset.attrs
            
            explanation = f"""
            ## {attrs.get('title', dataset_name)} Dataset
            
            **Description:** {attrs.get('description', 'No description available')}
            
            **Columns:** {', '.join(dataset.columns)}
            **Sample Questions:**
            - {attrs.get('example_questions', ['No example questions'])[0]}
            - {attrs.get('example_questions', [''])[1] if len(attrs.get('example_questions', [])) > 1 else ''}
            
            Try exploring with: `df.head()` or `df.describe()`
            """
            return explanation
            
        except Exception as e:
            return f"Error explaining dataset: {str(e)}"

    def _suggest_exercise(self, dataset_name: str) -> str:
        """Suggest an exercise for the dataset"""
        if not dataset_name:
            return "Please select a dataset first to get exercises."
        
        try:
            task = self.loader.get_quick_task(dataset_name)
            return f"""
            **Try this exercise:** {task['description']}
            
            **Steps:**
            1. {task['steps'][0]}
            2. {task['steps'][1]}
            3. {task['steps'][2]}
            
            **Sample Code:**
            ```python
            {task.get('sample_code', '# Your code here')}
            ```
            """
        except Exception as e:
            return f"Error suggesting exercise: {str(e)}"

    def _search_datasets(self, query: str) -> str:
        """Search available datasets"""
        try:
            results = self.loader.search_datasets(query.replace('find', '').replace('search', '').strip())
            
            if not results:
                return "No datasets found matching your search."
                
            response = "**Found these datasets:**\n\n"
            for name, desc in results.items():
                response += f"- **{name}**: {desc}\n"
                
            return response
            
        except Exception as e:
            return f"Search failed: {str(e)}"

    def _generate_colab_notebook(self, dataset_name: str) -> str:
        """Generate Colab notebook message"""
        if not dataset_name:
            return "Please select a dataset first to generate a notebook."
        return "Click the download button below to get your Colab notebook!"

    def _get_help_message(self) -> str:
        """Default help message"""
        return """
        **How I can help:**
        - Explain datasets: _"Tell me about the Avengers data"_
        - Suggest exercises: _"Give me a beginner exercise"_
        - Search datasets: _"Find datasets about music"_
        - Create notebooks: _"Make me a Colab notebook"_
        
        Select a dataset from the sidebar to begin!
        """