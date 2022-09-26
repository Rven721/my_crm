# thousand separator

def get_nubmer_with_serparaes(number):
    """The function will take a number and return it splited by thousands sting"""
    before_coma = str(number // 1).split(".", maxsplit=1)[0]
    after_coma = str(round(number % 1, 2)).split(".", maxsplit=1)[-1]
    if len(after_coma) < 2:
        after_coma += "0"
    count = 0
    res = ""
    for integer in before_coma[::-1]:
        res += integer
        count += 1
        if count % 3 == 0:
            res += " "
    output = f"{res[::-1]} руб. {after_coma} коп."
    return output
