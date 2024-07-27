class EmailType:
    USER_REGISTER_EMAIL = "USER_REGISTER_EMAIL"
    USER_FORGOT_PASSWORD_EMAIL = "USER_FORGOT_PASSWORD_EMAIL"


EMAIL_DATA = {
    "USER_REGISTER_EMAIL": {
        "html_template": "register.html",
        "subject": {
            "EN": "User registration",
        },
        "purpose": "confirm",
    },
    "USER_FORGOT_PASSWORD_EMAIL": {
        "html_template": "reset_password.html",
        "subject": {
            "EN": "Reset password",
        },
        "purpose": "reset-password",
    },
}
