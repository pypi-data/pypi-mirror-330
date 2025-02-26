# ----------------------------------------------------------------------
# LinkedIn Message Generation Code (Refactored to mirror email structure)
# ----------------------------------------------------------------------

from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

from dhisana.schemas.sales import (
    ContentGenerationContext, 
    ConversationContext,
    CampaignContext,
    Lead, 
    MessageGenerationInstructions, 
    MessageItem, 
    SenderInfo
)
from dhisana.utils.generate_structured_output_internal import (
    get_structured_output_internal,
    get_structured_output_with_assistant_and_vector_store
)
from dhisana.utils.assistant_tool_tag import assistant_tool

# ----------------------------------------------------------------------
# LinkedIn Connection Message Schema
# ----------------------------------------------------------------------
class LinkedInConnectMessage(BaseModel):
    subject: str
    body: str

# ----------------------------------------------------------------------
# Cleanup function (similar to cleanup_email_context)
# ----------------------------------------------------------------------
def cleanup_linkedin_context(linkedin_context: ContentGenerationContext) -> ContentGenerationContext:
    """
    Return a copy of ContentGenerationContext without unneeded or sensitive fields 
    for LinkedIn generation.
    """
    clone_context = linkedin_context.copy(deep=True)
    
    # Example: remove irrelevant external data for this context
    if clone_context.external_known_data:
        clone_context.external_known_data.external_openai_vector_store_id = None

    # Remove extra fields on the lead_info if desired
    clone_context.lead_info.task_ids = None
    clone_context.lead_info.email_validation_status = None
    clone_context.lead_info.linkedin_validation_status = None
    clone_context.lead_info.research_status = None
    clone_context.lead_info.enchrichment_status = None

    return clone_context

# ----------------------------------------------------------------------
# Known Framework Variations (fallback if user instructions are not provided)
# ----------------------------------------------------------------------
LINKEDIN_FRAMEWORK_VARIATIONS = [
    "Use a friendly intro mentioning their role and a quick reason to connect.",
    "Use social proof: reference an industry success story or insight.",
    "Use a brief mention of mutual interest or connection.",
    "Use P-S-B style (Pain, Solution, Benefit) but under 40 words.",
    "Use a 3-Bullet Approach: Industry/Pain, Value, Simple Ask."
]

# ----------------------------------------------------------------------
# Core function to generate a LinkedIn copy (similar to generate_personalized_email_copy)
# ----------------------------------------------------------------------
async def generate_personalized_linkedin_copy(
    linkedin_context: ContentGenerationContext,
    variation_text: str,
    tool_config: Optional[List[Dict]] = None,
) -> dict:
    """
    Generate a personalized LinkedIn connection message using the provided context and instructions.

    Steps:
      1. Build a prompt referencing 6 main sections:
          (a) Lead Info
          (b) Sender Info
          (c) Campaign Info
          (d) Variation / Instructions
          (e) External Data (if any)
          (f) Current Conversation
      2. Generate the LinkedIn message with or without vector store usage.
      3. Return the final subject & body, ensuring < 40 words.
    """
    cleaned_context = cleanup_linkedin_context(linkedin_context)

    lead_data = cleaned_context.lead_info or Lead()
    sender_data = cleaned_context.sender_info or SenderInfo()
    campaign_data = cleaned_context.campaign_context or CampaignContext()
    conversation_data = cleaned_context.current_conversation_context or ConversationContext()

    # Construct the consolidated prompt
    prompt = f"""
        Hi AI Assistant,

        Below is the context in 6 main sections. Use it to craft a concise, professional LinkedIn connection request message:
        Linked in connect message HAS to be maximum of 40 words. DO NOT go more than 40 words.

        1) Lead Information:
        {lead_data.dict()}

        2) Sender Information:
        Full Name: {sender_data.sender_full_name or ''}
        First Name: {sender_data.sender_first_name or ''}
        Last Name: {sender_data.sender_last_name or ''}
        Bio: {sender_data.sender_bio or ''}

        3) Campaign Information:
        Product Name: {campaign_data.product_name or ''}
        Value Proposition: {campaign_data.value_prop or ''}
        Call To Action: {campaign_data.call_to_action or ''}
        Pain Points: {campaign_data.pain_points or []}
        Proof Points: {campaign_data.proof_points or []}

        4) Follow these Instructions to generate the likedin connection request message:
        {variation_text}

        5) External Data / Vector Store:
        (File search or additional context if available.)

        6) Current Conversation Context:
        Email Thread: {conversation_data.current_email_thread or ''}
        LinkedIn Thread: {conversation_data.current_linkedin_thread or ''}

        IMPORTANT REQUIREMENTS:
        - Output must be JSON with "subject" and "body" fields only.
        - The entire message must be under 40 words total (subject + body).
        - No placeholders or extra instructions in the final output.
        - Do not include personal addresses, IDs, or irrelevant internal data.
    """

    vector_store_id = (
        linkedin_context.external_known_data.external_openai_vector_store_id
        if linkedin_context.external_known_data else None
    )

    if vector_store_id:
        # Use the vector store if available
        response_data, status = await get_structured_output_with_assistant_and_vector_store(
            prompt=prompt,
            response_format=LinkedInConnectMessage,
            vector_store_id=vector_store_id,
            tool_config=tool_config
        )
    else:
        # Otherwise, generate internally
        response_data, status = await get_structured_output_internal(
            prompt=prompt,
            response_format=LinkedInConnectMessage,
            tool_config=tool_config
        )

    if status != "SUCCESS":
        raise Exception("Error: Could not generate the LinkedIn message.")

    # Wrap in MessageItem for consistency
    response_item = MessageItem(
        message_id="",  # fill in if you have an ID
        sender_name=sender_data.sender_full_name or "",
        sender_email=sender_data.sender_email or "",
        receiver_name=lead_data.full_name or "",
        receiver_email=lead_data.email or "",
        iso_datetime=datetime.utcnow().isoformat(),
        subject=response_data.subject,
        body=response_data.body
    )

    return response_item.model_dump()

# ----------------------------------------------------------------------
# Primary function to generate multiple LinkedIn message variations
# (similar to generate_personalized_email)
# ----------------------------------------------------------------------
@assistant_tool
async def generate_personalized_linkedin_message(
    linkedin_context: ContentGenerationContext,
    number_of_variations: int = 3,
    tool_config: Optional[List[Dict]] = None
) -> List[dict]:
    """
    Generate multiple variations of a personalized LinkedIn connection message 
    using the provided context and instructions.

    :param linkedin_context: Consolidated context for LinkedIn generation
    :param number_of_variations: Number of variations to produce
    :param tool_config: Optional config for tool or vector store
    :return: A list of dictionaries, each containing 'subject' and 'body' only
    """
    message_instructions = linkedin_context.message_instructions or MessageGenerationInstructions()
    user_instructions_exist = bool((message_instructions.instructions_to_generate_message or "").strip())

    linkedin_variations = []
    
    for i in range(number_of_variations):
        # If user provided custom instructions, use them for each variation
        # Otherwise, pick from fallback frameworks in a round-robin fashion
        if user_instructions_exist:
            variation_text = message_instructions.instructions_to_generate_message
        else:
            variation_text = LINKEDIN_FRAMEWORK_VARIATIONS[i % len(LINKEDIN_FRAMEWORK_VARIATIONS)]
        
        personalized_copy = await generate_personalized_linkedin_copy(
            linkedin_context=linkedin_context,
            variation_text=variation_text,
            tool_config=tool_config
        )
        linkedin_variations.append(personalized_copy)

    return linkedin_variations
