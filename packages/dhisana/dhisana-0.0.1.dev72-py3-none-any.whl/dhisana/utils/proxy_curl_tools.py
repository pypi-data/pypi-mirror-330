import asyncio
import json
import logging
import os
import re
import aiohttp
import backoff
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.cache_output_tools import cache_output, retrieve_output
from dhisana.utils.clean_properties import cleanup_properties
from dhisana.utils.domain_parser import get_domain_from_website, is_excluded_domain
from dhisana.utils.serpapi_search_tools import search_google
from dhisana.utils.web_download_parse_tools import get_html_content_from_url
from urllib.parse import urlparse, urlunparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_proxycurl_access_token(tool_config: Optional[List[Dict]] = None) -> str:
    """
    Retrieves the PROXY_CURL_API_KEY access token from the provided tool configuration.

    Args:
        tool_config (list): A list of dictionaries containing the tool configuration. 
                            Each dictionary should have a "name" key and a "configuration" key,
                            where "configuration" is a list of dictionaries containing "name" and "value" keys.

    Returns:
        str: The PROXY_CURL_API_KEY access token.

    Raises:
        ValueError: If the access token is not found in the tool configuration or environment variable.
    """
    PROXY_CURL_API_KEY = None

    if tool_config:
        logger.debug(f"Tool config provided: {tool_config}")
        proxy_curl_config = next(
            (item for item in tool_config if item.get("name") == "proxycurl"), None
        )
        if proxy_curl_config:
            config_map = {
                item["name"]: item["value"]
                for item in proxy_curl_config.get("configuration", [])
                if item
            }
            PROXY_CURL_API_KEY = config_map.get("apiKey")
        else:
            logger.warning("No 'proxycurl' config item found in tool_config.")
    else:
        logger.debug("No tool_config provided or it's None.")

    # Check environment variable if no key found yet
    PROXY_CURL_API_KEY = PROXY_CURL_API_KEY or os.getenv("PROXY_CURL_API_KEY")

    if not PROXY_CURL_API_KEY:
        logger.error("PROXY_CURL_API_KEY not found in configuration or environment.")
        raise ValueError("PROXY_CURL_API_KEY access token not found in tool_config or environment variable")
    return PROXY_CURL_API_KEY


