import subprocess

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

        response = ""
        # Stream the response
        for line in iter(process.stdout.readline, ""):
            line = line.strip()  # Clean up each line
            if line:  # Only add non-empty lines
                response += line + " "
                yield line  # Yield each chunk immediately

        process.stdout.close()
        process.wait()

        # Finalize the response after streaming
        if response.strip():
            yield response.strip()
        else:
            yield "No content generated."

    except Exception as e:
        yield f"Error: {e}"
