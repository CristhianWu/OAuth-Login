from supertokens_python.recipe.emailverification.types import EmailDeliveryOverrideInput, EmailTemplateVars
from supertokens_python.recipe.emailpassword.types import EmailDeliveryOverrideInput, EmailTemplateVars
from typing import Dict, Any

def custom_verification_email_delivery(original_implementation: EmailDeliveryOverrideInput) -> EmailDeliveryOverrideInput:
    original_send_email = original_implementation.send_email

    async def send_email(template_vars: EmailTemplateVars, user_context: Dict[str, Any]) -> None:
        # must change the second url to the one you desire
        template_vars.email_verify_link = template_vars.email_verify_link.replace(
            f"http://localhost:5173/auth/verify-email", f"http://localhost:5173/your/path")

        return await original_send_email(template_vars, user_context)

    original_implementation.send_email = send_email
    return original_implementation
