from supertokens_python.recipe.emailverification.types import EmailDeliveryOverrideInput, EmailTemplateVars
from typing import Dict, Any
import os

def custom_email_delivery(original_implementation: EmailDeliveryOverrideInput) -> EmailDeliveryOverrideInput:
    original_send_email = original_implementation.send_email

    async def send_email(template_vars: EmailTemplateVars, user_context: Dict[str, Any]) -> None:

        # This is: `<YOUR_WEBSITE_DOMAIN>/auth/verify-email`
        dominio_web = os.getenv("WEBSITE_DOMAIN")
        template_vars.email_verify_link = template_vars.email_verify_link.replace(
            f"http://localhost:5173/auth/verify-email", f"http://localhost:5173/verify-email")

        return await original_send_email(template_vars, user_context)

    original_implementation.send_email = send_email
    return original_implementation