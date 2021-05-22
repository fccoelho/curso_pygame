# Curso de Programação de Jogos com Pygame
Criando um jogo de naves espaciais com Pygame. Para iniciantes em Python

## Pré-requisitos
Antes de começar este curso você precisa ter instalado em seu computador o git (com o qual irá clora este repositório) e o pygame

```bash
pip install pygame
```

## Acompanhando o curso

Para acompanhar o curso vamos usar `tags` do git para ir migrando o código através das várias etapas de desenvolvimento. Então antes de começar certifique-se de que todas as tags estão atualizadas em seu clone:

```bash
git fetch --all --tags
```
# O Jogo
O jogo que iremos criar chama-se "Corona Shooter". e trata-se de um jogo de naves espaciais inspirado em uma pandemia de coronavirus.

## Fase 0
Na fase 0 começamos a organizar basicamente o nosso código. Para viajar no tempo até a faso 0 use o seguinte comando:

```bash
git checkout Fase_0
```
Nesta fase criamos a estrutura básica do projeto e cria o módulo principal do jogo.

O módulo principal se chama [main.py](/coronashooter/main.py) e fica no diretório coronashooter.

Também criamos um arquivo de texto na raiz do nosso projeto, chamado de [requirements.txt](/requirements.txt) onde vamos listar todas as bibliotecas necessárias para o nosso jogo.

Nesta fase, se executado, o módulo `main.py` apenas apresenta uma janela escura.

## Fase 1
Na fase 1 vamos usar uma classe para organizar a inicialização e os parâmetros do nosso jogo. Vamos também criar um módulo adicional para cuidar da especificação do plano de fundo do jogo.

```bash
git checkout Fase_1
```

Ao final desta fase temos nosso plano de fundo rolando de cima para baixo no nosso jogo. Para isso também adicionamos uma imagem de fundo a um diretório de imagens onde iremos manter todos os elementos gráficos do nosso projeto. 

## Fase 2
Nesta fase iremos adicionar outros controles ao jogo.
```bash
git checkout Fase_2
```
Nesta fase movemos o tratamento de eventos para um método separado, e configuramos a tecla `ESC` como tecla de sair do jogo.
