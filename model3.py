import streamlit as st
import subprocess
import time

# Function to generate content with streaming support
def generate_content(prompt, model):
    try:
        process = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Send prompt to the model
        process.stdin.write(prompt + "\n")
        process.stdin.close()

        # Stream the response
        for line in iter(process.stdout.readline, ""):
            yield line.strip()  # Yield each line of output as it's generated

        process.stdout.close()
        process.wait()
    except Exception as e:
        yield f"Error: {e}"



