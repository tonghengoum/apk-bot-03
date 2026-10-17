import wikipedia
import requests
from typing import Optional

class ResearchEngine:
    def __init__(self, language: str = "en"):
        wikipedia.set_lang(language)

    def search_wikipedia(self, query: str) -> Optional[str]:
        """
        Search Wikipedia for a query and return the summary of the first result.
        Returns None if not found or an error occurs.
        """
        try:
            # Search for pages related to the query
            search_results = wikipedia.search(query)
            if not search_results:
                return None

            # Get the first result
            page_title = search_results[0]
            page = wikipedia.page(page_title)
            return page.summary
        except wikipedia.exceptions.DisambiguationError as e:
            # If there's a disambiguation error, try the first option
            try:
                page = wikipedia.page(e.options[0])
                return page.summary
            except Exception:
                return None
        except Exception:
            return None

    def research(self, query: str) -> str:
        """
        Research a query and return a formatted string with the results.
        Currently uses Wikipedia as the source.
        """
        summary = self.search_wikipedia(query)
        if summary:
            return f"According to Wikipedia:\n\n{summary}"
        else:
            # Fallback: try to use a simple request to a search API?
            # For now, return a placeholder.
            return f"I couldn't find detailed information about '{query}' on Wikipedia. " \
                   "Try rephrasing your question or be more specific."

# Example usage (for testing purposes)
if __name__ == "__main__":
    engine = ResearchEngine()
    result = engine.research("Artificial intelligence")
    print(result)