import streamlit as st
from model3 import generate_content  # Updated function for streaming is assumed
from pathlib import Path

# Set the page configuration
st.set_page_config(
    page_title="Pyramid Patron",
    page_icon="static/icon-egyptian-pyramids.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)
def clear_text():
    st.session_state.input_text = True
    
# Check and create "Conversation History" folder
history_folder = Path("Conversation_History")
history_folder.mkdir(exist_ok=True)

# Function to save conversation
def save_conversation(history):
    conversation_dir = Path("conversation_history")
    conversation_dir.mkdir(parents=True, exist_ok=True)

    # Generate file name based on the first few words of the first user input
    if history:
        first_words = history[0][0][:10].replace(" ", "_").replace("/", "_")
        file_name = f"{first_words}.txt"
    else:
        file_name = "new_chat.txt"

    file_path = conversation_dir / file_name
    with open(file_path, "w") as f:
        for user, bot in history:
            f.write(f"You: {user}\n")
            f.write(f"Bot: {bot}\n\n")
    return file_path

# Add "New Chat" button
if st.sidebar.button("New Chat"):
    save_conversation(st.session_state.history)
    st.session_state.history = []  # Clear history
    st.session_state.input_text = ""  # Clear input box

# Display saved conversations
if st.sidebar.checkbox("Show saved conversations"):
    saved_files = list(history_folder.glob("*.txt"))
    if saved_files:
        for file in saved_files:
            st.sidebar.markdown(f"- {file.name}")
    else:
        st.sidebar.markdown("No saved conversations.")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""  # For managing the input box state

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Add this line to initialize input_key
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# Main UI
st.markdown("<h1>Pyramid Patron</h1>", unsafe_allow_html=True)
model = st.sidebar.selectbox("Choose a model:", ["llama3.2", "model2", "model3"], key="model")

# Chat Interface
st.write("### Chat Interface")

# Capture user input with a text input widget
# Capture user input with a text input widget
# Capture user input with a text input widget
user_input = st.text_input(
    "Enter your prompt:",
    placeholder="How can I help you?",
    key=f"input_text_{st.session_state.input_key}"
)

# Handle send button logic
if st.button("Send ➤"):
    if user_input and user_input.strip():  # Check if input is not empty and not just whitespace
        # Add user message to history
        st.session_state.history.append((user_input, ""))
        bot_response = ""

        # Generate bot response and update history dynamically
        for chunk in generate_content(user_input, model):
            bot_response += chunk + " "

        st.session_state.history[-1] = (user_input, bot_response.strip())  # Finalize response

        # Increment the input key to create a new input field (clearing the old one)
        st.session_state.input_key += 1
        st.rerun()
    else:
        st.warning("Please enter a prompt.")

# Display the conversation history
st.write("### Conversation")
for user, bot in st.session_state.history:
    st.markdown(f"**You:** {user}")
    st.markdown(f"**Bot:** {bot}")