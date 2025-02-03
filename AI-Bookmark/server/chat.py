import os
import google.generativeai as genai

def generate_chat_response(bookmark, query):
    prompt = (
        f"Based on the bookmark titled '{bookmark.get('title', 'Unknown')}', "
        f"with summary: '{bookmark.get('summary', '')}', answer the following query:\n\n{query}\n\n"
        "Provide a detailed and informative response. If the answer is not fully contained in the bookmark, "
        "include relevant context from your general knowledge and state that the answer is based on your knowledge."
    )
    
    genai.configure(api_key=os.environ.get("GOOGLE_GENERATIVEAI_API_KEY", "YOUR_API_KEY"))
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=1024,
            temperature=0.2,
        )
    )
    
    if not response or not response.text:
        raise Exception("No response from Gemini API")
    
    return response.text.strip()
