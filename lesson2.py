# Exercise 1
#  import os
# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from google import genai



# load_dotenv()

# client=genai.Client(api_key=os.environ["Gemini_API_Key"])

# interaction = client.interactions.create(
#     model="gemini-3.6-flash",
#     system_instruction="You are a helpful coding assistant.",
#     input=("write a function to validate email"),
# # generation_config={"max_output_tokens":500}

# )

# answer=interaction.output_text

# print(answer)
# print("\n---")
# print(f"Interaction id: {interaction.id}")

# =================================================================================
# Exercise 2

# import os
# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from google import genai



# load_dotenv()

# client=genai.Client(api_key=os.environ["Gemini_API_Key"])

# interaction = client.interactions.create(
#     model="gemini-3.6-flash",
#     system_instruction="You are a helpful coding assistant.",
#     input="""
# Write a Python function `is_valid_email(email: str) -> bool`.

# Requirements:
# - Use the `re` module (no external dependencies)
# - Must reject strings with no '@' or no domain part
# - Do not attempt full RFC 5322 compliance — basic format checking is enough
# - Return False for None or empty string, do not raise an exception
# """,
# # generation_config={"max_output_tokens":500}

# )

# answer=interaction.output_text

# print(answer)
# print("\n---")
# print(f"Interaction id: {interaction.id}")

# ====================================================================================

# Exercise 3
# import os

# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# client = genai.Client(api_key=os.environ['Gemini_API_Key'])

# interaction=client.interactions.create(
#     model="gemini-3.6-flash",
#     system_instruction="You are a Helpfull HR assistence !",
#     input="""
#         Help me craft a resume!
        
#         Requirements
#         - Use a clean, modern template
# - Include sections: Contact, Summary, Experience, Education, Skills
# - Keep it under 500 words
# - Output only the Markdown text (no explanations, no chat)
#     """
# )
# answer=interaction.output_text
# print(answer)

# =======================================================================================
# Exercise 4

import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ['Gemini_API_Key'])

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    system_instruction="You are a helpful assistant.",
    input="""
Classify the sentiment of this review as exactly one word: positive, negative, or mixed.
Review: "The food was absolutely amazing and the service was quick."

Respond with ONLY the single word. No punctuation, no explanation.
"""
)
print(interaction.output_text)


    