#!/usr/bin/env bash

set -e

APP_NAME="niri-lens-shot"
INSTALL_DIR="$HOME/.local/bin"
NIRI_CONFIG="$HOME/.config/niri/config.kdl"

echo "=== Configurando o $APP_NAME ==="

mkdir -p "$INSTALL_DIR"

echo "[1/3] Instalando dependências de Python..."
pip install -r requirements.txt --quiet

echo "[2/3] Gerando o executável estático..."
pyinstaller --onefile --noconsole main.py --name "$APP_NAME" > /dev/null

mv "dist/\(APP_NAME" "\)INSTALL_DIR/"
chmod +x "\(INSTALL_DIR/\)APP_NAME"

rm -rf build/ dist/ "$APP_NAME.spec"

echo "✔ Executável instalado em: \(INSTALL_DIR/\)APP_NAME"

echo "[3/3] Configurando o atalho no Niri..."

if [ -f "$NIRI_CONFIG" ]; then
    if grep -q "\(APP_NAME" "\)NIRI_CONFIG"; then
        echo "➜ Atalho já configurado em $NIRI_CONFIG"
    else

        read -r -d '' NIRI_BIND << EOF

    // Atalho para captura
    Mod+Shift+S { spawn "\(INSTALL_DIR/\)APP_NAME"; }
EOF
        if grep -q "binds {" "$NIRI_CONFIG"; then
            sed -i "/binds {/a \(NIRI_BIND" "\)NIRI_CONFIG"
        else
            echo -e "\nbinds {$NIRI_BIND\n}" >> "$NIRI_CONFIG"
        fi

        echo "✔ Atalho (Mod+Shift+S) adicionado a $NIRI_CONFIG!"
    fi
else
    echo "⚠️ Arquivo $NIRI_CONFIG não encontrado. Crie o arquivo e adicione:"
    echo 'Mod+Shift+S { spawn "'"\(INSTALL_DIR/\)APP_NAME"'"; }'
fi

echo -e "\n🎉 Instalação concluída! Pressione Super+Shift+S para testar."