from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re
import os
from google import genai
from dotenv import load_dotenv

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Table Format:** All data extracted must always be presented in a table format."
)
# model = OllamaLLM(model="llama3.1")
# def parse_with_deepseek(dom_chunks, parse_description):
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model
#     parsed_results = []
#     for i, chunk in enumerate(dom_chunks, start=1):
#         response = chain.invoke(
#             {"dom_content": chunk, "parse_description": parse_description}
#         )
#         print(f"Parsed batch: {i} of {len(dom_chunks)}")
#         parsed_results.append(response)
#     return "\n".join(parsed_results)

# client = genai.Client(api_key="YOUR_API_KEY")
# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="Explain how AI works"
# )
# print(response.text)

def configure():
    load_dotenv()

def parse_with_gemini(dom_chunks, parse_description):
    configure()
    #client = genai.Client(api_key="AIzaSyBK2_gt_xEX7k_NiVXhJwpN77YmQaq6l2E")
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    chat = client.chats.create(model="gemini-2.0-flash")

    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chat.send_message_stream(f"From the following content, {parse_description}\n\nContent:\n{chunk}")
        result = ""
        for chunk in response:
            result += chunk.text
        parsed_results.append(result)
        print(f"Parsed batch: {i} of {len(dom_chunks)}")

    for message in chat._curated_history:
        print(f'role - {message.role}', end=": ")
        print(message.parts[0].text)

    return "\n".join(parsed_results)