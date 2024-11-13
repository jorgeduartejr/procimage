import numpy as np
import tkinter as tk
from tkinter import filedialog

# Função para aplicar filtro passa-baixa (Gaussian Blur)
def filtro_passa_baixa():
    if img_original is not None:
        img_filtrada = img_original.filter(ImageFilter.GaussianBlur(radius=7))
        exibir_imagem_filtrada(img_filtrada)

# Função para aplicar filtro passa-baixa (Média)
def filtro_media():
    if img_original is not None:
        img_array = np.array(img_original)
        kernel_size = 15
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
        img_filtrada = aplicar_filtro_movel(img_array, kernel)
        img_filtrada_pil = Image.fromarray(img_filtrada.astype(np.uint8))
        exibir_imagem_filtrada(img_filtrada_pil)

# Função para aplicar filtro passa-baixa (Mediana)
def filtro_mediana():
    if img_original is not None:
        img_array = np.array(img_original)
        kernel_size = 15
        img_filtrada = aplicar_filtro_mediana(img_array, kernel_size)
        img_filtrada_pil = Image.fromarray(img_filtrada.astype(np.uint8))
        exibir_imagem_filtrada(img_filtrada_pil)

# Função genérica para aplicar a convolução com o kernel fornecido
def aplicar_filtro_movel(imagem, kernel):
    h, w = imagem.shape
    kh, kw = kernel.shape
    img_filtrada = np.zeros_like(imagem)

    for i in range(kh // 2, h - kh // 2):
        for j in range(kw // 2, w - kw // 2):
            img_filtrada[i, j] = np.sum(imagem[i - kh // 2:i + kh // 2 + 1, j - kw // 2:j + kw // 2 + 1] * kernel)
    return img_filtrada

# Função para aplicar filtro de mediana manualmente
def aplicar_filtro_mediana(imagem, kernel_size):
    h, w = imagem.shape
    img_filtrada = np.zeros_like(imagem)

    for i in range(kernel_size // 2, h - kernel_size // 2):
        for j in range(kernel_size // 2, w - kernel_size // 2):
            patch = imagem[i - kernel_size // 2:i + kernel_size // 2 + 1, j - kernel_size // 2:j + kernel_size // 2 + 1]
            img_filtrada[i, j] = np.median(patch)
    return img_filtrada

# Função para exibir a imagem filtrada
def exibir_imagem_filtrada(img_filtrada):
    img_exibicao_filtrada = ImageTk.PhotoImage(img_filtrada)
    painel_imagem_filtrada.config(image=img_exibicao_filtrada)
    painel_imagem_filtrada.image = img_exibicao_filtrada

# Função para carregar imagem
def carregar_imagem():
    global img_original, img_exibicao
    caminho_imagem = filedialog.askopenfilename()
    if caminho_imagem:
        img_original = Image.open(caminho_imagem).convert('L')
        img_exibicao = ImageTk.PhotoImage(img_original)
        painel_imagem_original.config(image=img_exibicao)
        painel_imagem_original.image = img_exibicao

from PIL import Image, ImageTk, ImageFilter

def filtro_passa_alta():
    if img_original is not None:
        # Converte a imagem PIL para um array NumPy
        img_array = np.array(img_original)
        
        # Define o tamanho do kernel (reduzido para 5x5)
        kernel_size = 5
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
        
        # Aplica a suavização (passa-baixa) com o filtro de média
        img_suave = aplicar_filtro_movel(img_array, kernel)
        
        # Calcula a diferença entre a imagem original e a suavizada (passa-alta)
        img_filtrada = img_array.astype(np.float32) - img_suave.astype(np.float32)
        
        # Amplifica o contraste das bordas (opcional)
        fator_amplificacao = 2.0
        img_filtrada = fator_amplificacao * img_filtrada
        
        # Normaliza os valores da imagem para o intervalo [0, 255]
        img_filtrada = np.clip(img_filtrada, 0, 255).astype(np.uint8)
        
        # Converte a imagem filtrada de volta para formato PIL e exibe
        img_filtrada_pil = Image.fromarray(img_filtrada)
        exibir_imagem_filtrada(img_filtrada_pil)


def filtro_laplaciano():
    if img_original is not None:
        img_array = np.array(img_original)
        laplacian_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        img_filtrada = aplicar_filtro_movel(img_array, laplacian_kernel)
        img_filtrada = np.clip(img_filtrada, 0, 255).astype(np.uint8)
        img_filtrada_pil = Image.fromarray(img_filtrada)
        exibir_imagem_filtrada(img_filtrada_pil)

def filtro_sobel():
    if img_original is not None:
        # Converte a imagem PIL para um array NumPy
        img_array = np.array(img_original)

        # Define os kernels Sobel para os eixos X e Y
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

        # Aplica os filtros Sobel nos eixos X e Y
        grad_x = aplicar_filtro_movel(img_array, sobel_x)
        grad_y = aplicar_filtro_movel(img_array, sobel_y)

        # Calcula a magnitude do gradiente combinando grad_x e grad_y
        img_filtrada = np.hypot(grad_x, grad_y)  # Calcula a raiz quadrada da soma dos quadrados dos gradientes
        
        # Normaliza a imagem para o intervalo 0-255 e converte para uint8
        img_filtrada = (img_filtrada / img_filtrada.max()) * 255
        img_filtrada = img_filtrada.astype(np.uint8)

        # Converte de volta para imagem PIL e exibe
        img_filtrada_pil = Image.fromarray(img_filtrada)
        exibir_imagem_filtrada(img_filtrada_pil)



# Interface gráfica
janela = tk.Tk()
janela.title("Editor de Fotos - Filtros de Imagem")

# Painéis para exibir imagens
painel_imagem_original = tk.Label(janela)
painel_imagem_original.grid(row=0, column=0)

painel_imagem_filtrada = tk.Label(janela)
painel_imagem_filtrada.grid(row=0, column=1)

# Botões para carregar imagem e aplicar filtros passa-baixa
botao_carregar = tk.Button(janela, text="Carregar Imagem", command=carregar_imagem)
botao_carregar.grid(row=1, column=0)

botao_filtro_passa_baixa = tk.Button(janela, text="Filtro Passa-Baixa (Gaussian)", command=filtro_passa_baixa)
botao_filtro_passa_baixa.grid(row=1, column=1)

botao_filtro_media = tk.Button(janela, text="Filtro Passa-Baixa (Média)", command=filtro_media)
botao_filtro_media.grid(row=1, column=2)

botao_filtro_mediana = tk.Button(janela, text="Filtro Passa-Baixa (Mediana)", command=filtro_mediana)
botao_filtro_mediana.grid(row=1, column=3)

# Botões para aplicar filtros passa-alta
botao_filtro_passa_alta = tk.Button(janela, text="Filtro Passa-Alta (Subtração de Passa-Baixa)", command=filtro_passa_alta)
botao_filtro_passa_alta.grid(row=2, column=1)

botao_filtro_laplaciano = tk.Button(janela, text="Filtro Passa-Alta (Laplaciano)", command=filtro_laplaciano)
botao_filtro_laplaciano.grid(row=2, column=2)

botao_filtro_sobel = tk.Button(janela, text="Filtro Passa-Alta (Sobel)", command=filtro_sobel)
botao_filtro_sobel.grid(row=2, column=3)

janela.mainloop()
