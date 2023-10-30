class RentNotFoundError(Exception):
    pass
    

class CanNotBeRentedError(Exception):
    def __init__(self, message="This item cannot be rented."):
        self.message = message
        super().__init__(self.message)

class InsufficientBalanceError(Exception):
    pass

class AlreadyEndedError(Exception):
    pass