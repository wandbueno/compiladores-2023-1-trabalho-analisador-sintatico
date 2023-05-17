# Exemplo de analisador sintático

Exemplo de analisador sintático desenvolvido em Java, com a framework Spring para cuidar das dependências

## Onde está a main?

O equivalente da main está na classe ```CommandLineTestRunner.java```.

Esta classe é gerenciada pelo Spring e é executada durante o início da aplicação, e desta forma funciona como se fosse uma main para nosso propósito.

## Como executar

Existem duas formas de executar este projeto, uma utilizando Docker, e a outra utilizando o Java instalado localmente na máquina:

Com Docker:
```sh
# O ponto no final é necessário
docker build -t analisador-sintatico .
docker run --rm analisador-sintatico
```

Sem Docker (necessário ter o Java 17 ou superior instalado localmente):
```sh
# No Linux
./gradlew bootRun

# No Windows
gradlew.bat bootRun
```
