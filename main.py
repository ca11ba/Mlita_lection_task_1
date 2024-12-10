class Parser:
    def __init__(self, s: str):
        self.s = s
        self.i = 0  # текущий индекс в строке

    def parse(self):
        # Проверяем, соответствует ли строка правилу S и что разобрали всю строку
        if not self.parse_S():
            return False
        return self.i == len(self.s)

    def parse_S(self):
        # S -> P S | P
        # Нужно разобрать хотя бы один P
        if not self.parse_P():
            return False
        # После одного P, если ещё есть символы, пытаемся разобрать ещё один P, и так далее
        while self.i < len(self.s):
            saved_i = self.i
            if not self.parse_P():
                self.i = saved_i
                break
        return True

    def parse_P(self):
        # P -> '(' Q ')' | '[' Q ']'
        if self.i >= len(self.s):
            return False
        c = self.s[self.i]
        if c == '(':
            self.i += 1
            if not self.parse_Q(')'):
                return False
            if self.i >= len(self.s) or self.s[self.i] != ')':
                return False
            self.i += 1
            return True
        elif c == '[':
            self.i += 1
            if not self.parse_Q(']'):
                return False
            if self.i >= len(self.s) or self.s[self.i] != ']':
                return False
            self.i += 1
            return True
        else:
            return False

    def parse_Q(self, closing):
        # Q -> R | SPACE+
        # Попытаемся сначала разобрать R (вложенные P без пробелов).
        saved_i = self.i
        if self.parse_R():
            # Успешно разобрали R
            return True
        # Не удалось R, откатим индекс
        self.i = saved_i

        # Пробуем разобрать SPACE+ (пустые скобки, но должны содержать пробел)
        if not self.parse_spaces():
            return False

        # После пробелов внутри скобок, чтобы это было корректно (пустые скобки),
        # сразу должен идти закрывающий символ.
        # Проверим, что следующий символ - закрывающая скобка будет проверен выше в parse_P
        # Здесь достаточно, чтобы не было других символов, кроме закрывающей скобки
        # Если текущий символ не закрывающая скобка (closing), значит неверно.
        if self.i < len(self.s) and self.s[self.i] == closing:
            return True
        else:
            return False

    def parse_R(self):
        # R -> P | P R
        # Должны разобрать хотя бы один P без пробелов внутри R
        # В R пробелы недопустимы.
        saved_i = self.i
        if not self.parse_P_for_R():
            return False
        # Если удалось P, пробуем продолжить разбирать R (ещё P подряд)
        while True:
            saved_i = self.i
            if not self.parse_P_for_R():
                self.i = saved_i
                break
        return True

    def parse_P_for_R(self):
        # Внутри R пробелы недопустимы. Если следующий символ пробел - сразу False.
        if self.i < len(self.s) and self.s[self.i] == ' ':
            return False
        return self.parse_P()

    def parse_spaces(self):
        # SPACE+ -> ' ' | ' ' SPACE+
        # Должен быть хотя бы один пробел
        if self.i >= len(self.s) or self.s[self.i] != ' ':
            return False
        self.i += 1
        # Читаем оставшиеся пробелы, если есть
        while self.i < len(self.s) and self.s[self.i] == ' ':
            self.i += 1
        return True

def check_brackets(s: str) -> bool:
    parser = Parser(s)
    return parser.parse()


# Примеры использования:

"""test_strings = [
     "[(          )([ ]([ ](  )(  )))]",     # Пример из условия
            "( )",                          # Одна пара круглых пустых скобок с пробелом
            "[ ]",                          # Одна пара квадратных пустых скобок с пробелом
            "([ ])",                        # Вложенные скобки: снаружи круглые, внутри квадратные пустые
            "(( ))",                        # Двойные круглые: внешние содержат пустые внутренние
            "[ ( ) [ ] ]",         # Должно быть False
]"""


#for ts in test_strings:
   # print(ts, "=>", check_brackets(ts))


if __name__ == "__main__":
    while True:
        print("Чтобы выйти из программы пропишите 'exit' после 'Введите скобочное выражение'")
        
        expression = input("Введите скобочное выражение: ")
        if expression == "exit":
            break
        print(expression, "=>", check_brackets(expression))