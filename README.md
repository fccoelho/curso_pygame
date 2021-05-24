# Curso de Programação de Jogos com Pygame
Criando um jogo de naves espaciais com Pygame. Para iniciantes em Python

## Pré-requisitos
Antes de começar este curso você precisa ter instalado em seu computador o git (com o qual irá clonar este repositório) e o pygame

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

## Fase 3
Nesta fase vamos adicionar a Nave.

```bash
git checkout Fase_3
```
Para isso, vamos criar mais [um módulo](/coronashooter/elementos.py) como uma classe de base para qualquer `sprite` do jogo.

Em seguida iremos criar uma classe para a Nave do jogador e outra para as naves inimigas.

Ao final desta fase poderemos ver as naves na tela.

## Fase 4
Nesta fase vamos adicionar movimento às naves. Neste processo vamos adicionar também algumas coisas a mais, como a geração de novos virus, controle movimentos da nave do jogador, outras coisas a mais. 

Veja como o jogo ficou.
```bash
git checkout Fase_4
```

## Fase 5
Na fase 5 vamos adicionar tiros e colisões para completar o Jogo.

Os tiros serão implementados como uma classe. Também foram implementados pontuação e passagem de fases pelo jogador.

# Possibilidades de melhoria.
Após estas cinco fases de desenvolvimento, temos um jogo funcional. Mas ainda existem muitas possibilidades de melhorias. Na lista abaixo temos algumas sugestões, mas use a sua criatividade e pense em novas maneiras de incrementar o jogo básico.

- Adicional mostradores de pontos, nível e fase;
- Trocar tela de fundo, quando passa de nível;  
- Otimizar a [velocidade de atualização da tela](https://coderslegacy.com/improving-speed-performance-in-pygame/);
- Adicionar outros elementos ao jogo, como Diferentes tipos de vacina e variantes do vírus, mais resistentes a um tipo de vacina.
- Adicionar nível(is) chefão.
- Adicionar trilha sonora e efeitos sonoros
- Adicionar efeitos de explosão
- etc.
