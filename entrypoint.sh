#!/bin/bash
set -e

echo "[!] Actualizando firmas..."
suricata-update --quiet

echo "[!] Iniciando Streamlit..."
exec "$@"