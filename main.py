#!/usr/bin/env python3
"""
Wrapper principal para executar a aplicação.

Este arquivo permite executar: python main.py
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from app import main

if __name__ == "__main__":
    sys.exit(main())
