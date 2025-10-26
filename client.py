import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="paste your key here")  

# Use Gemini 2.0 model
model = genai.GenerativeModel("gemini-2.0-flash")

user_question = input("Ask Jarvis: ")
response = model.generate_content(
    f"You are Jarvis, a helpful assistant. User asked: {user_question}"
)
print("Jarvis:", response.text).
