import streamlit as st
import subprocess

def generate_content(prompt, model):
    """
    Sends a prompt to the Ollama model and retrieves the AI-generated content.
    """
    try:
        # Run the Ollama model
        result = subprocess.run(
            ["ollama", "run", model], 
            input=prompt, 
            text=True, 
            capture_output=True
        )
        
        # Debugging: Print the result to check the model's output
        if result.stdout:
            print(f"Model output: {result.stdout}")  # This prints to the console where you run Streamlit
        else:
            print(f"Model error: {result.stderr}")  # Print any errors if no output is returned
        
        # Return the output, stripping any extra spaces
        return result.stdout.strip() if result.stdout else None
    
    except Exception as e:
        print(f"Error: {e}")  # Print any exceptions in the console
        return f"Error: {e}"

# Streamlit App
st.title("AI Content Generator")
st.write("Generate high-quality content using AI models.")

# Input from the user
user_prompt = st.text_area("Enter your prompt:", placeholder="Write a short introduction about artificial intelligence.")
model = st.selectbox("Choose a model:", ["llama3.2", "another_model"])

# Initialize output variable within the button scope
output = None

# Generate Content Button
if st.button("Generate Content"):
    if user_prompt.strip():
        with st.spinner("Generating content..."):
            output = generate_content(user_prompt, model)
            
        # Check if output is generated and show it
        if output:
            st.subheader("Generated Content:")
            st.write(output)
        else:
            st.warning("Failed to generate content.")
    else:
        st.warning("Please enter a prompt.")

# Only show the download button if output is generated
if output:
    st.download_button(
        label="Download",
        data=output,
        file_name="generated_content.txt",
        mime="text/plain"
    )

# If no content is generated, show the warning.
elif st.button("Download Content"):
    st.warning("No content to download yet.")
