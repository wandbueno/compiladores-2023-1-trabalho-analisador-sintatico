package dev.crodrigues.compiladores.lexico.regra;

import dev.crodrigues.compiladores.lexico.Token;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
public class RegraDelimFecharParenteses implements Regra {

    @Override
    public List<Pattern> regras() {
        return List.of(
                Pattern.compile("^\\)")
        );
    }

    @Override
    public Token criarToken(Matcher matcher) {
        return Token
                .builder()
                .classe(Token.ClasseToken.DELIM_FECHAR_PARENTESES)
                .tamanhoMatch(matcher.end())
                .build();
    }

}
