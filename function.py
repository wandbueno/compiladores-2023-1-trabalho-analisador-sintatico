import re
import sys
from enum import Enum
from dataclasses import dataclass


class TokenClass(Enum):
    PONTO_FLUTUANTE = r"\d+\.\d+"
    CONSTANTE_INTEIRA = r"\b\d+\b"
    PALAVRA_RESERVADA = r"\b(struct|if|int|else|while|do|for|float|double|char|long|short|break|continue|case|switch|default|void|return|print|nil|fun|var)\b"
    OPERADOR = r"(<|>|=|==|!=|<=|>=|\|\||&&|\+=|-=|\*=|-=|--|\+\+|\+|\/|->|\*|-|\||!|&|%|and|or)"
    DELIMITADOR = r"[\[\](){};,]"
    CONSTANTE_TEXTO = r'"[^"]*"'
    IDENTIFICADOR = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"


token_index = 0
previous_token = None


@dataclass
class Token:
    token_class: TokenClass
    lexeme: str
    line: int
    column: int

    def __str__(self):
        return f'<{self.token_class.name}> {self.lexeme}'


def parse_code(code):
    global tokens
    lines = code.split('\n')
    tokens = []
    line_num = 1

    for line in lines:
        line = re.sub(r'\s+', ' ', line.strip())
        column = 1

        while line:
            match = None
            for token_class in TokenClass:
                regex = token_class.value
                match = re.match(regex, line)
                if match:
                    lexeme = match.group(0)
                    token = Token(token_class, lexeme, line_num, column)
                    tokens.append(token)
                    line = line[len(lexeme):].lstrip()
                    column += len(lexeme)
                    break

            if match is None:
                raise SyntaxError(
                    f"Erro léxico na linha {line_num}, coluna {column}: caractere inesperado: {line[0]!r}")

        line_num += 1

    return tokens


def error(message, token=None):
    if token:
        message += f", na linha {token.line}, coluna {token.column}"
    else:
        message += " no final do arquivo"
    raise SyntaxError(message)


def program():
    global token_index, tokens
    token_index = 0
    while not end_of_file():
        declaration()
    if not end_of_file():
        error("Unexpected token", tokens[token_index])


def declaration():
    if check(TokenClass.PALAVRA_RESERVADA, "fun"):
        funDecl()
    elif check(TokenClass.PALAVRA_RESERVADA, "var"):
        varDecl()
    else:
        statement()


def funDecl():
    match(TokenClass.PALAVRA_RESERVADA, "fun")
    function()


def varDecl():
    match(TokenClass.PALAVRA_RESERVADA, "var")
    match(TokenClass.IDENTIFICADOR)
    if check(TokenClass.OPERADOR, "="):
        match(TokenClass.OPERADOR, "=")
        expression()
    match(TokenClass.DELIMITADOR, ";")


def statement():
    if check(TokenClass.PALAVRA_RESERVADA, "print"):
        printStmt()
    elif check(TokenClass.PALAVRA_RESERVADA, "if"):
        ifStmt()
    elif check(TokenClass.PALAVRA_RESERVADA, "for"):
        forStmt()
    elif check(TokenClass.PALAVRA_RESERVADA, "return"):
        returnStmt()
    elif check(TokenClass.PALAVRA_RESERVADA, "while"):
        whileStmt()
    elif check(TokenClass.DELIMITADOR, "{"):
        block()
    else:
        exprStmt()


def ifStmt():
    match(TokenClass.PALAVRA_RESERVADA, "if")
    match(TokenClass.DELIMITADOR, "(")
    expression()
    match(TokenClass.DELIMITADOR, ")")
    statement()
    if check(TokenClass.PALAVRA_RESERVADA, "else"):
        match(TokenClass.PALAVRA_RESERVADA, "else")
        statement()


def printStmt():
    match(TokenClass.PALAVRA_RESERVADA, "print")
    expression()
    match(TokenClass.DELIMITADOR, ";")


def returnStmt():
    match(TokenClass.PALAVRA_RESERVADA, "return")
    if not check(TokenClass.DELIMITADOR, ";"):
        expression()
    match(TokenClass.DELIMITADOR, ";")


def forStmt():
    match(TokenClass.PALAVRA_RESERVADA, "for")
    match(TokenClass.DELIMITADOR, "(")
    expression()
    match(TokenClass.DELIMITADOR, ";")
    expression()
    match(TokenClass.DELIMITADOR, ";")
    expression()
    match(TokenClass.DELIMITADOR, ")")
    statement()


def whileStmt():
    match(TokenClass.PALAVRA_RESERVADA, "while")
    match(TokenClass.DELIMITADOR, "(")
    expression()
    match(TokenClass.DELIMITADOR, ")")
    statement()


def block():
    match(TokenClass.DELIMITADOR, "{")
    while not check(TokenClass.DELIMITADOR, "}") and not end_of_file():
        declaration()
    match(TokenClass.DELIMITADOR, "}")


def exprStmt():
    expression()
    match(TokenClass.DELIMITADOR, ";")


def expression():
    assignment()


