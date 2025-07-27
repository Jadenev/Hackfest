import streamlit as st
from loader import DatasetLoader
from chatbot.integration import DataDevChatbot
from chatbot.collab_generator import ColabGenerator
import time

# ========== SETUP ========== #
st.set_page_config(
    page_title="miniDataDev - Your Friendly Data Coach",
    layout="wide",
    page_icon="🌱"
)

# Custom CSS for improved visibility and styling
st.markdown("""
<style>
    /* Main sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4e79a7 0%, #2e4a6b 100%);
    }
    
    /* Dataset cards - improved contrast */
    .dataset-card {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #333333 !important;
        border-left: 4px solid #4e79a7;
    }
    .dataset-card h4 {
        color: #2e4a6b !important;
        margin-top: 0;
        font-size: 1.1rem;
    }
    .dataset-card p {
        color: #555555 !important;
        margin-bottom: 10px;
        font-size: 0.9rem;
    }
    .dataset-card small {
        color: #666666 !important;
        font-size: 0.8rem;
    }
    
    /* Chat bubbles */
    .stChatMessage {
        padding: 12px;
    }
    [data-testid="stChatMessageContent"] {
        font-size: 1rem;
    }
    
    /* Quick action buttons */
    .stButton>button {
        border: 1px solid #4e79a7 !important;
        background-color: #f0f8ff !important;
        color: #2e4a6b !important;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #e0f0ff !important;
        border-color: #3e699b !important;
    }
    
    /* Expander header */
    .stExpander [data-testid="stExpanderToggleIcon"] {
        color: #4e79a7 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize core components
loader = DatasetLoader()

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
            <div style="margin-top: 10px;">
                <small><b>Columns:</b> {', '.join(dataset.columns[:5])}...</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ========== MAIN INTERFACE ========== #
st.title("Data Skills Coach")
st.caption("Practice real data skills with guided assistance")

# Initialize chatbot session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = DataDevChatbot(loader)
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your data mentor. Select a dataset and ask me anything!"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Quick action buttons
with st.expander("🚀 Quick Actions", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Explain Dataset", use_container_width=True, key="explain_btn"):
            if 'dataset_selector' in st.session_state:
                st.session_state.messages.append({
                    "role": "user",
                    "content": f"Explain the {st.session_state.dataset_selector} dataset"
                })
                st.rerun()
            else:
                st.warning("Please select a dataset first")
    with col2:
        if st.button("💪 Suggest Exercise", use_container_width=True, key="exercise_btn"):
            if 'dataset_selector' in st.session_state:
                st.session_state.messages.append({
                    "role": "user", 
                    "content": f"Suggest an exercise for {st.session_state.dataset_selector}"
                })
                st.rerun()
            else:
                st.warning("Please select a dataset first")

# Chat input and processing
if prompt := st.chat_input("Ask about datasets or request exercises..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response with typing indicator
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = st.session_state.chatbot.respond(
                prompt,
                st.session_state.get("dataset_selector")
            )
            time.sleep(0.3)  # Small delay for better UX
            
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
            mime="application/json",
            key=f"notebook_{st.session_state.dataset_selector}"
        )