@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=3,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def enrich_person_info_from_proxycurl(
    linkedin_url: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None
):
    """
    Fetch a person's details from Proxycurl using LinkedIn URL, email, or phone number.

    Parameters:
    - linkedin_url (str, optional): LinkedIn profile URL of the person.
    - email (str, optional): Email address of the person.
    - phone (str, optional): Phone number of the person.

    Returns:
    - dict: JSON response containing person information.
    """
    logger.info("Entering enrich_person_info_from_proxycurl")

    API_KEY = get_proxycurl_access_token(tool_config)
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    if not linkedin_url and not email and not phone:
        logger.warning("No linkedin_url, email, or phone provided. At least one is required.")
        return {'error': "At least one of linkedin_url, email, or phone must be provided"}
    
    # Check cache if linkedin_url is provided
    if linkedin_url:
        cached_response = retrieve_output("enrich_person_info_from_proxycurl", linkedin_url)
        if cached_response is not None:
            logger.info(f"Cache hit for LinkedIn URL: {linkedin_url}")
            return cached_response

    params = {}
    if linkedin_url:
        params['url'] = linkedin_url
    if email:
        params['email'] = email
    if phone:
        params['phone'] = phone

    url = 'https://nubela.co/proxycurl/api/v2/linkedin'
    logger.debug(f"Making request to Proxycurl with params: {params}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=HEADERS, params=params) as response:
                logger.debug(f"Received response status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    if linkedin_url:
                        cache_output("enrich_person_info_from_proxycurl", linkedin_url, result)
                    logger.info("Successfully retrieved person info from Proxycurl.")
                    return result
                elif response.status == 404:
                    msg = "Person not found"
                    logger.warning(msg)
                    if linkedin_url:
                        cache_output("enrich_person_info_from_proxycurl", linkedin_url, {'error': msg})
                    return {'error': msg}
                elif response.status == 429:
                    msg = "Rate limit exceeded"
                    logger.warning(msg)
                    await asyncio.sleep(30)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=msg,
                        headers=response.headers
                    )
                else:
                    error_text = await response.text()
                    logger.error(f"Error from Proxycurl: {error_text}")
                    return {'error': error_text}
        except Exception as e:
            logger.exception("Exception occurred while fetching person info from Proxycurl.")
            raise e

@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=3,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def lookup_person_in_proxy_curl_by_name(
    first_name: str,
    last_name: str,
    company_name: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None,
):
    logger.info("Entering lookup_person_in_proxy_curl_by_name")

    if not first_name or not last_name:
        logger.warning("First name or last name missing for lookup.")
        return {'error': "Full name is required"}

    API_KEY = get_proxycurl_access_token(tool_config)
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'first_name': first_name,
        'last_name': last_name,
        'page_size': '1',
    }
    if company_name:
        params['current_company_name'] = company_name

    key = f"{first_name} {last_name} {company_name}".strip()
    if key:
        cached_response = retrieve_output("lookup_person_in_proxycurl_by_name", key)
        if cached_response is not None:
            logger.info(f"Cache hit for name lookup key: {key}")
            return cached_response

    url = 'https://nubela.co/proxycurl/api/v2/search/person'
    logger.debug(f"Making request to Proxycurl with params: {params}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                logger.debug(f"Received response status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    cache_output("lookup_person_in_proxycurl_by_name", key, result)
                    logger.info("Successfully retrieved person search info from Proxycurl.")
                    return result
                elif response.status == 404:
                    msg = "Person not found"
                    logger.warning(msg)
                    if key:
                        cache_output("lookup_person_in_proxycurl_by_name", key, {'error': msg})
                    return {'error': msg}
                elif response.status == 429:
                    msg = "Rate limit exceeded"
                    logger.warning(msg)
                    await asyncio.sleep(30)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=msg,
                        headers=response.headers
                    )
                else:
                    result = await response.json()
                    logger.warning(f"lookup_person_in_proxycurl_by_name error: {result}")
                    return {'error': result}
        except Exception as e:
            logger.exception("Exception occurred while looking up person by name.")
            raise e


