import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Função para carregar a imagem
def carregar_imagem():
    global img_original, img_exibicao
    caminho_imagem = filedialog.askopenfilename()
    img_original = cv2.imread(caminho_imagem)
    img_rgb = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)  # Convertendo para RGB para exibir
    img_exibicao = ImageTk.PhotoImage(Image.fromarray(img_rgb))
    painel_imagem_original.config(image=img_exibicao)
    painel_imagem_original.image = img_exibicao

# Função para aplicar filtro passa-baixa (Gaussian Blur)
def filtro_passa_baixa():
    if img_original is not None:
        img_filtrada = cv2.GaussianBlur(img_original, (15, 15), 0)
        exibir_imagem_filtrada(img_filtrada)

# Função para aplicar filtro passa-baixa (Média)
def filtro_media():
    if img_original is not None:
        img_filtrada = cv2.blur(img_original, (15, 15))
        exibir_imagem_filtrada(img_filtrada)

# Função para aplicar filtro passa-baixa (Mediana)
def filtro_mediana():
    if img_original is not None:
        img_filtrada = cv2.medianBlur(img_original, 15)
        exibir_imagem_filtrada(img_filtrada)

# Função para aplicar filtro passa-alta (Subtração de passa-baixa)
def filtro_passa_alta():
    if img_original is not None:
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        img_suave = cv2.GaussianBlur(img_gray, (15, 15), 0)
        img_filtrada = cv2.subtract(img_gray, img_suave)
        img_filtrada = cv2.convertScaleAbs(img_filtrada)
        exibir_imagem_filtrada(img_filtrada)

# Função para aplicar filtro passa-alta (Laplaciano)
def filtro_laplaciano():
    if img_original is not None:
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        img_filtrada = cv2.Laplacian(img_gray, cv2.CV_64F)
        img_filtrada = cv2.convertScaleAbs(img_filtrada)
        exibir_imagem_filtrada(img_filtrada)

# Função para aplicar filtro passa-alta (Sobel)
def filtro_sobel():
    if img_original is not None:
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=5)
        img_filtrada = cv2.sqrt(sobelx**2 + sobely**2)
        img_filtrada = cv2.convertScaleAbs(img_filtrada)
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

botao_filtro_passa_baixa = tk.Button(janela, text="Gaussian Blur (Passa-Baixa)", command=filtro_passa_baixa)
botao_filtro_passa_baixa.grid(row=1, column=1)

botao_filtro_media = tk.Button(janela, text="Filtro de Média (Passa-Baixa)", command=filtro_media)
botao_filtro_media.grid(row=2, column=1)

botao_filtro_mediana = tk.Button(janela, text="Filtro de Mediana (Passa-Baixa)", command=filtro_mediana)
botao_filtro_mediana.grid(row=3, column=1)

botao_filtro_passa_alta = tk.Button(janela, text="Passa-Alta (Subtração)", command=filtro_passa_alta)
botao_filtro_passa_alta.grid(row=1, column=2)

botao_filtro_laplaciano = tk.Button(janela, text="Filtro Laplaciano (Passa-Alta)", command=filtro_laplaciano)
botao_filtro_laplaciano.grid(row=2, column=2)

botao_filtro_sobel = tk.Button(janela, text="Filtro Sobel (Passa-Alta)", command=filtro_sobel)
botao_filtro_sobel.grid(row=3, column=2)

janela.mainloop()