def assignment():
    if check(TokenClass.IDENTIFICADOR):
        match(TokenClass.IDENTIFICADOR)
        if check(TokenClass.OPERADOR, "="):
            match(TokenClass.OPERADOR, "=")
            assignment()
        else:
            # função para voltar 1 token
            prev_token()
            logic_or()
    else:
        logic_or()


def logic_or():
    logic_and()
    while check(TokenClass.OPERADOR, "or"):
        match(TokenClass.OPERADOR, "or")
        logic_and()


def logic_and():
    equality()
    while check(TokenClass.OPERADOR, "and"):
        match(TokenClass.OPERADOR, "and")
        equality()


def equality():
    comparison()
    while check(TokenClass.OPERADOR, ["!=", "=="]):
        match(TokenClass.OPERADOR)
        comparison()


def comparison():
    term()
    while check(TokenClass.OPERADOR) and tokens[token_index].lexeme in ["<", ">", "<=", ">="]:
        next_token()
        term()


def term():
    factor()
    while True:
        if check(TokenClass.OPERADOR, "+"):
            match(TokenClass.OPERADOR, "+")
            factor()
        elif check(TokenClass.OPERADOR, "-"):
            match(TokenClass.OPERADOR, "-")
            factor()
        else:
            break


def factor():
    unary()
    while check(TokenClass.OPERADOR, "/") or check(TokenClass.OPERADOR, "*"):
        match(TokenClass.OPERADOR)
        unary()


def unary():
    if check(TokenClass.OPERADOR, "!") or check(TokenClass.OPERADOR, "-"):
        match(TokenClass.OPERADOR)
        unary()
    else:
        call()


def call():
    primary()
    while check(TokenClass.DELIMITADOR, "(") or check(TokenClass.DELIMITADOR, "."):
        if check(TokenClass.DELIMITADOR, "("):
            match(TokenClass.DELIMITADOR, "(")
            arguments()
            match(TokenClass.DELIMITADOR, ")")
        elif check(TokenClass.DELIMITADOR, "."):
            match(TokenClass.DELIMITADOR, ".")
            match(TokenClass.IDENTIFICADOR)


def primary():
    if check(TokenClass.PALAVRA_RESERVADA, "true") or \
       check(TokenClass.PALAVRA_RESERVADA, "false") or \
       check(TokenClass.PALAVRA_RESERVADA, "nil") or \
       check(TokenClass.PALAVRA_RESERVADA, "this") or \
       check(TokenClass.CONSTANTE_INTEIRA) or \
       check(TokenClass.CONSTANTE_TEXTO) or \
       check(TokenClass.IDENTIFICADOR):
        next_token()
    elif check(TokenClass.PALAVRA_RESERVADA, "super"):
        match(TokenClass.PALAVRA_RESERVADA, "super")
        match(TokenClass.DELIMITADOR, ".")
        match(TokenClass.IDENTIFICADOR)
    elif check(TokenClass.DELIMITADOR, "("):
        match(TokenClass.DELIMITADOR, "(")
        expression()
        match(TokenClass.DELIMITADOR, ")")
    else:
        token = None if end_of_file() else tokens[token_index]
        raise SyntaxError(
            f"\nToken inesperado na expressão primária: {token.token_class.name} {token.lexeme}, linha {token.line}, coluna {token.column}")


def function():
    match(TokenClass.IDENTIFICADOR)
    match(TokenClass.DELIMITADOR, '(')
    if check(TokenClass.IDENTIFICADOR):
        parameters()
    match(TokenClass.DELIMITADOR, ')')
    block()


def parameters():
    match(TokenClass.IDENTIFICADOR)
    while check(TokenClass.DELIMITADOR, ","):
        match(TokenClass.DELIMITADOR, ",")
        match(TokenClass.IDENTIFICADOR)


def arguments():
    expression()
    while check(TokenClass.DELIMITADOR, ","):
        match(TokenClass.DELIMITADOR, ",")
        expression()


# FUNÇÕES AUXILIARES ***************************

def end_of_file():
    global tokens, token_index
    return token_index >= len(tokens)


def check(expected_class, expected_value=None):
    global tokens, token_index
    if not end_of_file():
        token = tokens[token_index]
        if token.token_class == expected_class and (expected_value is None or token.lexeme == expected_value):
            return True
    return False


def match(expected_token_class, expected_token_value=None, function_name=None):
    global previous_token
    if not check(expected_token_class, expected_token_value):
        token = None if end_of_file() else tokens[token_index]
        expected_value_str = expected_token_value if expected_token_value is not None else "None"
        found_token_class_str = token.token_class.name if token is not None else "None"
        found_lexeme_str = token.lexeme if token is not None else "None"
        function_name_str = f" na função {function_name}" if function_name is not None else ""
        error_message = f"\nErro de análise sintática: Esperado {expected_token_class.name} {expected_value_str}, encontrado {found_token_class_str} {found_lexeme_str}{function_name_str}"
        error(error_message, token)
    else:
        previous_token = tokens[token_index]
        next_token()


def next_token():
    global token_index, tokens

    if not end_of_file():
        token = tokens[token_index]
        print(f"Token atual: {token}")
        token_index += 1
        return token
    else:
        return None


def prev_token():
    global token_index, previous_token
    if token_index > 0:
        token_index -= 1
        previous_token = tokens[token_index]
        return tokens[token_index]