@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=3,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def enrich_organization_info_from_proxycurl(
    organization_domain: Optional[str] = None,
    organization_linkedin_url: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None
):
    """
    Fetch an organization's details from Proxycurl using either the organization domain or LinkedIn URL.

    Parameters:
    - organization_domain (str, optional): Domain of the organization.
    - organization_linkedin_url (str, optional): LinkedIn URL of the organization.

    Returns:
    - dict: JSON response containing organization information.
    """
    logger.info("Entering enrich_organization_info_from_proxycurl")

    API_KEY = get_proxycurl_access_token(tool_config)
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    if not organization_domain and not organization_linkedin_url:
        logger.warning("No organization domain or LinkedIn URL provided.")
        return {'error': "Either organization domain or LinkedIn URL must be provided"}

    # If LinkedIn URL is provided, standardize it and fetch data
    if organization_linkedin_url:
        logger.debug(f"Organization LinkedIn URL provided: {organization_linkedin_url}")
        parsed_url = urlparse(organization_linkedin_url)
        if parsed_url.netloc != 'www.linkedin.com':
            standardized_netloc = 'www.linkedin.com'
            standardized_path = parsed_url.path
            if not standardized_path.startswith('/company/'):
                standardized_path = '/company' + standardized_path
            standardized_url = urlunparse(
                parsed_url._replace(netloc=standardized_netloc, path=standardized_path)
            )
            if standardized_url and not standardized_url.endswith('/'):
                standardized_url += '/'
        else:
            standardized_url = organization_linkedin_url
            if standardized_url and not standardized_url.endswith('/'):
                standardized_url += '/'

        # Check cache for standardized LinkedIn URL
        cached_response = retrieve_output("enrich_organization_info_from_proxycurl", standardized_url)
        if cached_response is not None:
            logger.info(f"Cache hit for organization LinkedIn URL: {standardized_url}")
            return cached_response

        # Fetch details using standardized LinkedIn URL
        url = 'https://nubela.co/proxycurl/api/linkedin/company'
        params = {
            'url': standardized_url,
            'categories': 'include',
            'funding_data': 'include',
            'exit_data': 'include',
            'acquisitions': 'include',
            'extra': 'include',
            'use_cache': 'if-present',
            'fallback_to_cache': 'on-error',
        }
        logger.debug(f"Making request to Proxycurl with params: {params}")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=HEADERS, params=params) as response:
                    logger.debug(f"Received response status: {response.status}")
                    if response.status == 200:
                        result = await response.json()
                        cache_output("enrich_organization_info_from_proxycurl", standardized_url, result)
                        logger.info("Successfully retrieved organization info from Proxycurl by LinkedIn URL.")
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"Error from Proxycurl organization info fetch by URL: {error_text}")
                        return {'error': error_text}
            except Exception as e:
                logger.exception("Exception occurred while fetching organization info from Proxycurl by LinkedIn URL.")
                raise e

    # If organization domain is provided, resolve domain to LinkedIn URL and fetch data
    if organization_domain:
        logger.debug(f"Organization domain provided: {organization_domain}")
        cached_response = retrieve_output("enrich_organization_info_from_proxycurl", organization_domain)
        if cached_response is not None:
            logger.info(f"Cache hit for organization domain: {organization_domain}")
            return cached_response

        resolve_url = 'https://nubela.co/proxycurl/api/linkedin/company/resolve'
        params = {'domain': organization_domain}
        logger.debug(f"Making request to Proxycurl to resolve domain with params: {params}")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(resolve_url, headers=HEADERS, params=params) as response:
                    logger.debug(f"Received response status: {response.status}")
                    if response.status == 200:
                        company_data = await response.json()
                        company_url = company_data.get('url')
                        if company_url:
                            parsed_url = urlparse(company_url)
                            if parsed_url.netloc != 'www.linkedin.com':
                                standardized_netloc = 'www.linkedin.com'
                                standardized_path = parsed_url.path
                                if not standardized_path.startswith('/company/'):
                                    standardized_path = '/company' + standardized_path
                                standardized_url = urlunparse(
                                    parsed_url._replace(netloc=standardized_netloc, path=standardized_path)
                                )
                            else:
                                standardized_url = company_url

                            profile_url = 'https://nubela.co/proxycurl/api/v2/linkedin/company'
                            try:
                                async with session.get(profile_url, headers=HEADERS, params={'url': standardized_url}) as profile_response:
                                    logger.debug(f"Received profile response status: {profile_response.status}")
                                    if profile_response.status == 200:
                                        result = await profile_response.json()
                                        cache_output("enrich_organization_info_from_proxycurl", organization_domain, result)
                                        logger.info("Successfully retrieved organization info from Proxycurl by domain.")
                                        return result
                                    else:
                                        error_text = await profile_response.json()
                                        logger.error(
                                            f"Error from Proxycurl organization profile fetch by resolved domain: {error_text}"
                                        )
                                        return {'error': error_text}
                            except Exception as e:
                                logger.exception("Exception occurred while fetching organization profile data.")
                                raise e
                        else:
                            logger.warning("Company URL not found for the provided domain.")
                            return {'error': 'Company URL not found for the provided domain'}
                    elif response.status == 429:
                        msg = "Rate limit exceeded"
                        logger.warning(msg)
                        await asyncio.sleep(30)
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=msg,
                            headers=response.headers
                        )
                    elif response.status == 404:
                        msg = "Item not found"
                        logger.warning(msg)
                        cache_output("enrich_organization_info_from_proxycurl", organization_domain, {'error': msg})
                        return {'error': "Person not found"}
                    else:
                        error_text = await response.text()
                        logger.error(f"Error from Proxycurl domain resolve: {error_text}")
                        return {'error': error_text}
            except Exception as e:
                logger.exception("Exception occurred while resolving organization domain on Proxycurl.")
                raise e


