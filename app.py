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
    return [list(reversed(col)) for col in zip(*matriz)]

def rotacionar_180(matriz):
    return [list(reversed(linha)) for linha in reversed(matriz)]

def rotacionar_270(matriz):
    return [list(col) for col in reversed(list(zip(*matriz)))]

def inverter_horizontal(matriz):
    return [list(reversed(linha)) for linha in matriz]

def inverter_vertical(matriz):
    return [linha.copy() for linha in reversed(matriz)]

# Operações de Permuta Dinâmicas
def trocar_linhas(matriz, i, j):
    nova_matriz = [linha.copy() for linha in matriz]
    nova_matriz[i], nova_matriz[j] = nova_matriz[j], nova_matriz[i]
    return nova_matriz

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
    
    # Inicializa o estado da sessão
    if 'matriz_original' not in st.session_state:
        st.session_state.matriz_original = None
    if 'resultado' not in st.session_state:
        st.session_state.resultado = None
    if 'segunda_matriz' not in st.session_state:
        st.session_state.segunda_matriz = None
    
    arquivo = st.file_uploader("Envie seu arquivo PBM", type="pbm", key="file_uploader")
    
    if arquivo:
        # Atualiza a matriz original se um novo arquivo foi carregado
        if st.session_state.matriz_original is None or arquivo.name != st.session_state.get('current_file'):
            st.session_state.matriz_original = ler_pbm(arquivo.read().decode('utf-8'))
            st.session_state.current_file = arquivo.name
            st.session_state.resultado = None
            st.session_state.segunda_matriz = None
        
        if st.session_state.matriz_original:
            matriz = st.session_state.matriz_original
            altura = len(matriz)
            largura = len(matriz[0]) if altura > 0 else 0
            
            # Mostra a matriz original
            st.subheader("Matriz Original")
            st.text(f"Dimensões: {largura}x{altura}")
            st.text('\n'.join(' '.join(str(x) for x in linha) for linha in matriz))
            st.write("---")
            
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
                    temp_result = matriz if st.session_state.resultado is None else st.session_state.resultado.copy()
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
                
                if op_math == "Multiplicar por escalar":
                    escalar = st.number_input("Valor do escalar:", min_value=0, value=1, key="escalar")
                    if st.button("Aplicar Multiplicação"):
                        temp_result = matriz if st.session_state.resultado is None else st.session_state.resultado
                        st.session_state.resultado = multiplicar_escalar(temp_result, escalar)
                
                elif op_math == "Somar com outra matriz":
                    arq2 = st.file_uploader("Envie a segunda matriz", type="pbm", key="arq2")
                    if arq2:
                        st.session_state.segunda_matriz = ler_pbm(arq2.getvalue().decode('utf-8'))
                    
                    if st.button("Aplicar Soma"):
                        if st.session_state.segunda_matriz is not None:
                            m2 = st.session_state.segunda_matriz
                            temp_result = matriz if st.session_state.resultado is None else st.session_state.resultado
                            if m2 and len(m2) == altura and len(m2[0]) == largura:
                                st.session_state.resultado = somar_matrizes(temp_result, m2)
                            else:
                                st.error("As matrizes devem ter as mesmas dimensões!")
                        else:
                            st.error("Por favor, envie a segunda matriz primeiro")
                
                elif op_math == "Negativa":
                    if st.button("Aplicar Negativa"):
                        temp_result = matriz if st.session_state.resultado is None else st.session_state.resultado
                        st.session_state.resultado = negativa(temp_result)
                
                elif op_math == "Contar pixels brancos":
                    if st.button("Contar Pixels Brancos"):
                        temp_result = matriz if st.session_state.resultado is None else st.session_state.resultado
                        st.success(f"Pixels brancos: {contar_uns(temp_result)}")
            
            # Exibe o resultado
            if st.session_state.resultado is not None:
                st.subheader("Resultado")
                st.text('\n'.join(' '.join(str(x) for x in linha) for linha in st.session_state.resultado))
                st.download_button("Download PBM", matriz_para_pbm(st.session_state.resultado), "resultado.pbm")

if __name__ == "__main__":
    main()