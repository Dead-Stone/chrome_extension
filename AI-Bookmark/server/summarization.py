import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_GENERATIVEAI_API_KEY", "YOUR_API_KEY"))

def fetch_and_extract(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        raise Exception(f"Error fetching URL: {str(e)}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    extracted_text = "\n".join(lines)
    return extracted_text

def summarize(url):
    extracted_text = fetch_and_extract(url)
    if not extracted_text or len(extracted_text) < 100:
        raise Exception("Not enough text found to summarize.")
    
    prompt = (
        "Please summarize the following text in 250 words or less. Return only the plain text summary without any additional formatting:\n\n" 
        + extracted_text
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=2096,
                temperature=0.2
            )
        )
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")

    summary = response.text
    if not summary:
        raise Exception("Google Generative AI did not return a summary.")
    return summary.strip()
