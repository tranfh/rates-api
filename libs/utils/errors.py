class CustomError(Exception):
    """Base class for custom errors."""
    pass

class MultipleDaysInputError(CustomError):
    """Exception raised for errors in price arguments if more than one day.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Start and end date must be on the same day"):
        self.message = message
        super().__init__(self.message)

class MultipleRatesError(CustomError):
    """Exception raised for if more than one rate found for price interval

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Multiple rates found for price interval"):
        self.message = message
        super().__init__(self.message)