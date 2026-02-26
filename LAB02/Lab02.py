"""Laboratório 02: Conversão BGR -> HSV e análise visual de canais H, S e V."""

from __future__ import annotations

from pathlib import Path
import argparse
import cv2


DEFAULT_IMAGE = Path(__file__).resolve().parent / "fruta12.jpg"


def carregar_imagem(caminho: Path):
    """Carrega uma imagem colorida com OpenCV."""
    imagem = cv2.imread(str(caminho), cv2.IMREAD_COLOR)
    if imagem is None:
        raise FileNotFoundError(
            f"Não foi possível abrir a imagem '{caminho}'. "
            "Verifique se o arquivo existe e se está em um formato suportado."
        )
    return imagem


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte uma imagem para HSV e exibe canais H, S e V."
    )
    parser.add_argument(
        "--imagem",
        type=Path,
        default=DEFAULT_IMAGE,
        help=f"Caminho da imagem de entrada (padrão: {DEFAULT_IMAGE.name}).",
    )
    args = parser.parse_args()

    imagem_bgr = carregar_imagem(args.imagem)
    imagem_hsv = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2HSV)
    canal_h, canal_s, canal_v = cv2.split(imagem_hsv)

    # Análise visual dos canais HSV:
    # H (Hue/Tonalidade): áreas claras indicam pixels com valores de matiz mais altos
    # dentro do intervalo do OpenCV (0 a 179). Esse canal representa "qual cor" é
    # percebida, não o brilho. Em geral, regiões com cores diferentes podem aparecer
    # com níveis de cinza distintos mesmo tendo brilho semelhante.
    #
    # S (Saturação): áreas claras indicam cores mais puras/vivas (alta saturação).
    # Áreas escuras tendem a cores dessaturadas, próximas de tons de cinza.
    #
    # V (Valor/Brilho): representa a intensidade luminosa. Áreas claras no V
    # correspondem às partes mais iluminadas da imagem original; áreas escuras,
    # às regiões de sombra ou menor brilho.

    cv2.imshow("Imagem original (BGR)", imagem_bgr)
    cv2.imshow("Canal H (Tonalidade) - escala de cinza", canal_h)
    cv2.imshow("Canal S (Saturacao) - escala de cinza", canal_s)
    cv2.imshow("Canal V (Brilho/Valor) - escala de cinza", canal_v)

    print("Janelas abertas. Pressione qualquer tecla para encerrar.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
