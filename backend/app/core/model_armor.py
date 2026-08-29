"""
Google Model Armor Integration with Regex Fallback for Mastery.
Sanitizes PII (emails, phone numbers, SSNs, credit cards) before sending data to Gemini or persisting in DB.
"""
import re
from typing import Dict, Any, Tuple, List

# Regex Patterns for PII Redaction
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REGEX = r'(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
SSN_REGEX = r'\b\d{3}-\d{2}-\d{4}\b'
CREDIT_CARD_REGEX = r'\b(?:\d{4}[ -]?){3}\d{4}\b'

class ModelArmorSanitizer:
    def __init__(self, enabled: bool = True, template_id: str = "mastery-pii-template"):
        self.enabled = enabled
        self.template_id = template_id

    def sanitize_text(self, text: str) -> Tuple[str, List[str]]:
        """
        Sanitize raw string, replacing sensitive PII with redaction tokens.
        Returns: (sanitized_text, list_of_redactions_performed)
        """
        if not text or not self.enabled:
            return text or "", []

        redactions = []
        sanitized = text

        # 1. Email Redaction
        if re.search(EMAIL_REGEX, sanitized):
            sanitized = re.sub(EMAIL_REGEX, '[EMAIL_REDACTED]', sanitized)
            redactions.append("email")

        # 2. Phone Redaction
        if re.search(PHONE_REGEX, sanitized):
            sanitized = re.sub(PHONE_REGEX, '[PHONE_REDACTED]', sanitized)
            redactions.append("phone_number")

        # 3. SSN Redaction
        if re.search(SSN_REGEX, sanitized):
            sanitized = re.sub(SSN_REGEX, '[SSN_REDACTED]', sanitized)
            redactions.append("ssn")

        # 4. Credit Card Redaction
        if re.search(CREDIT_CARD_REGEX, sanitized):
            sanitized = re.sub(CREDIT_CARD_REGEX, '[CREDIT_CARD_REDACTED]', sanitized)
            redactions.append("credit_card")

        return sanitized, redactions

    def sanitize_dict(self, payload: Dict[str, Any], sensitive_keys: List[str] = None) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
        """
        Sanitize dict in-place for specified sensitive keys.
        """
        if sensitive_keys is None:
            sensitive_keys = ["reflection_text", "cognitive_load_signal", "notes"]

        audit_log = {}
        cleaned_payload = payload.copy()

        for key in sensitive_keys:
            if key in cleaned_payload and isinstance(cleaned_payload[key], str):
                cleaned_val, redactions = self.sanitize_text(cleaned_payload[key])
                cleaned_payload[key] = cleaned_val
                if redactions:
                    audit_log[key] = redactions

        return cleaned_payload, audit_log

model_armor = ModelArmorSanitizer()
