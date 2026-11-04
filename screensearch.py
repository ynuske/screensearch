import os
import subprocess
import tempfile
import webbrowser
from urllib.parse import quote

import requests

LITTERBOX_API = "https://litterbox.catbox.moe/resources/internals/api.php"
TEMPO_EXPIRACAO = "1h"  #  1h, 12h, 24h, 72h
LENS_URL = "https://lens.google.com/uploadbyurl?url={}"
TIMEOUT_UPLOAD = 30


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
    )
}

ESTILO_SLURP = ["-b", "#89b4fa22", "-c", "#cba6f7ff", "-s", "#00000044", "-w", "2"]


def capturar_tela(caminho_saida):
    
    try:
        slurp = subprocess.run(
            ["slurp", *ESTILO_SLURP],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("Erro: 'slurp' não está instalado.")
        return False

    if slurp.returncode != 0:
        print("Captura de tela cancelada.")
        return False

    regiao = slurp.stdout.strip()

    try:
        grim = subprocess.run(["grim", "-g", regiao, caminho_saida])
    except FileNotFoundError:
        print("Erro: 'grim' não está instalado.")
        return False

    if grim.returncode != 0:
        print("Erro ao capturar a tela com o grim.")
        return False

    return True


def enviar_imagem(caminho_imagem):
    
    print("Enviando imagem...")

    try:
        with open(caminho_imagem, "rb") as arquivo:
            resposta = requests.post(
                LITTERBOX_API,
                data={"reqtype": "fileupload", "time": TEMPO_EXPIRACAO},
                files={"fileToUpload": arquivo},
                headers=HEADERS,
                timeout=TIMEOUT_UPLOAD,
            )
        resposta.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro no upload: {e}")
        return None

    url_publica = resposta.text.strip()

    if not url_publica.startswith("https://"):
        print(f"Resposta inesperada do servidor: {url_publica}")
        return None

    return url_publica


def buscar_no_google_lens(caminho_imagem):
    url_publica = enviar_imagem(caminho_imagem)
    if not url_publica:
        return

    url_lens = LENS_URL.format(quote(url_publica, safe=""))
    print(f"Sucesso! Abrindo Google Lens: {url_lens}")
    webbrowser.open(url_lens)


def main():
    # Arquivo temporario 
    fd, caminho_temp = tempfile.mkstemp(suffix=".png")
    os.close(fd)

    try:
        if capturar_tela(caminho_temp):
            buscar_no_google_lens(caminho_temp)
    finally:
        # Limpa o arquivo 
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)


if __name__ == "__main__":
    main()
