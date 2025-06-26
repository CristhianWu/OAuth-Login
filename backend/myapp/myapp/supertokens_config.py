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
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
)
from .custom_email.custom_delivery import (custom_verification_email_delivery,)
from .custom_email.custom_smtp import (custom_smtp_email_verification_content_override)
# Supertokens core
supertokens_config = SupertokensConfig(
    connection_uri="http://supertokens:3567",
    api_key="YOUR_API_KEY",
)

# App info
app_info = InputAppInfo(
    app_name="YOUR_APP_NAME",
    api_domain="http://localhost:8000",
    website_domain="http://localhost:8000", # Change to your frontend domain
)

# Framework
framework = 'django'

# Smtp config
gmailemail_config = SMTPSettings(
    host="YOUR_HOST",
    port=465,
    from_=SMTPSettingsFrom(
        name="YOUR_NAME",
        email='YOUR_EMAIL',
    ),
    password='YOUR_PASSWORD',
    secure=True,
    username="YOUR_USERNAME"
)

smtp_settings = gmailemail_config

# Recipe list
recipe_list = [
    session.init(
        cookie_secure=False,
        cookie_same_site="lax",
        expose_access_token_to_frontend_in_cookie_based_auth=True
    ),
    emailverification.init(
        mode='REQUIRED',
        email_delivery=EmailDeliveryConfig(
            override=custom_verification_email_delivery,
            service=emailverification.SMTPService(
                smtp_settings=smtp_settings,
                override=custom_smtp_email_verification_content_override
           )
        )
    ),
    emailpassword.init(),
    dashboard.init(),
    userroles.init(),
]

