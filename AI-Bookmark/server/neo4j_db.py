from neo4j import GraphDatabase

class Neo4jDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def create_user(self, user_id):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_user_tx, user_id)
            return result
    
    @staticmethod
    def _create_user_tx(tx, user_id):
        query = """
        MERGE (u:User {id: $user_id})
        RETURN u { .id } AS user
        """
        result = tx.run(query, user_id=user_id)
        record = result.single()
        return record["user"] if record else None
    
    def create_bookmark(self, bookmark_id, title, url, summary):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_bookmark_tx, bookmark_id, title, url, summary)
            return result
    
    # @staticmethod
    # def _create_bookmark_tx(tx, bookmark_id, title, url, summary):
    #     query = """
    #     MERGE (b:Bookmark {id: $bookmark_id})
    #     ON CREATE SET b.title = $title, b.url = $url, b.summary = $summary
    #     RETURN b { .id, .title, .url, .summary } AS bookmark
    #     """
    #     result = tx.run(query, bookmark_id=bookmark_id, title=title, url=url, summary=summary)
    #     record = result.single()
    #     return record["bookmark"] if record else None
    @staticmethod
    def _create_bookmark_tx(tx, bookmark_id, title, url, summary):
        query = """
        MERGE (b:Bookmark {id: $bookmark_id})
        ON CREATE SET b.title = $title, b.url = $url, b.summary = $summary
        RETURN b { .id, .title, .url, .summary, link: b.url } AS bookmark
        """
        result = tx.run(query, bookmark_id=bookmark_id, title=title, url=url, summary=summary)
        record = result.single()
        return record["bookmark"] if record else None

    def add_feedback(self, user_id, bookmark_id, feedback):
        rel_type = "LIKED" if feedback == "like" else "DISLIKED"
        with self.driver.session() as session:
            result = session.write_transaction(self._add_feedback_tx, user_id, bookmark_id, rel_type)
            return result

    @staticmethod
    def _add_feedback_tx(tx, user_id, bookmark_id, rel_type):
        query = f"""
        MATCH (u:User {{id: $user_id}}), (b:Bookmark {{id: $bookmark_id}})
        MERGE (u)-[r:{rel_type}]->(b)
        RETURN type(r) AS feedback
        """
        result = tx.run(query, user_id=user_id, bookmark_id=bookmark_id)
        record = result.single()
        return record["feedback"] if record else None
    
    def get_random_bookmarks(self, count=10):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_random_bookmarks_tx, count)
            return result

    # @staticmethod
    # def _get_random_bookmarks_tx(tx, count):
    #     query = """
    #     MATCH (b:Bookmark)
    #     WITH b, rand() AS random
    #     RETURN b { .id, .title, .url, .summary } AS bookmark
    #     ORDER BY random
    #     LIMIT $count
    #     """
    #     result = tx.run(query, count=count)
    #     return [record["bookmark"] for record in result]
    @staticmethod
    def _get_random_bookmarks_tx(tx, count):
        query = """
        MATCH (b:Bookmark)
        WITH b, rand() AS random
        RETURN b { .id, .title, .url, .summary, link: b.url } AS bookmark
        ORDER BY random
        LIMIT $count
        """
        result = tx.run(query, count=count)
        return [record["bookmark"] for record in result]

    def get_bookmark_by_id(self, bookmark_id):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_bookmark_by_id_tx, bookmark_id)
            return result

    @staticmethod
    def _get_bookmark_by_id_tx(tx, bookmark_id):
        query = """
        MATCH (b:Bookmark {id: $bookmark_id})
        RETURN b { .id, .title, .url, .summary } AS bookmark
        """
        result = tx.run(query, bookmark_id=bookmark_id)
        record = result.single()
        return record["bookmark"] if record else None
