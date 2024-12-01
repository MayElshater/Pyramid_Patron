
import streamlit as st
import subprocess
import time
import base64
from pathlib import Path


def generate_content(prompt, model):
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True
        )
        return result.stdout.strip() if result.stdout else None
    except Exception as e:
        return f"Error: {e}"
    


# Streamlit UI Updates
st.title("AI Content Generator")



def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set the path to your image
image_path = Path(__file__).parent / "static" / "pyramids.jpg"
encoded_image = get_base64_of_bin_file(image_path)
#st.subheader("Generate high-quality content using Ollama AI models.")
sidebar_bg_img = f"""
<style>
[data-testid="stSidebar"] {{
    background-image: url("data:image/png;base64,{encoded_image}");
    background-size: cover;
    background-position: center; 
    background-repeat: no-repeat;
}}

/* Styling all buttons */
button {{
    color: #000 !important; /* Black button text for visibility */
    background-color: #f0f0f0 !important; /* Light button background */
    border: 1px solid #ccc !important; /* Subtle border */
    border-radius: 5px !important;
    padding: 10px 20px !important;
    font-size: 18px !important; /* Ensure button text is legible */
}}

/* Button hover state */
button:hover {{
    background-color: #ddd !important; /* Slightly darker background on hover */
    color: #000 !important; /* Keep text black */
}}

/* Button active state */
button:active {{
    background-color: #bbb !important; /* Darker background when clicked */
    color: #000 !important; /* Keep text black */
}}

/* Ensure disabled buttons are styled properly */
button[disabled] {{
    background-color: #e0e0e0 !important;
    color: #888 !important;
    border: 1px solid #ccc !important;
}}
</style>
"""
st.markdown(sidebar_bg_img, unsafe_allow_html=True)

# Sidebar for model selection
model = st.sidebar.selectbox("Choose a model:", ["llama3.2", "another_model"])

# Input prompt area with a placeholder and larger size
st.markdown("""
<style>
    .stTextArea textarea {
        font-size: 20px !important;
    }
    .stTextArea label {
        font-size: 20px !important;
        color: #ffffff !important; /* Change this to your desired color */
    }
</style>
""", unsafe_allow_html=True)

user_prompt = st.text_area(
    "Enter your prompt:",
    placeholder="How Can I Help You",
    height=150
)

# Custom CSS for larger text and improved readability
page_bd_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{encoded_image}");
    background-size: cover;
    /*background-position: center;*/
    /*background-attachment: fixed;*/
    color: white;
    font-size: 22px;  /* Increase base font size */
    line-height: 1.6;  /* Improve text spacing */
}}
[data-testid="stAppViewContainer"] .block-container {{
    background-color: rgba(0, 0, 0, 0.7);  /* Semi-transparent overlay for readability */
    border-radius: 10px;
    padding: 2rem;
}}
h1, h2, h3, h4, h5, h6 {{
    color: #ffffff;  /* Ensure headings are white */
    font-size: 50px;  /* Larger headings */
}}
textarea, input, button {{
    font-size: 100px;  /* Larger input elements */
}}
</style>
"""



st.markdown(page_bd_img, unsafe_allow_html=True)

# Initialize session state if not already initialized

if 'output' not in st.session_state:
    st.session_state.output = None
if 'likes' not in st.session_state:
    st.session_state.likes = 0
if 'dislikes' not in st.session_state:
    st.session_state.dislikes = 0

# Function to simulate progressive output
def stream_output(content, font_size='30px', text_color='white', background_color='transparent'):
    placeholder = st.empty()
    for i in range(1, len(content) + 1):
        placeholder.markdown(
            f"""
            <p style='
                font-size: {font_size};
                color: {text_color};
                background-color: {background_color};
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            '>
                {content[:i]}
            </p>
            """,
            unsafe_allow_html=True
        )
        delay = max(0.01, min(0.05, 5 / len(content)))  # Adjust delay based on content length
        time.sleep(delay)
st.markdown("""
<style>
    .stSpinner > div > div {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


# Function to stream output progressively or redisplay stored content
def display_output(content, font_size='30px', text_color='white', background_color='transparent'):
    if content:
        st.markdown(
            f"""
            <p style='
                font-size: {font_size};
                color: {text_color};
                background-color: {background_color};
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            '>
                {content}
            </p>
            """,
            unsafe_allow_html=True
        )

# Generate Content Button
if st.button("Generate Content"):
    if user_prompt.strip():
        with st.spinner("Generating content..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            generated_content = generate_content(user_prompt, model)

            if generated_content:
                # Store the content in session state
               st.session_state.output = generated_content

                # Display the content
               #display_output(generated_content)  # Display once here

               st.success("Content generated successfully!")
            else:
                st.warning("Failed to generate content.")
    else:
        st.warning("Please enter a prompt.")

# Add a Clear button (reset session state)
if st.button("Clear"):
    # Reset content and like/dislike counts only
    st.session_state.output = None
    st.session_state.likes = 0
    st.session_state.dislikes = 0

# Like/Dislike Buttons under the generated content
if st.session_state.output:
    # Redisplay stored content only once
    display_output(st.session_state.output)  # Ensure no duplicate display

    # Like and Dislike buttons with counters
    like_button = st.button("👍 Like")
    dislike_button = st.button("👎 Dislike")

    if like_button:
        st.session_state.likes += 1
        st.success("Thank you for your feedback ☺️")
    
    if dislike_button:
        st.session_state.dislikes += 1
        st.error("We apologize as we are working to improve our responses 🙏🏻. Thank you for your feedback ❤️")

    # Display Like/Dislike counters
    st.write(
        f"<p style='font-size:30px; color:white;'>👍 Likes: {st.session_state.likes} | 👎 Dislikes: {st.session_state.dislikes}</p>",
        unsafe_allow_html=True
    )

    # Add download button after the response
    st.download_button(
        label="💾 Download",
        data=st.session_state.output,
        file_name="generated_content.txt",
        mime="text/plain"
    )
else:
    st.warning("No content to download yet.")
