import streamlit as st
from model3 import generate_content  # Updated function for streaming is assumed
from pathlib import Path
from img import get_base64_of_bin_file

# Set the page configuration (must be the first Streamlit command)
st.set_page_config( page_title="Pyramid Patron",page_icon="static/icon-egyptian-pyramids.png", layout="wide",initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .top-right-buttons {
        position: absolute;
        top: 0;
        right: 0;
        padding: 10px;
        z-index: 1001;  # Increased z-index
    }
    .top-right-buttons button {
        margin-left: 10px;
        padding: 5px 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        cursor: pointer;
    }
    .title {
        margin-top: 40px;  # Add top margin to push title down
    }
    </style>
    <div class="top-right-buttons">
        <button onclick="alert('Login clicked')">Login</button>
        <button onclick="alert('Sign up clicked')">Sign up</button>
    </div>
    """, unsafe_allow_html=True)
# Set up the image for background and sidebar
image_path = Path(__file__).parent / "static" / "pyramids.jpg"
encoded_image = get_base64_of_bin_file(image_path)

# Sidebar background
sidebar_bg_img = f"""
<style>
[data-testid="stSidebar"] {{
    background-image: url("data:image/png;base64,{encoded_image}");
    background-size: cover;
    background-position: center; 
    background-repeat: no-repeat;
}}
</style>
"""
st.markdown(sidebar_bg_img, unsafe_allow_html=True)

# Page background
page_bd_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{encoded_image}");
    background-size: cover;
    color: white;
}}
[data-testid="stAppViewContainer"] .block-container {{
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 10px;
    padding: 2rem;
}}
h1 {{
    color: gold;
    text-align: center;
}}
textarea, input, button {{
    font-size: 16px;
}}
</style>
"""
st.markdown(page_bd_img, unsafe_allow_html=True)

# Page title
st.markdown("<h1>Pyramid Patron</h1>", unsafe_allow_html=True)

# Sidebar for model selection and chat history
st.sidebar.title("Settings")
model = st.sidebar.selectbox("Choose a model:", ["llama3.2", "model2","model3"], key="model")

st.sidebar.title("Conversation History")
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history in the sidebar
for i, (user, bot) in enumerate(st.session_state.history):
    st.sidebar.markdown(f"**You:** {user}")
    st.sidebar.markdown(f"**Bot:** {bot}")

# Main interface
# Add custom CSS to change the label color
st.markdown("""
    <style>
    .stTextArea label {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

user_prompt = st.text_area(
    "Enter your prompt:",
    placeholder="How can I help you?",
    height=150
)

# Generate content button
if st.button("➤", key="send_button"):
    if user_prompt.strip():
        # Append user input to the history
        st.session_state.history.append((user_prompt, ""))

        # Placeholder for bot response
        response_placeholder = st.empty()

        # Stream the bot's response
        bot_response = ""
        for chunk in generate_content(user_prompt, model):
            bot_response += chunk + " "
            response_placeholder.markdown(f"**Bot:** {bot_response.strip()}")
        
        # Update history with the full bot response
        st.session_state.history[-1] = (user_prompt, bot_response.strip())
    else:
        st.warning("Please enter a prompt.")
# Download chat history button
if st.session_state.history:
    history_text = "\n".join(
        [f"You: {user}\nBot: {bot}" for user, bot in st.session_state.history]
    )
    st.download_button(
        label="💾 Download Conversation",
        data=history_text,
        file_name="conversation_history.txt",
        mime="text/plain"
    )
