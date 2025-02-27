class FlowValidationError(ValueError):
    """
    Exception raised when a flow is invalid.
    """

    pass


class RegisterParentError(RuntimeError):
    """
    Exception raised when a parent is registered after the flow has been initialized.
    """

    pass
