from langchain_ollama import ChatOllama

def get_response(user_input):
    llm = ChatOllama(model='gemma3:1b')

    prompt = f"""
    You are an AI Career Coach helping freshers.
    Give clear, practical, and professional advice.

    Question: {user_input}
    """

    response = llm.invoke(prompt)
    return response.content

# if __name__ == "__main__":
#     while True:
#         user_input = input("You: ")

#         if user_input.lower() == "exit":
#             print("Bot: Goodbye! 👋")
#             break

#         if not user_input.strip():
#             continue

#         result = get_response(user_input)
#         print("Bot:", result)


def analyze_resume(resume_text):
    llm = ChatOllama(model='gemma3:1b',temperature = 0.7)

    prompt = f"""
    You are an expert career coach and resume reviewer.

    Analyze the following resume and give:
    1. Strengths
    2. Weaknesses
    3. Missing skills
    4. Suggestions to improve

    Resume:
    {resume_text}
    """

    respose = llm.invoke(prompt)
    return respose.content