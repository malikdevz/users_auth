import re
#import phonenumbers
#from phonenumbers import NumberParseException

BASE_URL="http:/127.0.0.1:8000"
DEFAULT_FEMALE_PIC=BASE_URL+"/media/user-female-icon.png"
DEFAULT_MALE_PIC=BASE_URL+"/media/user-male-icon.png"
API_URL=BASE_URL+"/users/api/"
ACTIVATION_LINK=BASE_URL+"/activate_accnt/"


def is_lower_letters_only(text):
	return bool(re.fullmatch(r"[a-z]+",text))

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


"""def is_phone_number_valid(numero):
    try:
        parsed = phonenumbers.parse(numero, None)  # None = auto, lit l'indicatif
        return phonenumbers.is_valid_number(parsed)
    except NumberParseException:
        return False"""

"""def is_phone_number_valid(numero: str) -> bool:
    try:
        parsed = phonenumbers.parse(numero, None)
        return (
            phonenumbers.is_possible_number(parsed) and
            phonenumbers.is_valid_number(parsed)
        )
    except:
        return False"""
