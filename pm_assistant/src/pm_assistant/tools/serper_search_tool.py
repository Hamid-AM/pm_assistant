#Standard imports
import os
import requests
from dotenv import load_dotenv

#Import CrewAI's `tool` decorator from the correct location
from crewai.tools import tool

#Load environment variables from the `.env` file
load_dotenv()

#Fetch the SERPER API key from the environment
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

#This is the function that actually runs the Serper (Google Search) query
def run_serper_search(query: str) -> str:
    """
    Queries Serper.dev API with a search term and returns the top 5 search results.

    Args:
        query (str): The user's search term (e.g., "AI trends 2025").

    Returns:
        str: A formatted string with titles, links, and snippets for each result.
    """
    # Define the API endpoint and headers including your API key
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,            # Auth header
        "Content-Type": "application/json"      # API expects JSON format
    }
    # Set the search query in the payload
    payload = {"q": query}

    # Make the HTTP POST request to Serper
    response = requests.post(url, headers=headers, json=payload)

    # Extract up to 5 results from the "organic" section
    items = response.json().get("organic", [])[:5]

    # Format the output nicely
    formatted_results = "\n\n".join(
        f"- {item['title']}: {item['link']}\n  {item['snippet']}"
        for item in items
    )

    return formatted_results or "No results found."

#This turns our function into a CrewAI-compatible tool that can be passed to Agents
SerperSearchTool = tool("SerperSearchTool")(run_serper_search)

