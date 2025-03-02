import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def acinzentar_imagem(caminho):
    imagem_cinza = Image.open(caminho).convert('L')
    exibir_imagem(imagem_cinza)

def binarizar_imagem(caminho, limiar=127):
    imagem = Image.open(caminho).convert('L')
    pixels = np.array(imagem)
    binarizada = np.where(pixels > limiar, 255, 0)
    exibir_imagem(binarizada)

def exibir_imagem(imagem):
    plt.imshow(imagem, cmap='gray')
    plt.axis('off')
    plt.show()