class ApplicationError(Exception):
    """Controlled failure that can be translated into a safe public response."""

    code = "application_error"
    public_message = "The operation could not be completed."


class AuthenticationRequiredError(ApplicationError):
    code = "authentication_required"
    public_message = "Authentication evidence is required."


class InvalidAuthenticationError(ApplicationError):
    code = "invalid_authentication"
    public_message = "Authentication evidence is invalid."


class AuthenticationConfigurationError(ApplicationError):
    code = "authentication_unavailable"
    public_message = "Authentication is temporarily unavailable."
