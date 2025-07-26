import streamlit as st
from loader import DatasetLoader
import pandas as pd
import matplotlib.pyplot as plt

# ========== SETUP ========== #
st.set_page_config(
    page_title="miniDataDev - Your Friendly Data Coach",
    layout="wide",
    page_icon="🌱"
)

#styling
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f9fafb;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 1rem;
        box-shadow: 2px 0 10px rgba(0,0,0,0.05);
    }
    
    /* Dataset cards */
    .dataset-card {
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #ffffff;
        border-left: 4px solid #4e79a7;
        transition: all 0.2s;
    }
    .dataset-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Chat bubbles */
    .user-message {
        background-color: #e3f2fd;
        border-radius: 15px 15px 0 15px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-radius: 15px 15px 15px 0;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
    /* Title bar */
    .title-bar {
        display: flex;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize loader
loader = DatasetLoader()

# ========== SIDEBAR ========== #
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #4e79a7;">🌿 Your Datasets</h2>
        <p style="color: #666;">Ready-to-use learning playgrounds</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display all datasets as cards
    for name in loader.config.keys():
        config = loader.config[name]
        with st.container():
            st.markdown(f"""
            <div class="dataset-card">
                <h4>{config['metadata'].get('title', name.title())}</h4>
                <p style="color: #666; font-size: 0.9rem;">{config['metadata']['description']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="background-color: #e3f2fd; 
                                color: #1976d2; 
                                padding: 0.2rem 0.5rem; 
                                border-radius: 12px; 
                                font-size: 0.8rem;">
                        {config['difficulty'].title()}
                    </span>
                    <button onclick="loadDataset('{name}')" 
                            style="border: none; 
                                   background: #4e79a7; 
                                   color: white; 
                                   padding: 0.3rem 0.8rem; 
                                   border-radius: 5px; 
                                   cursor: pointer;">
                        Explore
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ========== MAIN CONTENT ========== #
# Title bar
st.markdown("""
<div class="title-bar">
    <h1 style="margin: 0; color: #4e79a7;">miniDataDev</h1>
    <div style="flex-grow: 1;"></div>
    <span style="color: #666;">Your gentle guide to data mastery</span>
</div>
""", unsafe_allow_html=True)

# Chat area
st.markdown("""
<div style="margin-top: 2rem;">
    <h3 style="color: #4e79a7;">💬 Data Mentor Chat</h3>
    <p style="color: #666;">Ask me about datasets, exercises, or anything data-related!</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! I'm your data mentor. Which dataset would you like to explore today? I can help you analyze it or suggest practice exercises."}
    ]

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate a response (connect to your actual chatbot)
    if "avengers" in prompt.lower():
        response = "Great choice! The Avengers dataset is perfect for beginners. Try this exercise:\n\n" + loader.get_quick_task("avengers", 0)
    elif "help" in prompt.lower():
        response = "I can:\n• Explain datasets\n• Suggest exercises\n• Help debug your code\n• Find additional resources\n\nWhat would you like help with?"
    else:
        response = "I'd be happy to help with that! First, which dataset are you working with? You can choose from our collection on the left."
    
   # assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to display new messages
    st.experimental_rerun()

#dataset loading
st.markdown("""
<script>
function loadDataset(name) {
    // This would connect to your actual loading logic
    console.log("Loading dataset: " + name);
    // In a real implementation, you'd update the chat or display area
}
</script>
""", unsafe_allow_html=True)