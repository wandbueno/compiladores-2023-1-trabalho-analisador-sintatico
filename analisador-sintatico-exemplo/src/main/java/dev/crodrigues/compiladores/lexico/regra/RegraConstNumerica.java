package dev.crodrigues.compiladores.lexico.regra;

import dev.crodrigues.compiladores.lexico.Token;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
public class RegraConstNumerica implements Regra {

    @Override
    public List<Pattern> regras() {
        return List.of(
                Pattern.compile("^[0-9]+")
        );
    }

    @Override
    public Token criarToken(Matcher matcher) {
        return Token
                .builder()
                .classe(Token.ClasseToken.CONST_NUMERICA)
                .lexema(matcher.group())
                .tamanhoMatch(matcher.end())
                .build();
    }

}
