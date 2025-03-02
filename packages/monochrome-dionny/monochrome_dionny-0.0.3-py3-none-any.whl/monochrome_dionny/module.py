import numpy as np
from PIL import Image
import os

def acinzentar_imagem(caminho):
    imagem_cinza = Image.open(caminho).convert('L')
    salvar_imagem(caminho, imagem_cinza, "cinza")

def binarizar_imagem(caminho, limiar=127):
    imagem = Image.open(caminho).convert('L')
    pixels = np.array(imagem)
    binarizada = np.where(pixels > limiar, 255, 0)
    salvar_imagem(caminho, binarizada, "binarizada")

def salvar_imagem(caminho, pixels, sufixo):
    nome_arquivo, extensao = os.path.splitext(os.path.basename(caminho))
    novo_nome = f"{nome_arquivo}_{sufixo}{extensao}"

    imagem_binarizada = Image.fromarray(np.uint8(pixels))
    imagem_binarizada.save(novo_nome)