import streamlit as st
import json

def format_search_result(results):
    """
    Format search results into a markdown string.

    Args:
        results (str): JSON string containing search results

    Returns:
        str: Formatted markdown string with search results
    """
    results = json.loads(results)
    answer = ""
    for result in results:
        answer += f'**[{result["title"]}]({result["url"]})**\n\n'
        answer += f'{result["content"]}\n\n'
        answer += f'신뢰도: {result["score"]}\n\n'
        answer += "\n-----\n"
    return answer