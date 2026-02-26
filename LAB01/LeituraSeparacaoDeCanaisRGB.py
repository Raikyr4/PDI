"""Laboratório 01: Leitura, exibição e separação de canais RGB (BGR no OpenCV)."""

from __future__ import annotations

from pathlib import Path
import argparse
import cv2


DEFAULT_IMAGE = Path(__file__).resolve().parent / "flores01.jpg"


def carregar_imagem(caminho: Path):
    """Carrega uma imagem colorida (8 bits por canal) usando OpenCV."""
    imagem = cv2.imread(str(caminho), cv2.IMREAD_COLOR)
    if imagem is None:
        raise FileNotFoundError(
            f"Não foi possível abrir a imagem '{caminho}'. "
            "Verifique se o arquivo existe e se está em um formato suportado."
        )
    return imagem


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lê uma imagem JPEG e exibe canais R, G e B em escala de cinza."
    )
    parser.add_argument(
        "--imagem",
        type=Path,
        default=DEFAULT_IMAGE,
        help=f"Caminho da imagem de entrada (padrão: {DEFAULT_IMAGE.name}).",
    )
    args = parser.parse_args()

    imagem_bgr = carregar_imagem(args.imagem)

    # OpenCV lê no formato BGR.
    canal_b, canal_g, canal_r = cv2.split(imagem_bgr)

    cv2.imshow("Imagem original (BGR)", imagem_bgr)
    cv2.imshow("Canal Vermelho (R) - escala de cinza", canal_r)
    cv2.imshow("Canal Verde (G) - escala de cinza", canal_g)
    cv2.imshow("Canal Azul (B) - escala de cinza", canal_b)

    print("Janelas abertas. Pressione qualquer tecla para encerrar.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
