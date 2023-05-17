package dev.crodrigues.compiladores.sintatico;

import dev.crodrigues.compiladores.lexico.AnalisadorLexico;
import dev.crodrigues.compiladores.lexico.Token;
import dev.crodrigues.compiladores.utils.StringUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.Objects;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Component
@RequiredArgsConstructor
@Slf4j
public class AnalisadorSintaticoInterpretador {

    private final AnalisadorLexico analisadorLexico;
    private String conteudoAtual;
    private Token tokenAtual;

    private int debugIdentacao = 0;

    public void analisar(String conteudo) {
        log.info("");
        log.info("");
        log.info("");
        conteudoAtual = conteudo;

        log.info("> analisar()");
        proximoToken();
        expressao();
        log.info("< analisar()");
    }

    private void expressao() {
        debugIdentacao++;
        log.info(StringUtils.indent("> expressao()", debugIdentacao));

        termo();
        if(testarClasse(Token.ClasseToken.OPERADOR_SOMA, Token.ClasseToken.OPERADOR_SUBTR)) {
            expressao();
        }

        debugIdentacao--;
        log.info(StringUtils.indent("< expressao()", debugIdentacao));
    }

    private void termo() {
        debugIdentacao++;
        log.info(StringUtils.indent("> termo()", debugIdentacao));

        fator();
        if(testarClasse(Token.ClasseToken.OPERADOR_MULTIPL, Token.ClasseToken.OPERADOR_DIV)) {
            termo();
        }

        debugIdentacao--;
        log.info(StringUtils.indent("< termo()", debugIdentacao));
    }

    private void fator() {
        debugIdentacao++;
        log.info(StringUtils.indent("> fator()", debugIdentacao));

        if(testarClasse(Token.ClasseToken.DELIM_ABRIR_PARENTESES)) {
            expressao();
            validarClasse(Token.ClasseToken.DELIM_FECHAR_PARENTESES);
        } else {
            validarClasse(Token.ClasseToken.CONST_NUMERICA);
        }

        debugIdentacao--;
        log.info(StringUtils.indent("< fator()", debugIdentacao));
    }

    private void proximoToken() {
        conteudoAtual = StringUtils.ltrim(conteudoAtual);
        tokenAtual = analisadorLexico.proximoToken(conteudoAtual);
        conteudoAtual = conteudoAtual.substring(tokenAtual.getTamanhoMatch());

        log.info(StringUtils.indent("- token obtido: {}", debugIdentacao), tokenAtual);
    }

    private boolean testarClasse(Token.ClasseToken ...classesToken) {
        String stringClasses = Stream
                .of(classesToken)
                .map(Objects::toString)
                .collect(Collectors.joining(", "));
        log.info(StringUtils.indent("? testando classes {} => {}", debugIdentacao), stringClasses, tokenAtual);

        boolean resultado = Stream
                .of(classesToken)
                .anyMatch(classeToken -> classeToken.equals(tokenAtual.getClasse()));

        if(resultado) {
            proximoToken();
        }

        return resultado;
    }

    private void validarClasse(Token.ClasseToken ...classesToken) {
        String stringClasses = Stream
                .of(classesToken)
                .map(Objects::toString)
                .collect(Collectors.joining(", "));
        log.info(StringUtils.indent("! validando classes {} => {}", debugIdentacao), stringClasses, tokenAtual);

        Stream
                .of(classesToken)
                .filter(classeToken -> classeToken.equals(tokenAtual.getClasse()))
                .findAny()
                .orElseThrow(() -> new ErroSintaticoException(tokenAtual.getClasse(), classesToken));

        proximoToken();
    }

}
