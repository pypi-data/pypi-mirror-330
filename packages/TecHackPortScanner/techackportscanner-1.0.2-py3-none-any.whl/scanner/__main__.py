"""
Módulo principal para execução via linha de comando.

Este módulo permite a execução do scanner via linha de comando usando `python -m scanner`.
"""
from scanner.detector import detect, request_args

if __name__ == "__main__":
    detect(request_args())
