import interpreter


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue

        interpret = interpreter.Interpreter(text)
        result = interpret.expression()
        print(result)


if __name__ == '__main__':
    main()
