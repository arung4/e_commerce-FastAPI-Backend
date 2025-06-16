from fastapi import HTTPException, status


# Authentication exceptions 

class UserAlreadyExistsException(HTTPException):

    def __init__(self,detail: str = "User with this email already exists"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UserNotExistsException(HTTPException):

    def __init__(self, detail: str = "User not exist with this email"):
        super.__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UserNotAllowedException(HTTPException): 

    def __init__(self, detail : str = "User not Allowed"):
        super.__init__(status_code = status.HTTP_401_UNAUTHORIZED, detail=detail)

class UserNotFoundException(HTTPException):
       def __init__(self, detail : str = "User not found, Not Authenticated"):
        super.__init__(status_code = status.HTTP_404_NOT_FOUND, detail=detail)



# Product Exceptions 


class ProductNotFoundException(HTTPException):
    def __init__(self, detail: str = "Product not found"):
        super().__init__(status_code=404, detail=detail)

    
class ProductAlreadyExistsException(HTTPException):

    def __init__(self,detail: str = ""):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)



# Cart Exceptions 

class AdminNotAllowedException(HTTPException):
    
    def __init__(self, detail : str = "Admin not Allowed"):
        super.__init__(status_code = status.HTTP_401_UNAUTHORIZED, detail=detail)

class ProductNotFoundCartException(HTTPException):
     def __init__(self, detail : str = "Product not found in cart"):
        super.__init__(status_code = status.HTTP_404_NOT_FOUND, detail=detail)


# Order Exception 

class OrderNotFoundException(HTTPException):
     def __init__(self, detail : str = "Order not found"):
        super.__init__(status_code = status.HTTP_404_NOT_FOUND, detail=detail)
