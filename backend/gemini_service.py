import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(context, question):

    prompt = f"""
You are KnowledgeBot.

Answer the user's question ONLY using the information provided in the context.

Rules:

1. Answer ONLY from the context.

2. If the answer is not available, reply exactly:

I couldn't find this information in the uploaded documents.

3. Never invent information.

4. Never use outside knowledge.

5. Be concise.

6. Use bullet points whenever appropriate.

7. Preserve:
- names
- dates
- numbers
- technical terms

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

        return "No answer generated."

    except Exception as e:

        print(e)

        return f"Gemini Error : {str(e)}"