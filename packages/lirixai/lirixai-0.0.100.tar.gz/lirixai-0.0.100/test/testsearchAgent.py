
from searchAgent import SearchAgentWrapper
import asyncio
import nest_asyncio


nest_asyncio.apply()




groq_api_key = "your api key"
tavily_api_key = "your api key"
search_agent_wrapper = SearchAgentWrapper(groq_api_key, tavily_api_key)

async def main():
    # Perform a search
    query = "what is the current price for the zephyrous g14 and tell me what the results are:"
    max_results = 5
    result_data = await search_agent_wrapper.do_search(query, max_results)

    # Extract and print the detailed text from the result
    if result_data and hasattr(result_data, 'data'):
        detailed_text = result_data.data.research_main
        print(detailed_text)
    else:
        print("No result data found.")

# Run the main function
asyncio.run(main())