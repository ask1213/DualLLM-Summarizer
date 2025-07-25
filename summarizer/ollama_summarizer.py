from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

load_dotenv()

# Initialize Ollama LLM via LangChain
model = ChatOllama(model="llama3")  

# Prompt template
prompt = PromptTemplate(
    template="""You are a helpful assistant that summarizes text. Please summarize the following text:\n\n{text}\n\nSummary:""",
    input_variables=["text"]
)

# Chain
summarizer = prompt | model

# Final summarization function
def summarize_with_ollama(scraped_data: dict) -> str:
    title = scraped_data.get("title", "No Title")
    text = scraped_data.get("text", "")
    
    if not text.strip():
        return f"# {title}\nNo content to summarize."

    try:
        response = summarizer.invoke({"text": text})
        summary = response.content.strip()
    except Exception as e:
        summary = f"Error summarizing with Ollama: {str(e)}"

    return f"# {title}\n\nSummary:\n{summary}"

if __name__ == "__main__":
    from scraper.web_scraper import get_page_content

    url = "https://example.com/your-article-here"
    scraped_data = get_page_content(url)

    summary = summarize_with_ollama(scraped_data)
    print(summary)