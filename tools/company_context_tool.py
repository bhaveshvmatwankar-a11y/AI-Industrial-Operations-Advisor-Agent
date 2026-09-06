from langchain.tools import tool

# Stores the currently active company name
ACTIVE_COMPANY_NAME = "Demo Factory"


def set_active_company_name(company_name: str):
    """
    Set the currently active company name.
    """
    global ACTIVE_COMPANY_NAME

    if company_name and company_name.strip():
        ACTIVE_COMPANY_NAME = company_name.strip()


def get_company_name() -> str:
    """
    Return the currently active company name.
    """
    return ACTIVE_COMPANY_NAME


@tool
def get_active_company_name() -> str:
    """
    Return the name of the company whose factory data
    is currently being analyzed.
    """
    return f"Active Company: {ACTIVE_COMPANY_NAME}"