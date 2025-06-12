from supertokens_python.recipe.emailverification.types import EmailDeliveryOverrideInput, EmailTemplateVars
from supertokens_python.recipe.emailpassword.types import EmailDeliveryOverrideInput, EmailTemplateVars
from decouple import config
from typing import Dict, Any
import os

def custom_email_delivery(original_implementation: EmailDeliveryOverrideInput) -> EmailDeliveryOverrideInput:
    original_send_email = original_implementation.send_email

    async def send_email(template_vars: EmailTemplateVars, user_context: Dict[str, Any]) -> None:

        dominio_web = config("WEBSITE_DOMAIN")
        template_vars.email_verify_link = template_vars.email_verify_link.replace(
            f"http://localhost:5173/auth/verify-email", f"http://localhost:5173/verify-email")

        return await original_send_email(template_vars, user_context)

    original_implementation.send_email = send_email
    return original_implementation

def custom_email_deliver(original_implementation: EmailDeliveryOverrideInput) -> EmailDeliveryOverrideInput:
    original_send_email = original_implementation.send_email

    async def send_email(template_vars: EmailTemplateVars, user_context: Dict[str, Any]) -> None:

        template_vars.password_reset_link = template_vars.password_reset_link.replace(
            "http://localhost:3000/auth/reset-password", "http://localhost:3000/your/path")
        return await original_send_email(template_vars, user_context)

    original_implementation.send_email = send_email
    return original_implementation