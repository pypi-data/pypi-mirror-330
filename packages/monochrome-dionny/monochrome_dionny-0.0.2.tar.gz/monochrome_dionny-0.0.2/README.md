# Monochrome Dionny
Esse pacote permite transformar as cores de uma imagem em tons de cinza ou binarizadas em preto e branco.

## Descrição
O objetivo da criação desse pacote foi para experiênciar e aprender a como utilizar o Pypi.

O pacote contem duas funções:
 - Acinzentar imagem: Transforma as cores da imagem em tons de cinza
 - Binarizar imagem: Transforma as cores da imagem em preto e branco

A imagem será exibida pelo Matplotlib e terá a opção para salvá-la.

## Instalação
```python
pip install monochrome-dionny
```

## Uso
### Acinzentar imagem
```python
import monochrome_dionny as monodio

camimho_imagem = r"C:\Users\UserA\Imagens\dio.jpg"

monodio.acinzentar_imagem(camimho_imagem)
```

### Binarizar imagem
```python
import monochrome_dionny as monodio

camimho_imagem = r"C:\Users\UserA\Imagens\dio.jpg"

monodio.binarizar_imagem(camimho_imagem)
```

## Cuidados
Certifique-se de adiconar um "r" antes do caminho da imagem, isso evitará problemas com as "\\".

```python
camimho = r"C:\Users\UserA\Imagens\dio.jpg"
```