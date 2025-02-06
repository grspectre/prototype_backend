def tokenize(expression):
    tokens = []
    number = ""
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isdigit() or char == '.':
            number += char
        else:
            if number:
                tokens.append(number)
                number = ""
            if char in "+-*/()":
                tokens.append(char)
            elif char.isspace():
                pass  # пропускаем пробелы
            else:
                raise ValueError(f"Недопустимый символ: {char}")
        i += 1
    if number:
        tokens.append(number)
    return tokens


def shunting_yard(tokens):
    out_queue = []
    op_stack = []
    
    # Определим приоритеты операторов (чем выше число, тем больше приоритет)
    prec = {'+':1, '-':1, '*':2, '/':2}
    
    for token in tokens:
        if token.replace('.', '', 1).isdigit():  # число (целое или с плавающей точкой)
            out_queue.append(token)
        elif token in prec:
            while op_stack and op_stack[-1] in prec and prec[op_stack[-1]] >= prec[token]:
                out_queue.append(op_stack.pop())
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            # Извлекаем операторы до встречной открывающей скобки
            while op_stack and op_stack[-1] != '(':
                out_queue.append(op_stack.pop())
            if not op_stack:
                raise ValueError("Не совпадают скобки")
            op_stack.pop()  # удаляем '('
        else:
            raise ValueError(f"Нераспознанный токен: {token}")
    
    while op_stack:
        if op_stack[-1] in '()':
            raise ValueError("Не совпадают скобки")
        out_queue.append(op_stack.pop())
        
    return out_queue


def evaluate_rpn(rpn_tokens):
    stack = []
    for token in rpn_tokens:
        if token.replace('.', '', 1).isdigit():
            stack.append(float(token))
        else:
            # Оператор: извлекаем два последних операнда
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b
            else:
                raise ValueError(f"Нераспознанный оператор: {token}")
            stack.append(result)
    if len(stack) != 1:
        raise ValueError("Ошибка вычисления")
    return stack[0]

if __name__ == "__main__":
    expr = "(2 + 3) * (4 - 1) / 5"
    tokens = tokenize(expr)
    print("Токены:", tokens)
    
    rpn = shunting_yard(tokens)
    print("ОПЗ:", rpn)
    
    result = evaluate_rpn(rpn)
    print("Результат:", result)