# const variable for command
class Commands:
    START = "/start"
    HELP = "/help"
    ABOUT = "/about"

    DATA_ENTRY = "/data_entry"
    CHAT_MODE = "/chat_mode"
    USER_PANEL = "/user_panel"

    LAST_REPORT = "/last_report"
    COUNT_REPORT = "/count_report"

    EXIT = "/exit"

class ValidateErrors:
    #title
    TITLE_ERROR = "invalid_title_length"
    TITLE_OK = "valid_title_length"

    #enum
    ENUM_ERROR = "invalid_not_in_enum:"
    ENUM_OK = "in_enum"

    #description
    DESCRIPTION_ERROR = "invalid_description_lengh"
    DESCRIPTION_OK = "valid_description_lengh"

    #empty
    EMPTY_ERROR = "empty_text"

    #onlu num
    ISDIGIT_ERROR = "only_number_text"