# procimage

## Descrição
`procimage` é um repositório para processamento de imagens. Este projeto contém scripts e ferramentas para manipulação, análise e transformação de imagens.

## Funcionalidades
- Carregamento de imagens em vários formatos
- Aplicação de filtros e efeitos
- Redimensionamento e corte de imagens
- Conversão entre diferentes formatos de imagem

## Requisitos
- Python 3.x
- Bibliotecas: `numpy`, `opencv-python`, `Pillow`

## Instalação
Clone o repositório e instale as dependências:
```bash
git clone https://github.com/seu-usuario/procimage.git
cd procimage
pip install -r requirements.txt
```

## Uso
Exemplo de uso básico:
```python
import procimage

# Carregar uma imagem
img = procimage.load_image('caminho/para/imagem.jpg')

# Aplicar um filtro
img_filtered = procimage.apply_filter(img, 'blur')

# Salvar a imagem processada
procimage.save_image(img_filtered, 'caminho/para/imagem_processada.jpg')
```

## Contribuição
Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.