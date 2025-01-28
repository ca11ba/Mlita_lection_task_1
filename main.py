
class Parser:
    def __init__(self, input_string):
        self.S_brackets = {'(', '['}
        self.string = input_string
        self.ch = None
        self.iterator = -1
        self.read()

    def read(self):
        self.iterator += 1
        if self.iterator >= len(self.string):
            self.ch = None
        else:
            self.ch = self.string[self.iterator]

    def run(self) -> bool:
        try:
            self.S()
            if self.iterator == len(self.string) and self.ch is None:
                return True
            else:
                return self.error()
        except ValueError as e:
            print(e)
            return False

    def S(self):
        if self.ch == '(':
            self.read()
            self.Q()
            if self.ch == ')':
                self.read()
            else: 
                self.error()
            self.S()
        if self.ch == '[':
            self.read()
            self.Q()
            if self.ch == ']':
                self.read()
            else:
                self.error() 
            self.S()

    def Q(self):
        if self.ch == ' ':
            self.read()
            self.P()
        elif self.ch == '(' or self.ch == '[':
            self.S()
        else: 
            self.error()

    def P(self):
        if self.ch == ' ':
            self.read()
            self.P()



    def error(self):
        raise ValueError("Получена ошибка!")


if __name__ == "__main__":
    print("Добро пожаловать!")
    print("- Введите exit для выхода из программы.")
    print()
    print("Введите правильное скобочное выражение, соответствующее следующему описанию:")
    print(""" Правильная скобочная запись с двумя видами скобок. Если внутри скобок нет ничего, то должен быть поставлен по крайней мере один пробел. В других местах пробелов не должно быть.
        Пример. 	Правильная запись: [( )([ ]([ ](  )( )))]
                    Неправильная запись [( )()][][()[]]""")
    print()

    while True:
        input_str = input("> ").strip()
        if input_str == "exit":
            break
        parser = Parser(input_str)
        if parser.run():
            print("Подходящее выражение")
            print()
        else:
            print("Выражение не подходит")
            print()
    print("Программа завершена!")
