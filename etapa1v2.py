import numpy as np
from PIL import Image, ImageFilter
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk

# Função para carregar a imagem
def carregar_imagem():
    global img_original, img_exibicao
    caminho_imagem = filedialog.askopenfilename()
    img_original = Image.open(caminho_imagem).convert('L')  # Converte para escala de cinza diretamente com PIL
    img_exibicao = ImageTk.PhotoImage(img_original)
    painel_imagem_original.config(image=img_exibicao)
    painel_imagem_original.image = img_exibicao

# Função para aplicar o filtro passa-alta (usando NumPy e PIL)
def filtro_passa_alta():
    if img_original is not None:
        # Converte a imagem para um array NumPy
        img_array = np.array(img_original)

        # Aplica suavização (filtro passa-baixa) usando um filtro de média
        kernel_size = 5
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
        img_suave = aplicar_filtro_movel(img_array, kernel)

        # Subtrai a imagem suavizada da imagem original (filtro passa-alta)
        img_filtrada = img_array - img_suave

        # Normaliza para evitar valores fora do intervalo [0, 255]
        img_filtrada = np.clip(img_filtrada, 0, 255).astype(np.uint8)

        # Converte de volta para a imagem PIL para exibir
        img_filtrada_pil = Image.fromarray(img_filtrada)
        img_exibicao_filtrada = ImageTk.PhotoImage(img_filtrada_pil)
        painel_imagem_filtrada.config(image=img_exibicao_filtrada)
        painel_imagem_filtrada.image = img_exibicao_filtrada

# Função para aplicar o filtro de média móvel (convolução simples)
def aplicar_filtro_movel(imagem, kernel):
    # Dimensões da imagem e do kernel
    h, w = imagem.shape
    kh, kw = kernel.shape
    img_suave = np.zeros_like(imagem)

    # Aplicar a convolução 2D manualmente
    for i in range(h - kh + 1):
        for j in range(w - kw + 1):
            img_suave[i, j] = np.sum(imagem[i:i+kh, j:j+kw] * kernel)
    
    return img_suave

# Interface gráfica
janela = tk.Tk()
janela.title("Editor de Fotos - Filtro Passa-Alta")

# Painéis para exibir imagens
painel_imagem_original = tk.Label(janela)
painel_imagem_original.grid(row=0, column=0)

painel_imagem_filtrada = tk.Label(janela)
painel_imagem_filtrada.grid(row=0, column=1)

# Botões para carregar imagem e aplicar filtros
botao_carregar = tk.Button(janela, text="Carregar Imagem", command=carregar_imagem)
botao_carregar.grid(row=1, column=0)

botao_filtro_passa_alta = tk.Button(janela, text="Filtro Passa-Alta", command=filtro_passa_alta)
botao_filtro_passa_alta.grid(row=1, column=1)

janela.mainloop()
