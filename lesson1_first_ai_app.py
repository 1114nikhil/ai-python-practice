# for Anthropic

# import os
# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from anthropic import Anthropic



# load_dotenv()

# client=Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# response= client.messages.create(
#     model="claude-sonnet-5",
#     max_tokens=300,
#     system="""
#             You are a senior Java/Spring boot Engineer, Explain error to Colleague
#     """,
#     messages=[
#         {
#             "role":"user", 
#             "content":"Explain this error in Plain English and suggest a fix:\n\n"
#                     "org.springframework.beans.factory.BeanCurrentlyInCreationException: "
#                 "Error creating bean with name 'orderService': "
#                 "Requested bean is currently in creation: Is there an unresolvable circular reference?"
#         }
#     ]
# )

# answer=response.content[0].text

# print(answer)

# for Gemini
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from google import genai
from google.genai import types



load_dotenv()

client=genai.Client(api_key=os.environ["Gemini_API_Key"])

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    system_instruction="""
            You are a senior Java/Spring boot Engineer, Explain error to Colleague
        """,
    input=("Explain this error in Plain English and suggest a fix:\n\n"
                    "org.springframework.beans.factory.BeanCurrentlyInCreationException: "
                "Error creating bean with name 'orderService': "
                "Requested bean is currently in creation: Is there an unresolvable circular reference?"),
    # generation_config={"max_output_tokens":500}

)

answer=interaction.output_text

print(answer)
print("\n---")
print(f"Interaction id: {interaction.id}")