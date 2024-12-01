
import subprocess
import time
import streamlit as st

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
    



# Streaming function for displaying text
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