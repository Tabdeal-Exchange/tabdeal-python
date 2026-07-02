#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/tabdeal-python-sdk"
VENV_PATH="$APP_HOME/venv"
VENV_PYTHON="$VENV_PATH/bin/python"

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

need_sudo() {
  if [[ "${EUID}" -ne 0 ]]; then
    echo "sudo"
  fi
}

install_prerequisites() {
  local sudo_cmd
  sudo_cmd="$(need_sudo)"

  echo "Python 3 or Tk support is missing. Attempting a conservative install..."

  if have_cmd apt-get; then
    ${sudo_cmd} apt-get update
    ${sudo_cmd} apt-get install -y python3 python3-venv python3-tk
    return
  fi
  if have_cmd dnf; then
    ${sudo_cmd} dnf install -y python3 python3-tkinter
    return
  fi
  if have_cmd yum; then
    ${sudo_cmd} yum install -y python3 tkinter
    return
  fi
  if have_cmd pacman; then
    ${sudo_cmd} pacman -Sy --noconfirm python tk
    return
  fi
  if have_cmd zypper; then
    ${sudo_cmd} zypper install -y python3 python3-tk
    return
  fi
  if have_cmd apk; then
    ${sudo_cmd} apk add --no-cache python3 py3-pip py3-virtualenv tcl tk
    return
  fi

  echo "Unsupported package manager. Install python3, python3-venv, and tkinter manually." >&2
  exit 1
}

if ! have_cmd python3; then
  install_prerequisites
fi

if ! python3 -c "import tkinter" >/dev/null 2>&1; then
  install_prerequisites
fi

mkdir -p "$APP_HOME"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Creating virtual environment in $VENV_PATH"
  python3 -m venv "$VENV_PATH"
fi

echo "Upgrading pip..."
"$VENV_PYTHON" -m pip install --upgrade pip

echo "Installing tabdeal-python from $PROJECT_ROOT"
"$VENV_PYTHON" -m pip install --upgrade "$PROJECT_ROOT"

echo "Launching Tabdeal Quickstart..."
"$VENV_PYTHON" -m tabdeal
