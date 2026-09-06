from langchain.tools import tool
from tools.company_context_tool import get_company_name


@tool
def get_current_company_name() -> str:
    """
    Return the name of the company whose factory data
    is currently loaded in the application.
    """

    company_name = get_company_name()

    if not company_name:
        return "No company name has been provided."

    return f"Current Company: {company_name}"