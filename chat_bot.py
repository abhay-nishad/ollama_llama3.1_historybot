import sys
import json
import os
import subprocess

# Set default encoding to UTF-8 (for older Python versions)
if sys.version_info < (3, 7):
    reload(sys)
    sys.setdefaultencoding("utf-8")

# File name for saving chat history
file_name = "chat_history.json"

# Function to save conversation history
def save_history(chat_history):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, ensure_ascii=False, indent=4)

# Function to load conversation history
def load_history():
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return []

# Function to format the conversation history for input
def format_history_for_model(chat_history):
    formatted_history = ""
    for entry in chat_history:
        formatted_history += f"You: {entry['You']}\nModel: {entry['Model']}\n"
    return formatted_history

# Load previous chat history
chat_history = load_history()

print("Previous chat loaded:", chat_history)

while True:
    user_input = input("You: ")
    
    # Add user input to chat history (placeholder for the model response)
    chat_history.append({"You": user_input, "Model": ""})

    # Format the conversation history to include it in the model's context
    conversation_context = format_history_for_model(chat_history)
    conversation_context += f"You: {user_input}\n"

    # Run the model using Ollama with the entire conversation context
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1"],
            input=conversation_context,  # No need to encode
            text=True,
            capture_output=True,
            check=True,
            encoding="utf-8"
        )
        response = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        response = "Error: Unable to get a response from the model."

    # Update the latest model response in the chat history
    chat_history[-1]["Model"] = response

    # Print the model's response
    print("Model:", response)
    
    # Save chat history after each interaction
    save_history(chat_history)

    # Exit condition (optional)
    if user_input.lower() == "exit":
        print("Chat saved. Exiting.")
        break
