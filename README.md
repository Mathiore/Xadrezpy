# ♟ Xadrez em Python com GUI e IA

Um jogo de xadrez com interface gráfica feita em `pygame`, com modo de dois jogadores ou contra uma IA básica. Inclui mini tabuleiros para visualização das jogadas.

## 🧠 Funcionalidades

* 🎮 Modo Player vs Player
* 🧠 Modo Player vs IA
* 📄 Regras oficiais das peças implementadas
* 🔍 Destaca jogadas possíveis ao clicar em uma peça
* 👑 Vitória ao capturar o Rei adversário
* ⟳ Reiniciar jogo após vitória
* 🔹 Mini tabuleiros com dicas para os dois jogadores

## 💡 Como usar

### 1. Requisitos

* Python 3.7+
* pygame

Instale o pygame:

```bash
pip install pygame
```

### 2. Estrutura esperada

Crie uma pasta chamada `pieces/` contendo as imagens `.png` das peças com os seguintes nomes:

```
pieces/
├── wp.png  # White Pawn
├── wr.png  # White Rook
├── wn.png  # White Knight
├── wb.png  # White Bishop
├── wq.png  # White Queen
├── wk.png  # White King
├── bp.png  # Black Pawn
├── br.png  # Black Rook
├── bn.png  # Black Knight
├── bb.png  # Black Bishop
├── bq.png  # Black Queen
├── bk.png  # Black King
```

### 3. Executando o jogo

Execute o script Python:

```bash
python nome_do_arquivo.py
```

> Substitua `nome_do_arquivo.py` pelo nome do arquivo .py principal

### 4. Menu de jogo

Ao iniciar, você pode escolher:

* 👥 Player vs Player
* 🧠 Player vs IA

## 🎯 Objetivo

Capturar o rei adversário! A IA vai tentar defender seu próprio rei e capturar o seu.

## 🧠 Como a IA funciona

A IA analisa:

* Se pode capturar o rei inimigo, ela o faz.
* Se pode capturar qualquer peça, ela o faz.
* Caso contrário, faz uma jogada válida aleatória.

## 🔹 Recursos extras

* Mini tabuleiros mostram sugestões de jogadas para as cores preta e branca.
* Interface com `pygame` e caixas de diálogo com `tkinter`.
  (Não está funcional ainda, falta implementar)

🌐 Desenvolvido com ❤️ usando Python + Pygame
