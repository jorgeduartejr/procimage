import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


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

# Função para aplicar erosão manualmente
def aplicar_erosao():
    global img_original
    if img_original is not None:
        img_array = np.array(img_original)
        img_erosao = np.zeros_like(img_array)
        
        for i in range(1, img_array.shape[0] - 1):
            for j in range(1, img_array.shape[1] - 1):
                if np.all(img_array[i-1:i+2, j-1:j+2] == 255):
                    img_erosao[i, j] = 255
                else:
                    img_erosao[i, j] = 0

        img_erosao_pil = Image.fromarray(img_erosao)
        exibir_imagem_filtrada(img_erosao_pil)

def aplicar_dilatacao():
    global img_original
def aplicar_dilatacao():
    if img_original is not None:
        img_array = np.array(img_original)
        img_dilatacao = np.zeros_like(img_array)
        
        for i in range(1, img_array.shape[0] - 1):
            for j in range(1, img_array.shape[1] - 1):
                if np.any(img_array[i-1:i+2, j-1:j+2] == 255):
                    img_dilatacao[i, j] = 255
                else:
                    img_dilatacao[i, j] = 0

        img_dilatacao_pil = Image.fromarray(img_dilatacao)
        exibir_imagem_filtrada(img_dilatacao_pil)
def aplicar_abertura():
    global img_original
# Função para aplicar abertura (erosão seguida de dilatação)
def aplicar_abertura():
    if img_original is not None:
        img_array = np.array(img_original)
        
        # Erosão
        img_erosao = np.zeros_like(img_array)
        for i in range(1, img_array.shape[0] - 1):
            for j in range(1, img_array.shape[1] - 1):
                if np.all(img_array[i-1:i+2, j-1:j+2] == 255):
                    img_erosao[i, j] = 255
                else:
                    img_erosao[i, j] = 0

        # Dilatação após erosão
        img_abertura = np.zeros_like(img_erosao)
        for i in range(1, img_erosao.shape[0] - 1):
            for j in range(1, img_erosao.shape[1] - 1):
                if np.any(img_erosao[i-1:i+2, j-1:j+2] == 255):
                    img_abertura[i, j] = 255
                else:
                    img_abertura[i, j] = 0

        img_abertura_pil = Image.fromarray(img_abertura)
def aplicar_fechamento():
    global img_original

# Função para aplicar fechamento (dilatação seguida de erosão)
def aplicar_fechamento():
    if img_original is not None:
        img_array = np.array(img_original)
        
        # Dilatação
        img_dilatacao = np.zeros_like(img_array)
        for i in range(1, img_array.shape[0] - 1):
            for j in range(1, img_array.shape[1] - 1):
                if np.any(img_array[i-1:i+2, j-1:j+2] == 255):
                    img_dilatacao[i, j] = 255
                else:
                    img_dilatacao[i, j] = 0

        # Erosão após dilatação
        img_fechamento = np.zeros_like(img_dilatacao)
        for i in range(1, img_dilatacao.shape[0] - 1):
            for j in range(1, img_dilatacao.shape[1] - 1):
                if np.all(img_dilatacao[i-1:i+2, j-1:j+2] == 255):
                    img_fechamento[i, j] = 255
                else:
                    img_fechamento[i, j] = 0

        img_fechamento_pil = Image.fromarray(img_fechamento)
        exibir_imagem_filtrada(img_fechamento_pil)

# Função para aplicar limiarização binária
def limiarizacao_binaria():
    if img_original is not None:
        img_array = np.array(img_original.convert('L'))
        limiar = 127
        img_limiarizada = np.where(img_array > limiar, 255, 0).astype(np.uint8)
        img_limiarizada_pil = Image.fromarray(img_limiarizada)
        exibir_imagem_filtrada(img_limiarizada_pil)

# Função para aplicar limiarização adaptativa (Otsu)
def limiarizacao_otsu():
    if img_original is not None:
        img_array = np.array(img_original.convert('L'))
        limiar = otsu_threshold(img_array)
        img_otsu = np.where(img_array > limiar, 255, 0).astype(np.uint8)
        img_otsu_pil = Image.fromarray(img_otsu)
        exibir_imagem_filtrada(img_otsu_pil)

# Função para calcular o limiar de Otsu
def otsu_threshold(img_array):
    hist, _ = np.histogram(img_array, bins=256, range=(0, 256))
    total = img_array.size
    current_max, threshold = 0, 0
    sum_total, sum_foreground, weight_background, weight_foreground = 0, 0, 0, 0

    for t in range(256):
        sum_total += t * hist[t]

    for t in range(256):
        weight_background += hist[t]
        if weight_background == 0:
            continue
        weight_foreground = total - weight_background
        if weight_foreground == 0:
            break
        sum_foreground += t * hist[t]
        mean_background = sum_foreground / weight_background
        mean_foreground = (sum_total - sum_foreground) / weight_foreground
        between_class_variance = weight_background * weight_foreground * ((mean_background - mean_foreground) ** 2)
        if between_class_variance > current_max:
            current_max = between_class_variance
            threshold = t
    return threshold

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

# Interface gráfica
janela = tk.Tk()
janela.title("Editor de Fotos - Operações Morfológicas e Segmentação")

# Painéis para exibir imagens
painel_imagem_original = tk.Label(janela)
painel_imagem_original.grid(row=0, column=0)

painel_imagem_filtrada = tk.Label(janela)
painel_imagem_filtrada.grid(row=0, column=1)

# Botões para carregar imagem e aplicar operações
botao_carregar = tk.Button(janela, text="Carregar Imagem", command=carregar_imagem)
botao_carregar.grid(row=1, column=0)

# Botões de operações morfológicas
botao_erosao = tk.Button(janela, text="Erosão", command=aplicar_erosao)
botao_erosao.grid(row=1, column=1)

botao_dilatacao = tk.Button(janela, text="Dilatação", command=aplicar_dilatacao)
botao_dilatacao.grid(row=1, column=2)

botao_abertura = tk.Button(janela, text="Abertura", command=aplicar_abertura)
botao_abertura.grid(row=2, column=1)

botao_fechamento = tk.Button(janela, text="Fechamento", command=aplicar_fechamento)
botao_fechamento.grid(row=2, column=2)

# Botões de segmentação
botao_limiarizacao_binaria = tk.Button(janela, text="Limiarização Binária", command=limiarizacao_binaria)
botao_limiarizacao_binaria.grid(row=3, column=1)

botao_limiarizacao_otsu = tk.Button(janela, text="Limiarização Otsu", command=limiarizacao_otsu)
botao_limiarizacao_otsu.grid(row=3, column=2)

janela.mainloop()
