import re
from function import parse_code, program


def main():
    try:
        with open('teste/teste5.c', 'r', encoding='utf-8') as f:
            code = f.read()

        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
        code = re.sub(r'//\s*[^\n]*', '', code, flags=re.DOTALL)

        tokens = parse_code(code)
        # print("\n\n ||||||||||||||||| Análise sintática ||||||||||||||||| ")
        # for token in tokens:
        #     print(token)

        program()
        print("\nAnálise sintática concluída com sucesso!!!")

    except SyntaxError as e:
        print(f"{e}")
        return 1

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
