"""will standartize raw phone number"""


def get_standart_phone(raw_number: str) -> str:
    """will standartize raw phone number"""
    allowd_symbols = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+")
    phone_dict = {}
    cleared_number = [char for char in raw_number if char in allowd_symbols]
    if len(cleared_number) == 10 and cleared_number[0] == "9":
        cleared_number = cleared_number[1:]
    elif len(cleared_number) == 11 and ''.join(cleared_number[:2]) in ["89", "79"]:
        cleared_number = cleared_number[2:]
    elif len(cleared_number) == 12 and ''.join(cleared_number[:3]) == "+79":
        cleared_number = cleared_number[3:]
    else:
        return False
    phone_dict['code'] = ''.join(cleared_number[:2])
    phone_dict['p1'] = ''.join(cleared_number[2:5])
    phone_dict['p2'] = ''.join(cleared_number[5:7])
    phone_dict['p3'] = ''.join(cleared_number[7:])
    phone_number = f"8 (9{phone_dict['code']}) {phone_dict['p1']}-{phone_dict['p2']}-{phone_dict['p3']}"
    return phone_number
