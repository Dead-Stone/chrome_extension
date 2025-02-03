from fastapi import APIRouter, HTTPException
from backend.models import get_db, add_user, get_user, update_user, delete_user, \
                            add_paper, get_paper, update_paper, delete_paper, \
                            add_interaction, get_interaction, update_interaction, delete_interaction, \
                            create_schema, parse_arxiv_response,fetch_arxiv_papers
from backend.schemas import User, Paper, Interaction
import xml.etree.ElementTree as ET

router = APIRouter()

# User CRUD endpoints
@router.post("/users")
def create_user(user: User):
    graph = get_db()
    add_user(graph, user.user_id)
    return {"status": "User created successfully", "user_id": user.user_id}

@router.get("/users/{user_id}")
def read_user(user_id: str):
    graph = get_db()
    user = get_user(graph, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}")
def update_user_endpoint(user_id: str, new_user_id: str):
    graph = get_db()
    update_user(graph, user_id, new_user_id)
    return {"status": "User updated successfully", "user_id": new_user_id}

@router.delete("/users/{user_id}")
def delete_user_endpoint(user_id: str):
    graph = get_db()
    delete_user(graph, user_id)
    return {"status": "User deleted successfully"}

# Paper CRUD endpoints
@router.post("/papers")
def create_paper(paper: Paper):
    graph = get_db()
    add_paper(graph, paper.paper_id, paper.title, paper.abstract, paper.link)
    return {"status": "Paper created successfully", "paper_id": paper.paper_id}

@router.get("/papers/{paper_id}")
def read_paper(paper_id: str):
    graph = get_db()
    paper = get_paper(graph, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@router.put("/papers/{paper_id}")
def update_paper_endpoint(paper_id: str, paper: Paper):
    graph = get_db()
    update_paper(graph, paper_id, paper.title, paper.abstract, paper.link)
    return {"status": "Paper updated successfully", "paper_id": paper_id}

@router.delete("/papers/{paper_id}")
def delete_paper_endpoint(paper_id: str):
    graph = get_db()
    delete_paper(graph, paper_id)
    return {"status": "Paper deleted successfully"}

# Interaction CRUD endpoints
@router.post("/interactions")
def create_interaction(interaction: Interaction):
    graph = get_db()
    add_interaction(graph, interaction.user_id, interaction.paper_id, interaction.interaction_type)
    return {"status": "Interaction created successfully", "user_id": interaction.user_id, "paper_id": interaction.paper_id}

@router.get("/interactions")
def read_interaction(user_id: str, paper_id: str):
    graph = get_db()
    interaction = get_interaction(graph, user_id, paper_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction

@router.put("/interactions")
def update_interaction_endpoint(interaction: Interaction):
    graph = get_db()
    update_interaction(graph, interaction.user_id, interaction.paper_id, interaction.interaction_type)
    return {"status": "Interaction updated successfully", "user_id": interaction.user_id, "paper_id": interaction.paper_id}

@router.delete("/interactions")
def delete_interaction_endpoint(user_id: str, paper_id: str):
    graph = get_db()
    delete_interaction(graph, user_id, paper_id)
    return {"status": "Interaction deleted successfully"}

# Schema creation endpoint
@router.post("/create-schema")
def create_schema_route():
    graph = get_db()
    create_schema(graph)
    return {"status": "Schema created successfully"}


router = APIRouter()

# Fetch and parse Arxiv papers
@router.get("/arxiv-papers")
def get_arxiv_papers(search_query: str = "machine learning", max_results: int = 5):
    xml_response = fetch_arxiv_papers(search_query, max_results)
    if not xml_response:
        raise HTTPException(status_code=404, detail="No papers found")
    
    # Parse the XML response
    papers = parse_arxiv_response(xml_response)
    return {"papers": papers}

