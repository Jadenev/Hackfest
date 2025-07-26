# chatbot/integration.py
from loader import DatasetLoader
import streamlit as st
import random
from loader import DatasetLoader

class DataDevChatbot:
    def __init__(self, loader: DatasetLoader):
        self.loader = loader
        self._initialize_flows()
    ##
    def _initialize_flows(self):
        """Pre-defined conversation patterns"""
        self.flows = {
            'explanation': self._explain_dataset,
            'exercise': self._suggest_exercise,
            'search': self._search_datasets,
            'colab': self._generate_colab_notebook
        }
    
    def respond(self, user_input: str, current_dataset: str = None) -> str:
        """Response generator"""
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
            return """Here's what I can help with:
- **Explain datasets**: "Tell me about the Avengers data"
- **Suggest exercises**: "Give me a beginner exercise" 
- **Search datasets**: "Find datasets about music"
- **Generate notebooks**: "Make me a Colab notebook"

What would you like to do?"""
        def _search_datasets(self, search_query: str) -> str: """Handle dataset search requests"""
        try:
            # Remove the 'find' or 'search' keywords from the query
            clean_query = search_query.replace('find', '').replace('search', '').strip()
            
            # Get matching datasets from the loader
            results = self.loader.search_datasets(clean_query)
            
            if not results:
                return "🔍 No datasets found matching your search. Try different keywords."
            
            response = "🔍 I found these datasets:\n\n"
            for name, metadata in results.items():
                response += f"• **{name}**: {metadata.get('description', 'No description available')}\n"
            
            return response
        except Exception as e:
            return f"⚠️ Search failed: {str(e)}"

    def _generate_colab_notebook(self, dataset_name: str) -> str:
        """Handle Colab notebook generation requests"""
        if not dataset_name:
            return "ℹ️ Please select a dataset first from the sidebar to generate a notebook."
        
        try:
            # This message will appear while the download button is being prepared
            return (f"📓 Ready to generate a Colab notebook for {dataset_name}! "
                   "The download button should appear below shortly...")
        except Exception as e:
            return f"⚠️ Notebook generation failed: {str(e)}"