import os
from dotenv import load_dotenv
import google.generativeai as genai
 
load_dotenv()
 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Loaded Gemini Key:", GEMINI_API_KEY[:10])
 
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)
 
 
def generate_answer(context, question):
 
    prompt = f"""
You are KnowledgeBot.

You must answer the user's question ONLY using the provided context from uploaded documents.

Strict Rules:

1. Use ONLY the information present in the context.
2. Do NOT use outside knowledge.
3. Do NOT assume, guess, or invent information.
4. If the context does not contain the answer, reply exactly:
I couldn't find this information in the uploaded documents.
5. If the question is unrelated to the context, reply exactly:
I couldn't find this information in the uploaded documents.
6. If the context only partially answers the question, answer only the part available in the context and clearly say that the remaining information was not found.
7. Be concise and professional.
8. Use bullet points whenever appropriate.
9. Preserve exact names, dates, numbers, headings, and technical terms from the context.
10. Do not mention that you are using outside knowledge.
11. Do not say "according to the provided context" or "based on the context".

Context:

{context}


Question:

{question}


Answer:
"""
 
    try:
 
        response = model.generate_content(
 
            prompt,
 
            generation_config={
 
                "temperature": 0.0,
 
                "top_p": 0.95,
 
                "top_k": 40,
 
                "max_output_tokens": 800
 
            }
 
        )
 
        if response.text:
 
            answer = response.text.strip()
 
            answer = answer.replace(
                "According to the provided context,",
                ""
            )
 
            answer = answer.replace(
                "According to the context,",
                ""
            )
 
            answer = answer.replace(
                "Based on the provided context,",
                ""
            )
 
            answer = answer.replace(
                "Based on the context,",
                ""
            )
 
            return answer.strip()
 
        return "I couldn't find this information in the uploaded documents."
 
    except Exception as e:

        print(e)

        return (
            "The AI service is temporarily unavailable. "
            "Please try again later."
    )