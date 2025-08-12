from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_google_genai import ChatGoogleGenerativeAI 
import os
from langchain_core.documents import Document
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import logging 
from pyvis.network import Network

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def generate_knowledge_graph(text:str=""):
    '''
    Generate a knowledge graph from the given text using the given API key.

    Args:
        text (str): The text to generate a knowledge graph from.

    Returns:
        graph_documents: The generated knowledge graph.
    '''
    llm = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.5-pro")
    logger.info("llm set to gemini-2.5-pro")
    llm_transformer = LLMGraphTransformer(llm=llm)
    logger.info("LLMGraphTransformer created")
    documents = [Document(page_content=text)]
    logger.info("documents created")
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    logger.info(f"graph_documents created: {graph_documents}")
    return graph_documents



def extract_text_from_url(url:str="") -> str:
    '''
    Extract text from the given URL using the given API key.

    Args:
        url (str): The URL to extract text from.

    Returns:
        text: The extracted text.
    '''
    logger.info(f"extracting text from {url}")
    response = requests.get(url)
    response.raise_for_status()
    logger.info("response received")
    soup = BeautifulSoup(response.text, 'html.parser')
    logger.info("extracting text from html")
    text = soup.get_text()
    logger.info(f"text extracted: {text}")
    return text


def visualize_knowledge_graph(nodes, relationships, output_file="knowledge_graph.html"):
    
    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", directed=True)

    # Add nodes
    for node in nodes:
        net.add_node(
            node.id,
            label=node.id,
            title=f"Type: {node.type}<br>Properties: {node.properties}",
            group=node.type
        )

    # Add relationships
    for rel in relationships:
        net.add_edge(
            rel.source.id,
            rel.target.id,
            label=rel.type,
            title=f"Properties: {rel.properties}"
        )

    net.toggle_physics(True)
    net.show_buttons(filter_=['physics'])

    # Save HTML without opening browser (avoids Jinja2 render bug)
    net.write_html(output_file)
    logger.info(f"Knowledge graph saved to {output_file}")


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Hypericum_androsaemum"
    text = extract_text_from_url(url)
    graph_documents = generate_knowledge_graph(text)
    visualize_knowledge_graph(graph_documents[0].nodes, graph_documents[0].relationships)








