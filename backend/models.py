from fastapi import requests
from py2neo import Graph
from backend.config import Config
import xml.etree.ElementTree as ET
import requests  # Correct import for making HTTP requests

def get_db():
    graph = Graph(Config.NEO4J_URI, auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD))
    return graph

# Schema management
def create_schema(graph):
    graph.run("CREATE CONSTRAINT FOR (u:User) REQUIRE u.user_id IS UNIQUE;")
    graph.run("CREATE CONSTRAINT FOR (p:Paper) REQUIRE p.paper_id IS UNIQUE;")

# User CRUD operations
def add_user(graph, user_id):
    # Add the user node
    graph.run("MERGE (u:User {user_id: $user_id})", user_id=user_id)
    
    # Retrieve and return the user's details
    result = graph.run("MATCH (u:User {user_id: $user_id}) RETURN u.user_id AS user_id", user_id=user_id).data()
    
    # Return the result
    if result:
        return result[0]  # Since we're only expecting one user node with that user_id
    else:
        return None


def get_user(graph, user_id):
    return graph.run("MATCH (u:User {user_id: $user_id}) RETURN u", user_id=user_id).data()

def update_user(graph, user_id, new_user_id):
    graph.run("MATCH (u:User {user_id: $user_id}) SET u.user_id = $new_user_id", user_id=user_id, new_user_id=new_user_id)

def delete_user(graph, user_id):
    graph.run("MATCH (u:User {user_id: $user_id}) DETACH DELETE u", user_id=user_id)

# Paper CRUD operations
def add_paper(graph, paper_id, title, abstract, link):
    graph.run("""
    MERGE (p:Paper {paper_id: $paper_id})
    SET p.title = $title, p.abstract = $abstract, p.link = $link
    """, paper_id=paper_id, title=title, abstract=abstract, link=link)

def get_paper(graph, paper_id):
    return graph.run("MATCH (p:Paper {paper_id: $paper_id}) RETURN p", paper_id=paper_id).data()

def update_paper(graph, paper_id, title, abstract, link):
    graph.run("""
    MATCH (p:Paper {paper_id: $paper_id})
    SET p.title = $title, p.abstract = $abstract, p.link = $link
    """, paper_id=paper_id, title=title, abstract=abstract, link=link)

def delete_paper(graph, paper_id):
    graph.run("MATCH (p:Paper {paper_id: $paper_id}) DETACH DELETE p", paper_id=paper_id)

# Interaction CRUD operations
def add_interaction(graph, user_id, paper_id, interaction_type):
    graph.run("""
    MATCH (u:User {user_id: $user_id}), (p:Paper {paper_id: $paper_id})
    MERGE (u)-[r:INTERACTED {type: $interaction_type}]->(p)
    """, user_id=user_id, paper_id=paper_id, interaction_type=interaction_type)

def get_interaction(graph, user_id, paper_id):
    return graph.run("""
    MATCH (u:User {user_id: $user_id})-[r:INTERACTED]->(p:Paper {paper_id: $paper_id})
    RETURN r
    """, user_id=user_id, paper_id=paper_id).data()

def update_interaction(graph, user_id, paper_id, interaction_type):
    graph.run("""
    MATCH (u:User {user_id: $user_id})-[r:INTERACTED]->(p:Paper {paper_id: $paper_id})
    SET r.type = $interaction_type
    """, user_id=user_id, paper_id=paper_id, interaction_type=interaction_type)

def delete_interaction(graph, user_id, paper_id):
    graph.run("""
    MATCH (u:User {user_id: $user_id})-[r:INTERACTED]->(p:Paper {paper_id: $paper_id})
    DELETE r
    """, user_id=user_id, paper_id=paper_id)


def fetch_arxiv_papers(search_query="machine learning", max_results=5):
    url = f'http://export.arxiv.org/api/query?search_query=all:{search_query}&start=0&max_results={max_results}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # return the raw XML response from Arxiv
    else:
        return None

def parse_arxiv_response(xml_response):
    # Parse the XML response
    root = ET.fromstring(xml_response)
    papers = []
    
    # Iterate through each entry (paper)
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        paper = {}
        paper['id'] = entry.find('{http://www.w3.org/2005/Atom}id').text
        paper['title'] = entry.find('{http://www.w3.org/2005/Atom}title').text
        paper['summary'] = entry.find('{http://www.w3.org/2005/Atom}summary').text
        
        authors = []
        for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
            authors.append(author.find('{http://www.w3.org/2005/Atom}name').text)
        paper['authors'] = authors
        
        # Find the PDF link
        pdf_link = entry.find("{http://www.w3.org/2005/Atom}link[@title='pdf']")
        if pdf_link is not None:
            paper['pdf_link'] = pdf_link.attrib['href']
        
        papers.append(paper)
    
    return papers

