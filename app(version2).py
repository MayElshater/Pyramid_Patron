import streamlit as st
from model3 import generate_content  # Updated function for streaming is assumed
from pathlib import Path
import datetime

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
def save_conversation(history, new_chat=False):
    # Use the Conversation_History folder
    conversation_dir = history_folder

    # Generate file name based on timestamp if it's a new chat
    if new_chat or not list(conversation_dir.glob("*.txt")):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"chat_{timestamp}.txt"
    else:
        # Use the existing file if it's not a new chat
        existing_files = list(conversation_dir.glob("*.txt"))
        file_name = existing_files[-1].name if existing_files else f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    file_path = conversation_dir / file_name
    with open(file_path, "w") as f:
        for user, bot in history:
            f.write(f"You: {user}\n")
            f.write(f"Bot: {bot}\n\n")
    return file_path

def load_conversation(file_path):
    conversation = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):  # Assuming each entry is 2 lines + 1 empty line
            user = lines[i].strip().replace("You: ", "")
            bot = lines[i+1].strip().replace("Bot: ", "")
            conversation.append((user, bot))
    return conversation

# Add "New Chat" button
if st.sidebar.button("New Chat"):
    if st.session_state.history:  # Only save if there's a conversation to save
        save_conversation(st.session_state.history, new_chat=True)
    st.session_state.history = []  # Clear history
    st.session_state.input_text = ""  # Clear input box
    st.rerun()

# Display saved conversations
if st.sidebar.checkbox("Show saved conversations"):
    saved_files = list(history_folder.glob("*.txt"))
    if saved_files:
        for file in saved_files:
            if st.sidebar.button(f"Load: {file.name}"):
                st.session_state.history = load_conversation(file)
                st.rerun()
    else:
        st.sidebar.markdown("No saved conversations.")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""  # For managing the input box state

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# Main UI
st.markdown("<h1>Pyramid Patron</h1>", unsafe_allow_html=True)
model = st.sidebar.selectbox("Choose a model:", ["llama3.2", "model2", "model3"], key="model")

# Chat Interface
st.write("### Chat Interface")

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
            st.markdown(f"**Bot:** {chunk}")  # Display each line of response

        st.session_state.history[-1] = (user_input, bot_response.strip())  # Finalize response

        # Save the conversation after each interaction
        save_conversation(st.session_state.history)

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
