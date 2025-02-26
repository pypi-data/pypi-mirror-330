import os
from typing import Dict, List, Optional, Any
import aiohttp
from pydantic import BaseModel
from dhisana.utils.apollo_tools import enrich_person_info_from_apollo
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.proxy_curl_tools import enrich_person_info_from_proxycurl

# --------------------------------------------------------------------------------
# 1. Data Model
# --------------------------------------------------------------------------------

class LeadLinkedInMatch(BaseModel):
    first_name_matched: bool = False
    last_name_matched: bool = False
    linkedin_url_valid: bool = False
    title_matched: bool = False
    location_matched: bool = False

# --------------------------------------------------------------------------------
# 2. Helper: Compare Single Field
# --------------------------------------------------------------------------------

def compare_field(
    lead_properties: Dict[str, Any],
    person_data: Dict[str, Any],
    lead_key: str,
    person_key: str
) -> bool:
    if not lead_properties.get(lead_key):
        return True

    lead_value = lead_properties.get(lead_key, "")
    person_value = person_data.get(person_key, "")

    if isinstance(lead_value, str) and isinstance(person_value, str):
        return lead_value.strip().lower() == person_value.strip().lower()

    return person_value == lead_value

# --------------------------------------------------------------------------------
# 3. Apollo Validation Function
# --------------------------------------------------------------------------------

@assistant_tool
async def validate_linkedin_url_with_apollo(
    lead_properties: Dict[str, Any],
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, bool]:
    """
    Validates the LinkedIn URL and user information using the Apollo API.

    Args:
        lead_properties (dict): Contains keys like:
            'first_name', 'last_name', 'job_title', 'lead_location', 'user_linkedin_url'.
        tool_config (Optional[List[Dict]]): Contains configuration for the Apollo tool.

    Returns:
        Dict[str, bool]: A dictionary with matching status:
            {
              "first_name_matched": bool,
              "last_name_matched": bool,
              "linkedin_url_valid": bool,
              "title_matched": bool,
              "location_matched": bool
            }
    """
    linkedin_url = lead_properties.get("user_linkedin_url", "")
    match_result = LeadLinkedInMatch()

    linkedin_data = await enrich_person_info_from_apollo(
        linkedin_url=linkedin_url, 
        tool_config=tool_config
    )
    # If no data is returned from Apollo, return defaults (all False except
    # the logic in compare_field where no input -> True).
    if not linkedin_data:
        return match_result.model_dump()

    person_data = linkedin_data.get("person", {})

    # Compare each field systematically
    match_result.first_name_matched = compare_field(lead_properties, person_data, "first_name", "first_name")
    match_result.last_name_matched = compare_field(lead_properties, person_data, "last_name", "last_name")
    match_result.title_matched = compare_field(lead_properties, person_data, "job_title", "title")
    match_result.location_matched = compare_field(lead_properties, person_data, "lead_location", "location")

    # If we got data, we consider the LinkedIn URL valid
    match_result.linkedin_url_valid = True

    return match_result.model_dump()

@assistant_tool
async def validate_linkedin_url_with_proxy_curl(
    lead_properties: Dict[str, Any],
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, bool]:
    """
    Validates the LinkedIn URL and user information using the Proxy Curl API.

    Args:
        lead_properties (dict): Contains keys like:
            'first_name', 'last_name', 'job_title', 'lead_location', 'user_linkedin_url'.
        tool_config (Optional[List[Dict]]): Contains configuration for the Apollo tool.

    Returns:
        Dict[str, bool]: A dictionary with matching status:
            {
              "first_name_matched": bool,
              "last_name_matched": bool,
              "linkedin_url_valid": bool,
              "title_matched": bool,
              "location_matched": bool
            }
    """
    linkedin_url = lead_properties.get("user_linkedin_url", "")
    match_result = LeadLinkedInMatch()

    linkedin_data = await enrich_person_info_from_proxycurl(
        linkedin_url=linkedin_url, 
        tool_config=tool_config
    )
    # If no data is returned from Apollo, return defaults (all False except
    # the logic in compare_field where no input -> True).
    if not linkedin_data:
        return match_result.model_dump()

    person_data = linkedin_data

    # Compare each field systematically
    match_result.first_name_matched = compare_field(lead_properties, person_data, "first_name", "first_name")
    match_result.last_name_matched = compare_field(lead_properties, person_data, "last_name", "last_name")
    match_result.title_matched = compare_field(lead_properties, person_data, "job_title", "occupation")
    # match_result.location_matched = compare_field(lead_properties, person_data, "lead_location", "location")

    # If we got data, we consider the LinkedIn URL valid
    match_result.linkedin_url_valid = True

    return match_result.model_dump()

# --------------------------------------------------------------------------------
# 4. High-Level Validation Router
# --------------------------------------------------------------------------------

ALLOWED_CHECK_LINKEDIN_TOOLS = ["apollo", "proxycurl", "zoominfo"]
LINKEDIN_VALIDATE_TOOL_NAME_TO_FUNCTION_MAP = {
    "apollo": validate_linkedin_url_with_apollo,
    "proxycurl": validate_linkedin_url_with_proxy_curl
}

@assistant_tool
async def check_linkedin_url_validity(
    lead_properties: Dict[str, Any],
    tool_config: Optional[List[Dict]] = None
) -> Dict[str, bool]:
    """
    Validates LinkedIn URL (and related fields) by choosing the appropriate tool
    from the tool_config.

    Args:
        lead_properties (dict): Lead info (e.g. first_name, last_name, job_title, lead_location, user_linkedin_url).
        tool_config (Optional[List[Dict]]): Configuration to identify which tool is available.

    Returns:
        Dict[str, bool]: Standardized response from the chosen validation function.

    Raises:
        ValueError: If no tool configuration or no suitable validation tool is found.
    """
    if not tool_config:
        raise ValueError("No tool configuration found.")

    chosen_tool_func = None
    for item in tool_config:
        tool_name = item.get("name")
        if tool_name in LINKEDIN_VALIDATE_TOOL_NAME_TO_FUNCTION_MAP and tool_name in ALLOWED_CHECK_LINKEDIN_TOOLS:
            chosen_tool_func = LINKEDIN_VALIDATE_TOOL_NAME_TO_FUNCTION_MAP[tool_name]
            break

    if not chosen_tool_func:
        raise ValueError("No suitable LinkedIn validation tool found in tool_config.")

    return await chosen_tool_func(lead_properties, tool_config)
