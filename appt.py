import streamlit as st

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
        #delay = max(0.01, min(0.05, 5 / len(content)))  # Adjust delay based on content length
        #time.sleep(delay)


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