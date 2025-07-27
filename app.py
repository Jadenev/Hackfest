import os
import base64
import streamlit as st
from data_loader.loader import DatasetLoader
from chatbot.explainer import Explainer
from chatbot.colab_generator import ColabGenerator
from chatbot.kaggle_fetcher import KaggleDatasetFetcher
from chatbot.integration import DataDevChatbot

# Custom CSS styling
st.markdown("""
<style>
    .stApp {
        background-color: #5b8cba;
        background-image: linear-gradient(315deg, #5b8cba 0%, #4a6fa5 74%);
    }
    .title-wrapper {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .title-emoji {
        font-size: 2.5rem;
        margin-right: 10px;
    }
    .title-text {
        color: #f0f8ff;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    .notebook-link {
        background-color: rgba(255,255,255,0.9);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-left: 4px solid #f0f8ff;
    }
    .download-btn {
        background-color: #4a6fa5 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }
    .chat-container {
        background-color: rgba(255,255,255,0.9);
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        background-color: rgba(255,255,255,0.9) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    .stButton>button {
        border-radius: 8px !important;
        padding: 8px 16px !important;
        transition: all 0.3s !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    .st-chat-message {
        padding: 12px 16px !important;
        border-radius: 12px !important;
        margin: 8px 0 !important;
    }
    .user-message {
        background-color: #e3f2fd !important;
    }
    .assistant-message {
        background-color: #f5f5f5 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_services():
    """Initialize and return all service components"""
    try:
        loader = DatasetLoader()
        explainer = Explainer(loader)
        notebook_builder = ColabGenerator()
        kaggle_fetcher = KaggleDatasetFetcher(api_key=os.getenv('KAGGLE_API_KEY'))
        
        chatbot = DataDevChatbot(
            loader=loader,
            explainer=explainer,
            notebook_builder=notebook_builder,
            kaggle_fetcher=kaggle_fetcher
        )
        return loader, explainer, notebook_builder, kaggle_fetcher, chatbot
    except Exception as e:
        st.error(f"Service initialization failed: {str(e)}")
        raise

def main():
    # Custom title with emoji and styling
    st.markdown("""
    <div class="title-wrapper">
        <div class="title-emoji">🌿</div>
        <div class="title-text"><h1>miniDataDev</h1></div>
    </div>
    <p style='color:#f0f8ff; font-size: 1.1rem;'>Your friendly data analysis assistant</p>
    """, unsafe_allow_html=True)
    
    try:
        with st.spinner("Loading services..."):
            loader, explainer, notebook_builder, kaggle_fetcher, chatbot = load_services()

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! I can help you analyze datasets. Ask me anything!"}]

        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📂 Datasets", divider="blue")
            dataset_names = loader.list_datasets()
            selected_dataset = st.selectbox("Choose a dataset", dataset_names)
            
            if st.button("🔍 Explain Dataset", use_container_width=True):
                with st.expander("Dataset Explanation", expanded=True):
                    st.markdown(explainer.explain_dataset(selected_dataset))
            
            if st.button("💡 Suggest Exercise", use_container_width=True):
                with st.expander("Practice Exercise", expanded=True):
                    st.markdown(explainer.suggest_exercise(selected_dataset))
            
            if st.button("📝 Create Notebook", use_container_width=True):
                notebook_path = notebook_builder.build_notebook(selected_dataset)
                notebook_name = os.path.basename(notebook_path)
                
                with open(notebook_path, "rb") as f:
                    notebook_bytes = f.read()
                
                st.markdown(f"""
                <div class="notebook-link">
                    <h4 style='color:#2c3e50;'>🎉 Notebook Ready!</h4>
                    <p style='color:#2c3e50;'><strong>Saved to:</strong> <code style='background:#f5f5f5; padding:2px 4px; border-radius:4px;'>{os.path.abspath(notebook_path)}</code></p>
                    <div style="margin-top:12px;">
                        <a href="data:application/x-ipynb+json;base64,{base64.b64encode(notebook_bytes).decode()}" 
                           download="{notebook_name}" 
                           class="download-btn">
                           ⬇️ Download Notebook
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.subheader("💬 Chat Assistant", divider="blue")
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Chat input
            if prompt := st.chat_input("Ask me anything about data analysis"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Display user message
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Get AI response
                with st.chat_message("assistant", avatar="🌿"):
                    response = chatbot.respond(prompt)
                    st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Application error: {str(e)}")

if __name__ == "__main__":
    main()