# 🖼️ Super Processador PBM

Um projeto em Python com Streamlit para manipulação de imagens no formato **PBM (Portable Bitmap)**, usando exclusivamente operações matriciais **puras** — sem bibliotecas externas como NumPy. Ideal para estudos de **álgebra linear**, **processamento de imagens** e manipulação de arquivos em **formato binário textual**.

---

## 🚀 Funcionalidades

O app permite:

### 📐 Operações Geométricas
- 🔄 **Transposição** da matriz (espelhamento diagonal)
- ↪️ **Rotação 90°, 180° e 270°**
- ↔️ **Inversão horizontal**
- ↕️ **Inversão vertical**

### 🔃 Permuta de Linhas e Colunas
- 🔁 Troca entre linhas simetricamente (ex: 1ª com a última, 2ª com penúltima, etc)
- 🔁 Troca entre colunas simetricamente

### 🧮 Operações Matemáticas
- 🌓 **Imagem negativa** (0 ↔ 1)
- 🔢 **Contagem de pixels brancos (valor 1)**
- ✖️ **Multiplicação por escalar**
- ➕ **Soma entre duas imagens PBM de mesma dimensão**

---

## 📥 Como usar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/super-processador-pbm.git
cd super-processador-pbm
```

### 2. Instale o Streamlit
```bash
pip install streamlit
```

### 3. Rode o projeto
```bash
streamlit run app.py
```

---

## 📁 Como preparar uma imagem `.pbm`

- O formato suportado é o **P1** (texto ASCII).
- Exemplo:
  ```
  P1
  5 5
  0 0 1 0 0
  0 1 1 1 0
  1 1 1 1 1
  0 1 1 1 0
  0 0 1 0 0
  ```

Você pode criar suas próprias imagens com qualquer editor de texto e salvar como `.pbm`.

---

## 🧠 Por trás do código

### 📌 Como o programa funciona:

1. **Leitura** do arquivo PBM manualmente (sem bibliotecas de imagem).
2. **Conversão** do conteúdo para uma matriz de inteiros.
3. Aplicação das operações via **manipulação direta de listas** (nada de `numpy`, `cv2`, etc).
4. Exibição e **download** do novo arquivo `.pbm` gerado com base na matriz modificada.

---

## 🛠️ O que foi evitado

- ❌ Não usa `numpy`
- ❌ Não usa `opencv`, `PIL` ou bibliotecas gráficas
- ✅ Apenas `Streamlit` e lógica com listas puras em Python

---

## ✨ Exemplos de uso

### 🔄 Rotação 90°:
```text
Antes:
1 0 0
1 1 0
1 0 1

Depois:
1 1 1
0 1 0
1 0 0
```

### ↔️ Inversão Horizontal:
```text
Antes:
0 1 0
1 0 1

Depois:
0 1 0
1 0 1
```

---

## 📌 Possíveis melhorias

- Suporte a imagens P4 (binário)
- Detecção visual com bibliotecas gráficas (opcional)
- Aplicações em filtros e reconhecimento de padrões

---

## 🤝 Contribuição

Sinta-se à vontade para abrir **pull requests**, propor melhorias ou reportar **issues**!

---

## 📜 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.