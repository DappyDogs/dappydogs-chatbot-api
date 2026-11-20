class ApplicationError(Exception):
    """Controlled failure that can be translated into a safe public response."""

    code = "application_error"
    public_message = "The operation could not be completed."
