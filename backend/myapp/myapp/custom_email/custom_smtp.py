from supertokens_python.recipe.emailverification.types import SMTPOverrideInput as EVSMTPOverrideInput, EmailTemplateVars as EVEmailTemplateVars
from supertokens_python.recipe.emailpassword.types import SMTPOverrideInput, EmailTemplateVars
from supertokens_python.ingredients.emaildelivery.types import EmailContent
from typing import Dict, Any
from supertokens_python.recipe.emailpassword.types import EmailDeliveryOverrideInput, EmailTemplateVars


def custom_smtp_reset_password_content_override(original_implementation: SMTPOverrideInput) -> SMTPOverrideInput:
    original_get_content = original_implementation.get_content

    async def get_content(template_vars: EmailTemplateVars, user_context: Dict[str, Any]) -> EmailContent:
        # contenido de recuperacion de contraseña
        reset_link = template_vars.password_reset_link
        user_email = template_vars.user

        # Llamar la implementacion original y cambiarla
        original_content = await original_get_content(template_vars, user_context)

        # Cambiar asunto
        original_content.subject = "Recuperar contraseña"

        original_content.is_html =  f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Verificaci&oacute;n de Correo</title>
            </head>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
                <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                        <td align="center">
                            <table width="600px" style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                <tr>
                                    <td align="center">
                                        <h2 style="color: #F86F67;">Canbio de contrase&ntilde;a Peppas App!</h2>
                                        <p style="color: #555; font-size: 16px;">
                                            Antes de comenzar, necesitamos verificar tu correo electr&oacute;nico.
                                        </p>
                                        <p style="color: #555; font-size: 16px;">
                                            Haz clic en el siguiente bot&oacute;n para :
                                        </p>
                                        <p>
                                            <a href="{reset_link}" style="background-color: #F86F67; color: #ffffff; padding: 12px 20px; text-decoration: none; font-size: 16px; border-radius: 5px; display: inline-block;">
                                                Confirmar Cuenta
                                            </a>
                                        </p>
                                        <p style="color: #777; font-size: 14px;">
                                            Este enlace est&aacute; disponible por 24 horas.
                                        </p>
                                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                                        <p style="color: #777; font-size: 14px;">
                                            Si no solicitaste este correo, ign&oacute;ralo.
                                        </p>
                                        <p style="color: #F86F67; font-size: 14px; font-weight: bold;">
                                            - Peppa Team
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

        return original_content

    original_implementation.get_content = get_content
    return original_implementation


def custom_smtp_email_verification_content_override(original_implementation: EVSMTPOverrideInput) -> EVSMTPOverrideInput:
    original_get_content = original_implementation.get_content

    async def get_content(template_vars: EVEmailTemplateVars, user_context: Dict[str, Any]) -> EmailContent:
        # contenido de verificacion de email
        verify_link = template_vars.email_verify_link
        user_email = template_vars.user

        # Llamar la implementacion original y cambiarla
        original_content = await original_get_content(template_vars, user_context)

        # Cambiar asunto
        original_content.subject = "Verifique su cuenta"

        # Modificar el contenido del email
        original_content.body = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Verificaci&oacute;n de Correo</title>
            </head>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
                <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                        <td align="center">
                            <table width="600px" style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                                <tr>
                                    <td align="center">
                                        <h2 style="color: #F86F67;">Bienvenido a Peppas App!</h2>
                                        <p style="color: #555; font-size: 16px;">
                                            Antes de comenzar, necesitamos verificar tu correo electr&oacute;nico.
                                        </p>
                                        <p style="color: #555; font-size: 16px;">
                                            Haz clic en el siguiente bot&oacute;n para confirmar tu cuenta:
                                        </p>
                                        <p>
                                            <a href="{verify_link}" style="background-color: #F86F67; color: #ffffff; padding: 12px 20px; text-decoration: none; font-size: 16px; border-radius: 5px; display: inline-block;">
                                                Confirmar Cuenta
                                            </a>
                                        </p>
                                        <p style="color: #777; font-size: 14px;">
                                            Este enlace est&aacute; disponible por 24 horas.
                                        </p>
                                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                                        <p style="color: #777; font-size: 14px;">
                                            Si no solicitaste este correo, ign&oacute;ralo.
                                        </p>
                                        <p style="color: #F86F67; font-size: 14px; font-weight: bold;">
                                            - Peppa Team
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



def custom_email_deliver(original_implementation: EmailDeliveryOverrideInput) -> EmailDeliveryOverrideInput:
    original_send_email = original_implementation.send_email

    async def send_email(template_vars: EmailTemplateVars, user_context: Dict[str, Any]) -> None:
        # This is: `<YOUR_WEBSITE_DOMAIN>/auth/reset-password`
        template_vars.password_reset_link = template_vars.password_reset_link.replace(
            "http://localhost:3000/auth/reset-password", "http://localhost:3000/your/path")
        return await original_send_email(template_vars, user_context)

    original_implementation.send_email = send_email
    return original_implementation