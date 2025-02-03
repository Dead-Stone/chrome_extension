import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_really_secret_key'

    # Neo4j connection settings
    NEO4J_URI="neo4j+s://99bda7e5.databases.neo4j.io"
    NEO4J_USERNAME="neo4j"
    NEO4J_PASSWORD="AhX2duMe221J-4Hh-wzsjqGXTQeVVGq7jMgHu_jcMyA"
