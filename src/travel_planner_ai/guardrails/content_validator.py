import re
import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

def validate_blog_content(agent_output):
    """
    LLM-powered guardrail function for Responsible AI content validation.
    Uses AI to detect PII, bias, harmful content, and ensure ethical standards.
    """
    try:
        # Extract content from agent output
        if hasattr(agent_output, 'raw'):
            content = agent_output.raw
        else:
            content = str(agent_output)
        
        # Initialize LLM for guardrail validation
        guardrail_llm = LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Guardrail validation prompt
        guardrail_prompt = f"""
        You are a Responsible AI content validator. Analyze the following travel content and:
        
        1. DETECT & REDACT PII: Find and replace any personal information (emails, phones, addresses, credit cards, SSNs) with [PII_REDACTED]
        2. CHECK FOR HARMFUL CONTENT: Identify discriminatory, offensive, illegal, or unsafe content
        3. DETECT BIAS: Look for unfair bias against any group, gender, race, or demographic
        4. ENSURE INCLUSIVITY: Verify content is accessible and welcoming to all travelers
        5. CULTURAL SENSITIVITY: Check for respectful treatment of cultures and customs
        
        Content to validate:
        {content}
        
        Respond with:
        - VALIDATION_STATUS: PASS or FAIL
        - CLEANED_CONTENT: The content with PII redacted and any issues fixed
        - ISSUES_FOUND: List any problems detected
        
        If FAIL, explain why and suggest improvements.
        Always add appropriate AI disclaimers about verification and responsible travel.
        """
        
        # Get LLM validation response
        validation_response = guardrail_llm.invoke(guardrail_prompt)
        
        # Parse response to determine if content passes
        if "VALIDATION_STATUS: FAIL" in validation_response:
            return False, "Content blocked by AI guardrails. Please regenerate with more inclusive and ethical content."
        
        # Extract cleaned content or use original with basic disclaimer
        if "CLEANED_CONTENT:" in validation_response:
            cleaned_start = validation_response.find("CLEANED_CONTENT:") + len("CLEANED_CONTENT:")
            cleaned_content = validation_response[cleaned_start:].strip()
        else:
            cleaned_content = content
        
        # Add standard AI disclaimer
        disclaimer = "\n\n---\nAI Travel Assistant: This information is AI-generated and validated by responsible AI guardrails. Please verify details when booking. Safe travels!"
        
        return True, cleaned_content + disclaimer
        
    except Exception as e:
        # Fallback: Basic PII redaction + disclaimer
        content_str = str(agent_output) if agent_output else "Content unavailable"
        
        # Basic PII patterns
        pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
        
        for pii_type, pattern in pii_patterns.items():
            content_str = re.sub(pattern, '[PII_REDACTED]', content_str, flags=re.IGNORECASE)
        
        fallback_disclaimer = "\n\n---\nAI Assistant: Guardrail validation failed. Content processed with basic PII protection. Please verify all information carefully."
        return True, content_str + fallback_disclaimer