@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=3,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def enrich_job_info_from_proxycurl(
    job_url: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None
):
    """
    Fetch a job's details from Proxycurl using the job URL.

    Parameters:
    - job_url (str, optional): URL of the LinkedIn job posting.

    Returns:
    - dict: JSON response containing job information.
    """
    logger.info("Entering enrich_job_info_from_proxycurl")

    API_KEY = get_proxycurl_access_token(tool_config)
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    if not job_url:
        logger.warning("No job URL provided.")
        return {'error': "Job URL must be provided"}
    
    # Check cache
    cached_response = retrieve_output("enrich_job_info_from_proxycurl", job_url)
    if cached_response is not None:
        logger.info(f"Cache hit for job URL: {job_url}")
        return cached_response

    params = {'url': job_url}
    api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/job'
    logger.debug(f"Making request to Proxycurl for job info with params: {params}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_endpoint, headers=HEADERS, params=params) as response:
                logger.debug(f"Received response status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    cache_output("enrich_job_info_from_proxycurl", job_url, result)
                    logger.info("Successfully retrieved job info from Proxycurl.")
                    return result
                elif response.status == 429:
                    msg = "Rate limit exceeded"
                    logger.warning(msg)
                    await asyncio.sleep(30)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=msg,
                        headers=response.headers
                    )
                elif response.status == 404:
                    msg = "Job not found"
                    logger.warning(msg)
                    cache_output("enrich_job_info_from_proxycurl", job_url, {'error': msg})
                    return {'error': msg}
                else:
                    error_text = await response.text()
                    logger.error(f"Error from Proxycurl: {error_text}")
                    return {'error': error_text}
        except Exception as e:
            logger.exception("Exception occurred while fetching job info from Proxycurl.")
            raise e


@assistant_tool
@backoff.on_exception(
    backoff.expo,
    aiohttp.ClientResponseError,
    max_tries=3,
    giveup=lambda e: e.status != 429,
    factor=10,
)
async def search_recent_job_changes(
    job_titles: List[str],
    locations: List[str],
    max_items_to_return: int = 100,
    tool_config: Optional[List[Dict]] = None
) -> List[dict]:
    """
    Search for individuals with specified job titles and locations who have recently changed jobs.

    Parameters:
    - job_titles (List[str]): List of job titles to search for.
    - locations (List[str]): List of locations to search in.
    - max_items_to_return (int, optional): Maximum number of items to return. Defaults to 100.

    Returns:
    - List[dict]: List of individuals matching the criteria.
    """
    logger.info("Entering search_recent_job_changes")

    API_KEY = get_proxycurl_access_token(tool_config)
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    url = 'https://nubela.co/proxycurl/api/search/person'
    results = []
    page = 1
    per_page = min(max_items_to_return, 100)

    logger.debug(f"Starting search with job_titles={job_titles}, locations={locations}, max_items={max_items_to_return}")

    async with aiohttp.ClientSession() as session:
        while len(results) < max_items_to_return:
            params = {
                'job_title': ','.join(job_titles),
                'location': ','.join(locations),
                'page': page,
                'num_records': per_page
            }
            logger.debug(f"Request params: {params}")

            try:
                async with session.get(url, headers=HEADERS, params=params) as response:
                    logger.debug(f"Received response status: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        people = data.get('persons', [])
                        if not people:
                            logger.info("No more people found, ending search.")
                            break
                        results.extend(people)
                        logger.info(f"Fetched {len(people)} results on page {page}. Total so far: {len(results)}")
                        page += 1
                        if len(results) >= max_items_to_return:
                            logger.info("Reached max items limit.")
                            break
                    elif response.status == 429:
                        msg = "Rate limit exceeded"
                        logger.warning(msg)
                        await asyncio.sleep(30)
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=msg,
                            headers=response.headers
                        )
                    else:
                        error_text = await response.text()
                        logger.error(f"Error while searching recent job changes: {error_text}")
                        break
            except Exception as e:
                logger.exception("Exception occurred while searching recent job changes.")
                break

    return results[:max_items_to_return]


@assistant_tool
async def find_matching_job_posting_proxy_curl(
    company_name: str,
    keywords_check: List[str],
    optional_keywords: List[str],
    organization_linkedin_url: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None  
) -> List[str]:
    """
    Find job postings on LinkedIn for a given company using Google Custom Search.
    Double check the same with Proxycurl API.

    Args:
        company_name (str): The name of the company.
        keywords_check (List[str]): A list of keywords to include in the search.
        optional_keywords (List[str]): A list of optional keywords to include in the search.
        organization_linkedin_url (Optional[str]): The LinkedIn URL of the company.
        tool_config (Optional[List[Dict]]): Proxycurl tool configuration.
    
    Returns:
        List[str]: A list of job posting links.
    """
    logger.info("Entering find_matching_job_posting_proxy_curl")

    if not company_name:
        logger.warning("No company name provided.")
        return []
    
    if not keywords_check:
        logger.warning("No keywords_check provided, defaulting to an empty list.")
        keywords_check = []

    if not optional_keywords:
        logger.warning("No optional_keywords provided, defaulting to an empty list.")
        optional_keywords = []

    keywords_list = [kw.strip().lower() for kw in keywords_check]
    job_posting_links = []

    # Build the search query
    keywords_str = ' '.join(f'"{kw}"' for kw in keywords_check)
    optional_keywords_str = ' '.join(f'{kw}' for kw in optional_keywords)
    query = f'site:*linkedin.com/jobs/view/ "{company_name}" {keywords_str} {optional_keywords_str}'
    logger.debug(f"Google search query: {query}")

    # First Google search attempt
    results = await search_google(query.strip(), 1, tool_config=tool_config)
    if not isinstance(results, list) or len(results) == 0:
        logger.info("No results found. Attempting fallback query without optional keywords.")
        query = f'site:*linkedin.com/jobs/view/ "{company_name}" {keywords_str}'
        results = await search_google(query.strip(), 1, tool_config=tool_config)
        if not isinstance(results, list) or len(results) == 0:
            logger.info("No job postings found in fallback search either.")
            return job_posting_links

    # Process each search result
    for result_item in results:
        try:
            result_json = json.loads(result_item)
        except json.JSONDecodeError:
            logger.debug("Skipping invalid JSON result.")
            continue

        link = result_json.get('link', '')
        if not link:
            logger.debug("No link in result; skipping.")
            continue
        
        if "linkedin.com/jobs/view/" not in link:
            logger.debug("Link is not a LinkedIn job posting; skipping.")
            continue

        # Normalize the LinkedIn domain to www.linkedin.com
        parsed = urlparse(link)
        new_link = parsed._replace(netloc="www.linkedin.com").geturl()
        link = new_link

        # Use Proxycurl to enrich job info
        logger.debug(f"Fetching job info from Proxycurl for link: {link}")
        try:
            json_result = await enrich_job_info_from_proxycurl(link, tool_config=tool_config)
        except Exception as e:
            logger.exception("Exception occurred while enriching job info from Proxycurl.")
            continue

        if not json_result:
            logger.debug("No job info returned; skipping.")
            continue

        text = json.dumps(json_result).lower()

        company_match = False
        if organization_linkedin_url and json_result.get('company', {}):
            result_url = json_result.get('company', {}).get('url', '').lower()
            result_path = urlparse(result_url).path
            company_path = urlparse(organization_linkedin_url.lower()).path
            company_match = (result_path == company_path)
        else:
            company_match = False

        keywords_found = any(kw in text for kw in keywords_list)

        # If company matches and keywords are found, add to results
        if company_match and keywords_found:
            job_posting_links.append(link)

    logger.info(f"Found {len(job_posting_links)} matching job postings.")
    return job_posting_links

def fill_in_missing_properties(input_user_properties: dict, person_data: dict) -> dict:
    """
    If input_user_properties has a non-empty value for a field, keep it.
    Otherwise, use that field from person_data.
    """

    # Helper function to determine if a property is considered "empty"
    def is_empty(value):
        # Checks for None, empty string, or string with only whitespace
        return value is None or (isinstance(value, str) and not value.strip())

    # Email
    if is_empty(input_user_properties.get("email")):
        input_user_properties["email"] = person_data.get("email", "")

    # Phone
    if is_empty(input_user_properties.get("phone")):
        input_user_properties["phone"] = person_data.get("contact", {}).get("sanitized_phone", "")

    # Full name
    if is_empty(input_user_properties.get("full_name")) and person_data.get("full_name"):
        input_user_properties["full_name"] = person_data["full_name"]

    # First name
    if is_empty(input_user_properties.get("first_name")) and person_data.get("first_name"):
        input_user_properties["first_name"] = person_data["first_name"]

    # Last name
    if is_empty(input_user_properties.get("last_name")) and person_data.get("last_name"):
        input_user_properties["last_name"] = person_data["last_name"]

    # Occupation -> job_title
    if is_empty(input_user_properties.get("job_title")) and person_data.get("occupation"):
        input_user_properties["job_title"] = person_data["occupation"]

    # Headline
    if is_empty(input_user_properties.get("headline")) and person_data.get("headline"):
        input_user_properties["headline"] = person_data["headline"]

    # Summary
    if is_empty(input_user_properties.get("summary_about_lead")) and person_data.get("summary"):
        input_user_properties["summary_about_lead"] = person_data["summary"]

    # Experiences
    experiences = person_data.get("experiences", [])
    if experiences:
        # Current role data
        # Organization Name
        if is_empty(input_user_properties.get("organization_name")):
            input_user_properties["organization_name"] = experiences[0].get("company", "")

        # Organization Linkedin URL
        org_url = experiences[0].get("company_linkedin_profile_url", "")
        if org_url and is_empty(input_user_properties.get("organization_linkedin_url")):
            input_user_properties["organization_linkedin_url"] = org_url

        # If there's a second experience, track it as previous
        if len(experiences) > 1:
            previous_org = experiences[1]
            prev_org_url = previous_org.get("company_linkedin_profile_url", "")

            if prev_org_url and is_empty(input_user_properties.get("previous_organization_linkedin_url")):
                input_user_properties["previous_organization_linkedin_url"] = prev_org_url

            if is_empty(input_user_properties.get("previous_organization_name")):
                input_user_properties["previous_organization_name"] = previous_org.get("company", "")

    # Combine city/state if available (and if lead_location is empty)
    if is_empty(input_user_properties.get("lead_location")):
        if person_data.get("city") or person_data.get("state"):
            combined = f"{person_data.get('city', '')}, {person_data.get('state', '')}"
            input_user_properties["lead_location"] = combined.strip(", ")

    return input_user_properties


async def enrich_user_info_with_proxy_curl(input_user_properties: dict, tool_config: Optional[List[Dict]] = None) -> dict:
    """
    Enriches the user info (input_user_properties) with data from Proxycurl using:
    1. LinkedIn URL or email (if provided),
    2. Otherwise by first name and last name, or full name.

    Args:
        input_user_properties (dict): Dictionary with user details (e.g. LinkedIn URL, email, names).
        tool_config (Optional[List[Dict]]): Proxycurl tool configuration.

    Returns:
        dict: Updated input_user_properties with enriched data from Proxycurl.
    """
    logger.info("Entering enrich_user_info_with_proxy_curl")

    if not input_user_properties:
        logger.warning("No input_user_properties provided; returning empty dict.")
        return {}

    linkedin_url = input_user_properties.get("user_linkedin_url", "")
    email = input_user_properties.get("email", "")
    user_data_from_proxycurl = None

    logger.debug(
        f"Attempting to enrich data for LinkedIn URL='{linkedin_url}', Email='{email}'"
    )

    # If linkedin url or email is present, lookup
    if linkedin_url or email:
        try:
            user_data_from_proxycurl = await enrich_person_info_from_proxycurl(
                linkedin_url=linkedin_url,
                email=email,
                tool_config=tool_config
            )
            if user_data_from_proxycurl and linkedin_url:
                logger.info(f"User data found for LinkedIn URL: {linkedin_url}")
                input_user_properties["user_linkedin_url"] = linkedin_url
        except Exception as e:
            logger.exception("Exception occurred while enriching person info by LinkedIn or email.")
    else:
        # Otherwise, fallback to name-based lookup
        first_name = input_user_properties.get("first_name", "")
        last_name = input_user_properties.get("last_name", "")
        full_name = input_user_properties.get("full_name", "")

        if not first_name or not last_name:
            if full_name:
                name_parts = full_name.split(" ", 1)
                first_name = first_name or name_parts[0]
                last_name = last_name or (name_parts[1] if len(name_parts) > 1 else "")

        if not full_name:
            full_name = f"{first_name} {last_name}".strip()

        company = input_user_properties.get("organization_name", "")
        logger.debug(f"Looking up person by name: {first_name} {last_name}, company: {company}")

        if first_name and last_name:
            try:
                search_result = await lookup_person_in_proxy_curl_by_name(
                    first_name=first_name,
                    last_name=last_name,
                    company_name=company,
                    tool_config=tool_config
                )
                results = search_result.get("results", [])
                person_company = ""
                for person in results:
                    linkedin_profile_url = person.get("linkedin_profile_url", "")
                    if linkedin_profile_url:
                        data_from_proxycurl = await enrich_person_info_from_proxycurl(
                            linkedin_url=linkedin_profile_url,
                            tool_config=tool_config
                        )
                        if data_from_proxycurl:
                            person_name = data_from_proxycurl.get("name", "").lower()
                            person_first_name = data_from_proxycurl.get("first_name", "").lower()
                            person_last_name = data_from_proxycurl.get("last_name", "").lower()
                            experiences = data_from_proxycurl.get('experiences', [])
                            for exp in experiences:
                                exp_company = exp.get("company", "").lower()
                                if exp_company == company.lower():
                                    person_company = exp_company
                                    break
                            # If there's a match for name/company, use the data
                            if (
                                (person_name == full_name.lower() or
                                 (person_first_name == first_name.lower() and person_last_name == last_name.lower()))
                                and (not company or person_company == company.lower())
                            ):
                                logger.info(f"User data found for name: {full_name}")
                                input_user_properties["user_linkedin_url"] = linkedin_profile_url
                                user_data_from_proxycurl = data_from_proxycurl
                                break
            except Exception as e:
                logger.exception("Exception occurred while looking up person by name.")
                pass

    if not user_data_from_proxycurl:
        logger.debug("No user data returned from Proxycurl.")
        input_user_properties["linkedin_url_match"] = False
        return input_user_properties

    # If user data was found, populate input_user_properties
    url_pattern = re.compile(r'(https?://[^\s]+)', re.IGNORECASE)

    def sanitize_urls_in_data(data):
        """
        Recursively walk through 'data' and remove any URL that is not under linkedin.com domain.
        """
        if isinstance(data, dict):
            sanitized = {}
            for k, v in data.items():
                sanitized[k] = sanitize_urls_in_data(v)
            return sanitized
        elif isinstance(data, list):
            return [sanitize_urls_in_data(item) for item in data]
        elif isinstance(data, str):
            def replace_non_linkedin(match):
                link = match.group(1)
                if "linkedin.com" not in (urlparse(link).netloc or ""):
                    return ""
                return link
            return re.sub(url_pattern, replace_non_linkedin, data)
        return data

    person_data = sanitize_urls_in_data(user_data_from_proxycurl)
    additional_props = input_user_properties.get("additional_properties") or {}
    
    # Check if there's a match on first/last name
    first_matched = bool(
        input_user_properties.get("first_name")
        and person_data.get("first_name") == input_user_properties["first_name"]
    )
    last_matched = bool(
        input_user_properties.get("last_name")
        and person_data.get("last_name") == input_user_properties["last_name"]
    )

    if first_matched and last_matched:
        input_user_properties["linkedin_url_match"] = True
        input_user_properties["linkedin_validation_status"] = "valid"
        

    input_user_properties = fill_in_missing_properties(input_user_properties, person_data)
    
    company_data = await enrich_organization_info_from_proxycurl(
        organization_linkedin_url=input_user_properties.get("organization_linkedin_url"),
        tool_config=tool_config
    )
    
    person_data = cleanup_properties(person_data)
            
    additional_props["pc_person_data"] = json.dumps(person_data)
    
    company_data = cleanup_properties(company_data)
    additional_props["pc_company_data"] = json.dumps(company_data)
    input_user_properties["additional_properties"] = additional_props


    logger.info("Enrichment of user info with Proxycurl complete.")
    return input_user_properties
