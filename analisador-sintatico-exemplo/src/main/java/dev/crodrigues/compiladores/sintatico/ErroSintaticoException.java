package dev.crodrigues.compiladores.sintatico;

import dev.crodrigues.compiladores.lexico.Token;

import java.util.Objects;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class ErroSintaticoException extends RuntimeException {

    private final Token.ClasseToken obtida;
    private final Token.ClasseToken[] esperadas;

    public ErroSintaticoException(Token.ClasseToken obtida, Token.ClasseToken ...esperadas) {
        this.obtida = obtida;
        this.esperadas = esperadas;
    }

    @Override
    public String getMessage() {
        String stringEsperadas = Stream
                .of(esperadas)
                .map(Objects::toString)
                .collect(Collectors.joining(", "));
        
        return "Classes esperadas: [" + stringEsperadas + "], obtida: " + obtida.toString();
    }
}
