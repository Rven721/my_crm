"""Small imitation of calculatior work"""


def check_the_expression(expression):
    """Проверит содержит ли строка тоьлько разрешенные символы"""
    allowd_simpols = ('-+/*')
    slog_count = 0
    sig_index = None
    for index, value in enumerate(expression):
        if not isinstance(value, float):
            if value not in allowd_simpols or sig_index == index - 1:
                return False
            else:
                sig_index = index
        slog_count += 1
    if slog_count == 0:
        return False
    return True


def check_parenthes(expression):
    """Проверить совпадает ли число скобок в примере"""
    if '(' in expression or ')' in expression:
        if expression.count(')') == expression.count('('):
            return True
    return False


def find_parenthes(expression):
    """Вернет содержимое в скобках"""
    par_start = None
    for index, value in enumerate(expression):
        if value == '(':
            par_start = index
    par_end = expression.find(')', par_start)
    return (par_start, par_end, expression[par_start + 1:par_end])


def resolve_parenthes(expression):
    """Решит выражение в скобках"""
    par_start, par_end, cur_expression = find_parenthes(expression)
    if cur_expression:
        res = make_calculations(cur_expression)
        expression = expression[:par_start] + str(res[0]) + expression[par_end + 1:]
    else:
        expression = expression[:par_start] + expression[par_end + 1:]
    return expression


def parce_the_expression(expression):
    """Вернет выражение в виде списка, что бы было проще проводить расчеты"""
    expression = expression.replace(',', '.')
    signs = ('+-*/')
    result = []
    i = 0
    while i < len(expression):
        if expression[i] in signs:
            try:
                first_part = float(expression[:i].strip())
            except ValueError:
                first_part = expression[:i].strip()
            sig = expression[i]
            result.append(first_part)
            result.append(sig)
            expression = expression[i + 1:].strip()
            i = 0
        else:
            i += 1
    try:
        result.append(float(expression))
    except ValueError:
        result.append(expression)
    return result


def make_primary_actions(expression):
    """Выполнит действия первого порядка и вернет оставшиеся выражение"""
    i = 0
    while i < len(expression):
        if expression[i] == '*':
            res = expression[i - 1] * expression[i + 1]
            expression = expression[:i - 1] + [res] + expression[i + 2:]
            i = 0
        elif expression[i] == "/":
            res = expression[i - 1] / expression[i + 1]
            expression[i] = res
            expression = expression[:i - 1] + [float(res)] + expression[i + 2:]
            i = 0
        else:
            i += 1
    return expression


def make_secondery_actions(expression):
    """Выполнит действия второго порядка и вернет оставшиеся выражение"""
    i = 0
    while i < len(expression):
        if expression[i] == '-':
            res = expression[i - 1] - expression[i + 1]
            expression = expression[:i - 1] + [res] + expression[i + 2:]
            i = 0
        elif expression[i] == "+":
            res = expression[i - 1] + expression[i + 1]
            expression[i] = res
            expression = expression[:i - 1] + [float(res)] + expression[i + 2:]
            i = 0
        else:
            i += 1
    return expression


def make_calculations(expression):
    """Вернет результат калькуляции"""
    while check_parenthes(expression):
        expression = resolve_parenthes(expression)
    expression = parce_the_expression(expression)
    if not check_the_expression(expression):
        return False
    while '*' in expression or '/' in expression:
        expression = make_primary_actions(expression)
    while '-' in expression or '+' in expression:
        expression = make_secondery_actions(expression)
    if int(expression[0]) < 0:
        return False
    return expression
