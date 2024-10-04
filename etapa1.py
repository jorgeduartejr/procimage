import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Função para carregar a imagem
def carregar_imagem():
    global img_original, img_exibicao
    caminho_imagem = filedialog.askopenfilename()
    img_original = cv2.imread(caminho_imagem)
    img_rgb = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)  # Convertendo para RGB para exibir
    img_exibicao = ImageTk.PhotoImage(Image.fromarray(img_rgb))
    painel_imagem_original.config(image=img_exibicao)
    painel_imagem_original.image = img_exibicao

# Função para aplicar filtro passa-baixa (exemplo: GaussianBlur)
def filtro_passa_baixa():
    if img_original is not None:
        img_filtrada = cv2.GaussianBlur(img_original, (15, 15), 0)
        exibir_imagem_filtrada(img_filtrada)

import numpy as np
import cv2

import numpy as np
import cv2

# Função para aplicar filtro passa-alta usando subtração de um filtro passa-baixa
def filtro_passa_alta():
    if img_original is not None:
        # Converte a imagem original para escala de cinza
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        
        # Aplica um filtro passa-baixa (por exemplo, GaussianBlur)
        img_suave = cv2.GaussianBlur(img_gray, (15, 15), 0)
        
        # Subtrai a imagem suavizada da imagem original
        img_filtrada = cv2.subtract(img_gray, img_suave)

        # Amplifica os detalhes para exibição
        img_filtrada = cv2.convertScaleAbs(img_filtrada)

        # Para uma visualização melhor, aplicamos um limite
        _, img_filtrada = cv2.threshold(img_filtrada, 5, 500, cv2.THRESH_BINARY)

        # Exibe a imagem filtrada
        exibir_imagem_filtrada(img_filtrada)


# Função para exibir a imagem filtrada
def exibir_imagem_filtrada(img_filtrada):
    img_rgb = cv2.cvtColor(img_filtrada, cv2.COLOR_BGR2RGB) if len(img_filtrada.shape) == 3 else img_filtrada
    img_exibicao = ImageTk.PhotoImage(Image.fromarray(img_rgb))
    painel_imagem_filtrada.config(image=img_exibicao)
    painel_imagem_filtrada.image = img_exibicao

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Editor de Fotos - Filtros")

# Painéis para exibir imagens
painel_imagem_original = tk.Label(janela)
painel_imagem_original.grid(row=0, column=0)

painel_imagem_filtrada = tk.Label(janela)
painel_imagem_filtrada.grid(row=0, column=1)

# Botões para carregar imagem e aplicar filtros
botao_carregar = tk.Button(janela, text="Carregar Imagem", command=carregar_imagem)
botao_carregar.grid(row=1, column=0)

botao_filtro_passa_baixa = tk.Button(janela, text="Filtro Passa-Baixa", command=filtro_passa_baixa)
botao_filtro_passa_baixa.grid(row=1, column=1)

botao_filtro_passa_alta = tk.Button(janela, text="Filtro Passa-Alta", command=filtro_passa_alta)
botao_filtro_passa_alta.grid(row=1, column=2)

janela.mainloop()
