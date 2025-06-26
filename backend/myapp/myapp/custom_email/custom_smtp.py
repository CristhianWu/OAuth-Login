from supertokens_python.recipe.emailverification.types import SMTPOverrideInput as EVSMTPOverrideInput, EmailTemplateVars as EVEmailTemplateVars
from supertokens_python.ingredients.emaildelivery.types import EmailContent
from typing import Dict, Any


def custom_smtp_email_verification_content_override(original_implementation: EVSMTPOverrideInput) -> EVSMTPOverrideInput:
    original_get_content = original_implementation.get_content

    async def get_content(template_vars: EVEmailTemplateVars, user_context: Dict[str, Any]) -> EmailContent:
        verify_link = template_vars.email_verify_link

        # Call original implementation for customization
        original_content = await original_get_content(template_vars, user_context)

        # Change Subject
        original_content.subject = "Verifique su cuenta"

        # Email Content
        original_content.body = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Email Verification</title>
            </head>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
                <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                        <td align="center">
                            <table width="600px" style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                <tr>
                                    <td align="center">
                                        <h2 style="color: #F86F67;">Welcome!</h2>
                                        <p style="color: #555; font-size: 16px;">
                                            Before getting started, we need to verify your email address.
                                        </p>
                                        <p style="color: #555; font-size: 16px;">
                                            Please click the button below to confirm your account:
                                        </p>
                                        <p>
                                            <a href="{verify_link}" style="background-color: #F86F67; color: #ffffff; padding: 12px 20px; text-decoration: none; font-size: 16px; border-radius: 5px; display: inline-block;">
                                                Confirm Account
                                            </a>
                                        </p>
                                        <p style="color: #777; font-size: 14px;">
                                            This link will expire in 24 hours.
                                        </p>
                                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                                        <p style="color: #777; font-size: 14px;">
                                            If you did not request this email, please ignore it.
                                        </p>
                                        <p style="color: #F86F67; font-size: 14px; font-weight: bold;">
                                            Thank you!
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
        original_content.is_html = True
        return original_content

    original_implementation.get_content = get_content
    return original_implementation



