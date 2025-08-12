import streamlit as st
import os
import json
import tempfile
from main import generate_knowledge_graph, extract_text_from_url, visualize_knowledge_graph
from dotenv import load_dotenv
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Page config
st.set_page_config(page_title="Knowledge Graph Generator", layout="wide")

# Hide streamlit style and make full screen
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}

/* Make main content area full height */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: none;
}

/* Make the iframe component full size */
.stHtml {
    height: calc(100vh - 2rem) !important;
}

.stHtml > div {
    height: 100% !important;
}

.stHtml iframe {
    height: 100% !important;
    width: 100% !important;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar: Input controls
st.sidebar.header("📥 Input Options")
input_type = st.sidebar.radio("Select Input Type", ("Insert Text", "Insert URL"))

if input_type == "Insert Text":
    text_data = st.sidebar.text_area("Enter your text:", height=150)
else:
    url_input = st.sidebar.text_input("Enter a public webpage URL:")

generate_button = st.sidebar.button("Generate Knowledge Graph", use_container_width=True)

# Main content: Visualization
if generate_button:
    if input_type == "Insert URL":
        if not url_input.strip():
            st.sidebar.warning("⚠️ Please provide a valid URL.")
            st.stop()
        text_data = extract_text_from_url(url_input)
        st.sidebar.success("✅ Text extracted from URL!")
    else:
        if not text_data.strip():
            st.sidebar.warning("⚠️ Please provide input text.")
            st.stop()

    with st.spinner("Processing..."):
        # Step 1: Generate knowledge graph
        graph_documents = generate_knowledge_graph(text_data)
        st.sidebar.success("✅ Knowledge graph generated!")

        try:
            # Parse JSON if needed
            if isinstance(graph_documents, str):
                graph_data = json.loads(graph_documents)
            elif isinstance(graph_documents, list) and isinstance(graph_documents[0], str):
                graph_data = json.loads(graph_documents[0])
            else:
                graph_data = graph_documents

            # Assuming graph_data[0] has .nodes and .relationships
            nodes = graph_data[0].nodes
            relationships = graph_data[0].relationships
            st.sidebar.success("✅ Nodes and relationships extracted")

            # Step 2: Visualize knowledge graph
            temp_html = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
            visualize_knowledge_graph(nodes, relationships, temp_html.name)

            with open(temp_html.name, "r", encoding="utf-8") as f:
                graph_html = f.read()
            
            st.sidebar.success("✅ Knowledge graph visualized!")

            # Display the graph in full screen - takes entire main panel
            components.html(
                graph_html, 
                height=800,  # Keep a large height
                scrolling=False
            )
                 
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.title("🕸️ Knowledge Graph Generator")
    st.write("Select input type and provide content to generate an interactive knowledge graph.")
    st.write("👈 Use the sidebar to get started.")