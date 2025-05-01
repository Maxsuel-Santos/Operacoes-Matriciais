import streamlit as st

def ler_pbm(conteudo):
    linhas = [linha.strip() for linha in conteudo.split('\n') 
             if linha.strip() and not linha.startswith('#')]
    if not linhas or linhas[0] != 'P1':
        st.error("Formato PBM inválido. Deve começar com P1.")
        return None
    largura, altura = map(int, linhas[1].split())
    dados = ' '.join(linhas[2:]).split()
    return [[int(dados[i*largura + j]) for j in range(largura)] for i in range(altura)]

def matriz_para_pbm(matriz):
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0
    return f"P1\n{largura} {altura}\n" + '\n'.join(' '.join(map(str, linha)) for linha in matriz)

# Operações Geométricas
def transposta(matriz):
    return [[linha[i] for linha in matriz] for i in range(len(matriz[0]))]

def rotacionar_90(matriz):
    return [list(linha)[::-1] for linha in zip(*matriz)]

def rotacionar_180(matriz):
    return [linha[::-1] for linha in matriz[::-1]]

def rotacionar_270(matriz):
    return [list(linha) for linha in zip(*matriz)][::-1]

def inverter_horizontal(matriz):
    return [linha[::-1] for linha in matriz]

def inverter_vertical(matriz):
    return matriz[::-1]

# Operações de Permuta Dinâmicas
def trocar_linhas(matriz, i, j):
    matriz[i], matriz[j] = matriz[j], matriz[i]
    return matriz

def trocar_colunas(matriz, i, j):
    return [[linha[i] if k == j else linha[j] if k == i else linha[k] 
            for k in range(len(linha))] for linha in matriz]

def gerar_opcoes_permuta(tamanho, tipo):
    return [f"Trocar {tipo} {i+1}ª e {tamanho-i}ª" for i in range(tamanho//2)]

# Operações Matemáticas
def somar_matrizes(m1, m2):
    return [[m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]

def multiplicar_escalar(matriz, escalar):
    return [[pixel * escalar for pixel in linha] for linha in matriz]

def negativa(matriz):
    return [[1 - pixel for pixel in linha] for linha in matriz]

def contar_uns(matriz):
    return sum(sum(linha) for linha in matriz)

def main():
    st.title("Super Processador PBM")
    
    arquivo = st.file_uploader("Envie seu arquivo PBM", type="pbm")
    
    if arquivo:
        matriz = ler_pbm(arquivo.read().decode('utf-8'))
        if matriz:
            altura = len(matriz)
            largura = len(matriz[0]) if altura > 0 else 0
            
            # Mostra a matriz original imediatamente após o upload
            st.subheader("Matriz Original")
            st.text(f"Dimensões: {largura}x{altura}")
            st.text('\n'.join(' '.join(str(x) for x in linha) for linha in matriz))
            st.write("---")  # Linha divisória
            
            tab1, tab2, tab3 = st.tabs(["Operações Geométricas", "Permutas", "Operações Matemáticas"])
            
            with tab1:
                op_geo = st.selectbox("Selecione:", [
                    "Nenhuma", "Transposta", "Rotacionar 90°", "Rotacionar 180°", 
                    "Rotacionar 270°", "Inverter Horizontal", "Inverter Vertical"
                ], key="geo")
                
                if op_geo == "Transposta":
                    resultado = transposta(matriz)
                elif op_geo == "Rotacionar 90°":
                    resultado = rotacionar_90(matriz)
                elif op_geo == "Rotacionar 180°":
                    resultado = rotacionar_180(matriz)
                elif op_geo == "Rotacionar 270°":
                    resultado = rotacionar_270(matriz)
                elif op_geo == "Inverter Horizontal":
                    resultado = inverter_horizontal(matriz)
                elif op_geo == "Inverter Vertical":
                    resultado = inverter_vertical(matriz)
            
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    opcoes_linhas = ["Nenhuma"] + gerar_opcoes_permuta(altura, "linha")
                    op_linha = st.selectbox("Linhas:", opcoes_linhas, key="linha")
                
                with col2:
                    opcoes_colunas = ["Nenhuma"] + gerar_opcoes_permuta(largura, "coluna")
                    op_coluna = st.selectbox("Colunas:", opcoes_colunas, key="coluna")
                
                resultado = None
                if op_linha != "Nenhuma":
                    idx = opcoes_linhas.index(op_linha) - 1
                    resultado = trocar_linhas(matriz, idx, altura - 1 - idx)
                
                if op_coluna != "Nenhuma":
                    idx = opcoes_colunas.index(op_coluna) - 1
                    if resultado is None:
                        resultado = trocar_colunas(matriz, idx, largura - 1 - idx)
                    else:
                        resultado = trocar_colunas(resultado, idx, largura - 1 - idx)
            
            with tab3:
                op_math = st.selectbox("Operação:", [
                    "Nenhuma", "Negativa", "Contar pixels brancos", 
                    "Multiplicar por escalar", "Somar com outra matriz"
                ], key="math")
                
                if op_math == "Negativa":
                    resultado = negativa(matriz)
                elif op_math == "Contar pixels brancos":
                    st.success(f"Pixels brancos: {contar_uns(matriz)}")
                elif op_math == "Multiplicar por escalar":
                    escalar = st.number_input("Valor do escalar:", min_value=0, value=1, key="escalar")
                    resultado = multiplicar_escalar(matriz, escalar)
                elif op_math == "Somar com outra matriz":
                    arq2 = st.file_uploader("Envie a segunda matriz", type="pbm", key="arq2")
                    if arq2:
                        m2 = ler_pbm(arq2.read().decode('utf-8'))
                        if m2 and len(m2) == altura and len(m2[0]) == largura:
                            resultado = somar_matrizes(matriz, m2)
                        else:
                            st.error("As matrizes devem ter as mesmas dimensões!")
            
            if 'resultado' in locals() and resultado is not None:
                st.subheader("Resultado")
                st.text('\n'.join(' '.join(str(x) for x in linha) for linha in resultado))
                st.download_button("Download PBM", matriz_para_pbm(resultado), "resultado.pbm")

if __name__ == "__main__":
    main()