class RateLimitExceeded(Exception):
    """Привышен лимит вызовов."""
    def __init__(self, message):
        self.message = message
        super().__init__(message)