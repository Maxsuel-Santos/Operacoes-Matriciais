import streamlit as st

# Função para ler o arquivo .pbm
def ler_pbm(conteudo):
    linhas = [linha.strip() for linha in conteudo.split('\n') 
             if linha.strip() and not linha.startswith('#')]
    if not linhas or linhas[0] != 'P1':
        st.error("Formato PBM inválido. Deve começar com P1.")
        return None
    largura, altura = map(int, linhas[1].split())
    dados = ' '.join(linhas[2:]).split()
    return [[int(dados[i*largura + j]) for j in range(largura)] for i in range(altura)]

# Função para converter .pbm para matriz de 0s e 1s
def matriz_para_pbm(matriz):
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0
    return f"P1\n{largura} {altura}\n" + '\n'.join(' '.join(map(str, linha)) for linha in matriz)

# Operações Geométricas
def transposta(matriz):
    return [[linha[i] for linha in matriz] for i in range(len(matriz[0]))]

def rotacionar_90(matriz):
    return [list(reversed(col)) for col in zip(*matriz)]

def rotacionar_180(matriz):
    return [list(reversed(linha)) for linha in reversed(matriz)]

def rotacionar_270(matriz):
    return [list(col) for col in reversed(list(zip(*matriz)))]

def inverter_horizontal(matriz):
    return [list(reversed(linha)) for linha in matriz]

def inverter_vertical(matriz):
    return [linha.copy() for linha in reversed(matriz)]

# Operações de Permuta
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
            
            # Mostra a matriz original
            st.subheader("Matriz Original")
            st.text(f"Dimensões: {largura}x{altura}")
            st.text('\n'.join(' '.join(str(x) for x in linha) for linha in matriz))
            st.write("---")
            
            # Variável para armazenar o resultado
            if 'resultado' not in st.session_state:
                st.session_state.resultado = None
            
            tab1, tab2, tab3 = st.tabs(["Operações Geométricas", "Permutas", "Operações Matemáticas"])
            
            with tab1:
                op_geo = st.selectbox("Selecione:", [
                    "Nenhuma", "Transposta", "Rotacionar 90°", "Rotacionar 180°", 
                    "Rotacionar 270°", "Inverter Horizontal", "Inverter Vertical"
                ], key="geo")
                
                if st.button("Aplicar Transformação Geométrica"):
                    if op_geo == "Transposta":
                        st.session_state.resultado = transposta(matriz)
                    elif op_geo == "Rotacionar 90°":
                        st.session_state.resultado = rotacionar_90(matriz)
                    elif op_geo == "Rotacionar 180°":
                        st.session_state.resultado = rotacionar_180(matriz)
                    elif op_geo == "Rotacionar 270°":
                        st.session_state.resultado = rotacionar_270(matriz)
                    elif op_geo == "Inverter Horizontal":
                        st.session_state.resultado = inverter_horizontal(matriz)
                    elif op_geo == "Inverter Vertical":
                        st.session_state.resultado = inverter_vertical(matriz)
            
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    opcoes_linhas = ["Nenhuma"] + gerar_opcoes_permuta(altura, "linha")
                    op_linha = st.selectbox("Linhas:", opcoes_linhas, key="linha")
                
                with col2:
                    opcoes_colunas = ["Nenhuma"] + gerar_opcoes_permuta(largura, "coluna")
                    op_coluna = st.selectbox("Colunas:", opcoes_colunas, key="coluna")
                
                if st.button("Aplicar Permuta"):
                    temp_result = matriz if st.session_state.resultado is None else st.session_state.resultado
                    if op_linha != "Nenhuma":
                        idx = opcoes_linhas.index(op_linha) - 1
                        temp_result = trocar_linhas(temp_result, idx, altura - 1 - idx)
                    
                    if op_coluna != "Nenhuma":
                        idx = opcoes_colunas.index(op_coluna) - 1
                        temp_result = trocar_colunas(temp_result, idx, largura - 1 - idx)
                    
                    st.session_state.resultado = temp_result
            
            with tab3:
                op_math = st.selectbox("Operação:", [
                    "Nenhuma", "Negativa", "Contar pixels brancos", 
                    "Multiplicar por escalar", "Somar com outra matriz"
                ], key="math")
                
                # Mostra input do escalar 
                if op_math == "Multiplicar por escalar":
                    escalar = st.number_input("Valor do escalar:", min_value=0, value=1, key="escalar")
                
                # Mostra upload de arquivo 
                if op_math == "Somar com outra matriz":
                    arq2 = st.file_uploader("Envie a segunda matriz", type="pbm", key="arq2")
                
                if st.button("Aplicar Operação Matemática"):
                    temp_result = matriz if st.session_state.resultado is None else st.session_state.resultado
                    if op_math == "Negativa":
                        st.session_state.resultado = negativa(temp_result)
                    elif op_math == "Multiplicar por escalar":
                        st.session_state.resultado = multiplicar_escalar(temp_result, escalar)
                    elif op_math == "Somar com outra matriz":
                        if 'arq2' in st.session_state and st.session_state.arq2 is not None:
                            m2 = ler_pbm(st.session_state.arq2.getvalue().decode('utf-8'))
                            if m2 and len(m2) == altura and len(m2[0]) == largura:
                                st.session_state.resultado = somar_matrizes(temp_result, m2)
                            else:
                                st.error("As matrizes devem ter as mesmas dimensões!")
                        else:
                            st.error("Por favor, envie a segunda matriz primeiro")
                    elif op_math == "Contar pixels brancos":
                        st.success(f"Pixels brancos: {contar_uns(temp_result)}")
            
            # Exibe o resultado
            if st.session_state.resultado is not None:
                st.subheader("Resultado")
                st.text('\n'.join(' '.join(str(x) for x in linha) for linha in st.session_state.resultado))
                st.download_button("Download PBM", matriz_para_pbm(st.session_state.resultado), "resultado.pbm")

if __name__ == "__main__":
    main()
