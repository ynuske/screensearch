import os
import subprocess
import webbrowser
import requests


def capturar_tela(caminho_saida="/tmp/print.png"):
    estilo_slurp = " -b '#89b4fa22' -c '#cba6f7ff' -s '#00000044' -w 2"
    comando = f'grim -g "$(slurp {estilo_slurp})" {caminho_saida}'
    resultado = subprocess.run(comando, shell=True)

    if resultado.returncode != 0:
        print("Captura de tela cancelada.")
        return False

    return True


def buscar_no_google_lens(caminho_imagem):
    
    url_api = "https://catbox.moe/user/api.php"

    print("Enviando imagem...")

    try:
        
        with open(caminho_imagem, "rb") as arquivo:
            files = {"fileToUpload": arquivo}
            data = {"reqtype": "fileupload"}

            
            resposta = requests.post(url_api, data=data, files=files)

        if resposta.status_code == 200:
            url_imagem_publica = resposta.text.strip()

           
            url_lens = (
                f"https://www.google.com/searchbyimage?image_url={url_imagem_publica}"
            )

            print(f"Sucesso! Abrindo Google Lens: {url_lens}")

         
            webbrowser.open(url_lens)
        else:
            print(f"Erro no upload. Código HTTP: {resposta.status_code}")

    except Exception as e:
        print(f"Ocorreu um erro durante a requisição: {e}")


def main():
    caminho_temp = "/tmp/print.png"

  
    if capturar_tela(caminho_temp):
       
        buscar_no_google_lens(caminho_temp)

        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)


if __name__ == "__main__":
    main()
