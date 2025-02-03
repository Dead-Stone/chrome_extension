import summarization
from chat import generate_chat_response

class SummarizationAgent:
    def summarize(self, bookmark_data):
        """
        Uses the summarization module to summarize the webpage at bookmark_data['url'].
        """
        # Call your existing summarization function.
        summary = summarization.summarize(bookmark_data.get("url"))
        bookmark_data["summary"] = summary
        return bookmark_data

class ConversationAgent:
    def converse(self, bookmark_data, query):
        """
        Uses the chat module to generate a conversational response.
        """
        # Call your existing chat module function.
        response = generate_chat_response(bookmark_data, query)
        return response

class ManagerAgent:
    def __init__(self, db):
        self.db = db
        self.summarizer = SummarizationAgent()
        self.converser = ConversationAgent()

    def handle_summarization(self, bookmark_data, user_email):
        """
        Summarize a bookmark, store it in the database, and (optionally) create a relationship between
        the user and the bookmark.
        """
        # Generate summary using the summarization agent.
        updated_data = self.summarizer.summarize(bookmark_data)
        # Save the bookmark in the database.
        bookmark = self.db.create_bookmark(
            updated_data.get("id"),
            updated_data.get("title"),
            updated_data.get("url"),
            updated_data.get("summary")
        )
        # Ensure the user node exists.
        self.db.create_user(user_email)
        # (Optional) You could create a relationship here (e.g. SAVED) if desired.
        return bookmark

    def handle_chat(self, bookmark_id, query):
        """
        Retrieve the bookmark by its ID and generate a chat response using the conversation agent.
        """
        bookmark = self.db.get_bookmark_by_id(bookmark_id)
        if not bookmark:
            raise Exception("Bookmark not found")
        response = self.converser.converse(bookmark, query)
        return response

    def handle_feedback(self, bookmark_id, user_email, feedback):
        """
        Create a relationship between the user node and bookmark node based on the feedback.
        """
        return self.db.add_feedback(user_email, bookmark_id, feedback)
