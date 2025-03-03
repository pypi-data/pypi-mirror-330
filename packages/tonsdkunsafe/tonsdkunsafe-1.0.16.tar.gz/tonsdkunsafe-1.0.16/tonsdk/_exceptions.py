
class TonSdkException(Exception):
    """
    Base class for tonsdkunsafe exceptions.
    Subclasses should provide `.default_detail` properties.
    """
    default_detail = 'tonsdkunsafe error.'

    def __init__(self, detail=None):
        self.detail = self.default_detail if detail is None else detail

    def __str__(self):
        return str(self.detail)
