"""Laboratório 01: leitura e separação de canais em lote.

Ao executar este arquivo, todas as imagens suportadas da pasta LAB01 são processadas.
As visualizações são montadas em um único painel (2x2) para evitar múltiplas janelas.
"""

from __future__ import annotations

from pathlib import Path
import cv2
import numpy as np


BASE_DIR = Path(__file__).resolve().parent
SUPPORTED_EXTENSIONS = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff")
WINDOW_NAME = "LAB01 - Original + Canais RGB"
MAX_WINDOW_WIDTH = 1400
MAX_WINDOW_HEIGHT = 900


def listar_imagens(base_dir: Path) -> list[Path]:
    imagens: list[Path] = []
    for pattern in SUPPORTED_EXTENSIONS:
        imagens.extend(base_dir.glob(pattern))
    return sorted(imagens)


def criar_tile(imagem: np.ndarray, titulo: str, tamanho: tuple[int, int]) -> np.ndarray:
    tile = cv2.resize(imagem, tamanho, interpolation=cv2.INTER_AREA)
    cv2.putText(
        tile,
        titulo,
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    return tile


def ajustar_para_tela(imagem: np.ndarray) -> np.ndarray:
    altura, largura = imagem.shape[:2]
    fator = min(MAX_WINDOW_WIDTH / largura, MAX_WINDOW_HEIGHT / altura, 1.0)
    if fator == 1.0:
        return imagem
    novo_tamanho = (int(largura * fator), int(altura * fator))
    return cv2.resize(imagem, novo_tamanho, interpolation=cv2.INTER_AREA)


def montar_painel(imagem_bgr: np.ndarray, nome_arquivo: str) -> np.ndarray:
    canal_b, canal_g, canal_r = cv2.split(imagem_bgr)

    h, w = imagem_bgr.shape[:2]
    tile_size = (max(320, w // 2), max(240, h // 2))

    original = criar_tile(imagem_bgr.copy(), f"Original: {nome_arquivo}", tile_size)
    red = criar_tile(cv2.cvtColor(canal_r, cv2.COLOR_GRAY2BGR), "Canal R", tile_size)
    green = criar_tile(cv2.cvtColor(canal_g, cv2.COLOR_GRAY2BGR), "Canal G", tile_size)
    blue = criar_tile(cv2.cvtColor(canal_b, cv2.COLOR_GRAY2BGR), "Canal B", tile_size)

    linha_superior = cv2.hconcat([original, red])
    linha_inferior = cv2.hconcat([green, blue])
    painel = cv2.vconcat([linha_superior, linha_inferior])
    return ajustar_para_tela(painel)


def main() -> None:
    imagens = listar_imagens(BASE_DIR)
    if not imagens:
        raise FileNotFoundError(f"Nenhuma imagem encontrada em {BASE_DIR}.")

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    for indice, caminho in enumerate(imagens, start=1):
        imagem_bgr = cv2.imread(str(caminho), cv2.IMREAD_COLOR)
        if imagem_bgr is None:
            print(f"[AVISO] Não foi possível abrir: {caminho.name}")
            continue

        painel = montar_painel(imagem_bgr, caminho.name)
        cv2.imshow(WINDOW_NAME, painel)
        print(
            f"[{indice}/{len(imagens)}] {caminho.name} | "
            "ENTER/ESPACO: próxima imagem | Q/ESC: sair"
        )

        tecla = cv2.waitKey(0) & 0xFF
        if tecla in (ord("q"), 27):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
