
import streamlit as st
from model import generate_content, stream_output
import time
from img import get_base64_of_bin_file
from pathlib import Path


# Streamlit UI Updates
#st.markdown("<h1 style='text-align: center; color: gold;'>Pyramid Patron</h1>", unsafe_allow_html=True)




# Set the path to your image
image_path = Path(__file__).parent / "static" / "pyramids.jpg"
encoded_image = get_base64_of_bin_file(image_path)

# First, set the page config to remove default header
st.set_page_config(page_title="Pyramid Patron", page_icon="static\icon-egyptian-pyramids.png", layout="wide", initial_sidebar_state="collapsed")

# Then, add the custom CSS and buttons
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

# Now add the title
st.markdown("<h1 class='title' style='text-align: center; color: gold;'>Pyramid Patron</h1>", unsafe_allow_html=True)


#Sidebar Background
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
model = st.sidebar.selectbox("Choose a model:", ["llama3.2", "model1", "model2"])



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


# Page Background
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
if 'content_displayed' not in st.session_state:
    st.session_state.content_displayed = False

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
               st.session_state.content_displayed = False  # Reset flag for streaming

                
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
    st.session_state.content_displayed = False  # Reset the display flag

# Display generated content
if st.session_state.output and not st.session_state.content_displayed:
    stream_output(st.session_state.output)  # Stream content only if not already displayed
    st.session_state.content_displayed = True  # Set the flag to indicate content has been streamed

# Like/Dislike Buttons under the generated content
if st.session_state.output:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Like"):
            st.session_state.likes += 1
            st.success("Thank you for your feedback ☺️")
    
    with col2:
        if st.button("👎 Dislike"):
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
