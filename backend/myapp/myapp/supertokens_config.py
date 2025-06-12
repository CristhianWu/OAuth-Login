from supertokens_python.recipe import (
    emailpassword,
    session,
    dashboard,
    userroles,
    emailverification,)
from supertokens_python.ingredients.emaildelivery.types import (
    EmailDeliveryConfig,
    SMTPSettingsFrom,
    SMTPSettings)
from supertokens_python.recipe.emailpassword import SMTPService as EPSMTPService
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
)
from .custom_email.custom_delivery import (custom_email_deliver,
                                           custom_email_delivery)
from .custom_email.custom_smtp import (custom_smtp_email_verification_content_override,
                                      custom_smtp_reset_password_content_override)
# Supertokens core
supertokens_config = SupertokensConfig(
    connection_uri="http://supertokens:3567",
    api_key="f84e167c-24a9-49d7-a334-474ac6c79004",
)

# App info
app_info = InputAppInfo(
    app_name="Peppa",
    api_domain="http://localhost:5000",
    website_domain="http://localhost:5173",
)

# Framework
framework = 'django'

# Smtp config
gmailemail_config = SMTPSettings(
    host="smtp.gmail.com",
    port=465,
    from_=SMTPSettingsFrom(
        name="Peppa",
        email='peppasapp25@gmail.com',
    ),
    password='evjg umta keuy mewp',
    secure=True,
    username="peppasapp25@gmail.com"
)

smtp_settings = gmailemail_config

# DB URL
DATABASE_URL="postgresql://user:password@db:5432/mydatabase"


# Recipe list
recipe_list = [
    session.init(
        cookie_secure=False,
        cookie_same_site="lax",
        expose_access_token_to_frontend_in_cookie_based_auth=True
    ),
    emailverification.init(
        mode='OPTIONAL',
        email_delivery=EmailDeliveryConfig(
            override=custom_email_delivery,
            service=emailverification.SMTPService(
                smtp_settings=smtp_settings,
                override=custom_smtp_email_verification_content_override
           )
        )
    ),
    emailpassword.init(
        email_delivery=EmailDeliveryConfig(
            service=EPSMTPService(
                smtp_settings=smtp_settings,
                override=custom_smtp_reset_password_content_override
            )
        )
    ),
    dashboard.init(),
    userroles.init(),
]

