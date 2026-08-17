from core.enums import ValidatesOutput , ExperienceCategory
from functools import wraps
from .constants import ValidateErrors
def validations(func):
    """this decorator check validate status

    Args:
        func (function): deacorate func

    Returns:
        ValidatesOutput: state and message
    """    
    @wraps(func)
    def wrapper (text : str , *args , **kwargs) -> ValidatesOutput:
        text = text.strip().lower()

        # general conditions
        if not text or len(text) < 2:
            return ValidatesOutput(message=ValidateErrors.EMPTY_ERROR)

        if text.isdigit():
            return ValidatesOutput(message=ValidateErrors.ISDIGIT_ERROR)

        # special conditions
        status, message= func(text , *args , **kwargs)

        return ValidatesOutput(message=message,status=status)
    
    return wrapper

@validations
def validate_title_data(text:str) -> ValidatesOutput :
    status = 3 < len(text) < 20

    if status:
        message = ValidateErrors.TITLE_OK
    else:
        message = ValidateErrors.TITLE_ERROR

    return status, message

@validations
def validate_enum_items(text:str , enum) -> ValidatesOutput:
    status = text in [num.value.lower() for num in enum ]

    if status:
        message = ValidateErrors.ENUM_OK
    else:
        message = f"{ValidateErrors.ENUM_ERROR}{enum.__name__}"

    return status, message 

@validations
def validate_description(text:str) -> ValidatesOutput :
    status = 30 < len(text) < 1000 

    if status:
        message = ValidateErrors.DESCRIPTION_OK
    else :
        message = ValidateErrors.DESCRIPTION_ERROR

    return status, message 

def get_validation_message(error: str | None) -> str | None:

    messages = {
        ValidateErrors.TITLE_ERROR:
            "عنوان باید بین ۴ تا ۲۰ کاراکتر باشد.",

        ValidateErrors.DESCRIPTION_ERROR:
            "توضیحات باید بین ۳۰ تا ۱۰۰۰ کاراکتر باشد.",

        ValidateErrors.EMPTY_ERROR:
            "متن نمی‌تواند خالی باشد.",

        ValidateErrors.ISDIGIT_ERROR:
            "متن نمی‌تواند فقط شامل عدد باشد.",

    }

    if error is None:
        return None

    if error.startswith(ValidateErrors.ENUM_ERROR):
        return "گزینه انتخاب‌شده معتبر نیست."

    return messages.get(error)