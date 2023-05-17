package dev.crodrigues.compiladores.lexico;

import dev.crodrigues.compiladores.lexico.regra.Regra;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;

@Component
@RequiredArgsConstructor
public class AnalisadorLexico {

    private final List<Regra> regras;

    public Token proximoToken(String conteudo) {
        if(conteudo.isBlank()) {
            return Token
                    .builder()
                    .classe(Token.ClasseToken.FIM_ARQUIVO)
                    .tamanhoMatch(0)
                    .build();
        }

        return regras
                .stream()
                .map(regra -> regra.tokenizar(conteudo))
                .flatMap(Optional::stream)
                .findFirst()
                .orElseThrow(ErroLexicoException::new);

    }

}
