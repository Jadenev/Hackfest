import streamlit as st
from loader import DatasetLoader
from chatbot.integration import DataDevChatbot
from chatbot.colab_generator import ColabGenerator
import time

# ========== SETUP ========== #
st.set_page_config(
    page_title="miniDataDev - Your Friendly Data Coach",
    layout="wide",
    page_icon="🌱"
)

# Initialize core components
loader = DatasetLoader()

# Custom CSS for UI polish
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4e79a7 0%, #2e4a6b 100%);
    }
    .dataset-card {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .assistant-message {
        background-color: #f0f8ff;
        border-radius: 15px;
        padding: 12px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR ========== #
with st.sidebar:
    st.title("🌱 miniDataDev")
    st.markdown("**Your friendly data skills coach**")
    
    # Dataset selector
    selected_dataset = st.selectbox(
        "Choose a dataset:",
        loader.list_datasets(),
        key="dataset_selector"
    )
    
    # Dataset info card
    if selected_dataset:
        dataset = loader.load_dataset(selected_dataset)
        st.markdown(f"""
        <div class="dataset-card">
            <h4>{dataset.attrs.get('title', selected_dataset.title())}</h4>
            <p>{dataset.attrs.get('description', '')}</p>
            <div style="color: #666; font-size: 0.8em;">
                <b>Columns:</b> {', '.join(dataset.columns[:5])}...
            </div>
        </div>
        """, unsafe_allow_html=True)

# ========== MAIN INTERFACE ========== #
st.title("miniDataDev")
st.caption("Your gentle guide to data mastery")

# Initialize chatbot session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = DataDevChatbot(loader)
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your data mentor. Select a dataset and ask me anything about it!"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Clear chat button
if st.button("🔄 Clear Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat cleared! What would you like to explore?"}
    ]
    st.rerun()

# Quick action buttons
with st.expander("🚀 Quick Actions"):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Explain Dataset"):
            # Auto-trigger explanation
            st.session_state.messages.append({"role": "user", "content": "Explain this dataset"})
            st.rerun()
    with col2:
        if st.button("Suggest Exercise"):
            # Auto-trigger exercise
            st.session_state.messages.append({"role": "user", "content": "Suggest an exercise"})
            st.rerun()

# Chat input and processing
if prompt := st.chat_input("Ask about datasets or request exercises..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response with typing indicator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Get response from chatbot
            response = st.session_state.chatbot.respond(
                prompt,
                st.session_state.get("dataset_selector")
            )
            time.sleep(0.5)  # minimum delay UX
            
        # Display full response
        st.markdown(response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Handle Colab notebook generation
    if any(keyword in prompt.lower() for keyword in ["colab", "notebook"]):
        notebook_json = ColabGenerator.generate_notebook(
            st.session_state.dataset_selector,
            loader
        )
        st.download_button(
            "📥 Download Notebook",
            data=notebook_json,
            file_name=f"{st.session_state.dataset_selector}_practice.ipynb",
            mime="application/json"
        )