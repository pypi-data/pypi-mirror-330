#!/usr/bin/python3

import tempfile
import subprocess
import os
import sys
import platform


import webbrowser

def open_url(url):
    """Abre a URL no navegador padrão do sistema operacional."""
    webbrowser.open(url)
    
def open_from_filepath(file_path):
    """Open the file in the default text editor according to the operating system"""
    
    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return -1
    
    # Detecta o sistema operacional
    so = platform.system().lower()
    
    try:
        # Define o editor baseado no sistema operacional
        if so == "linux" or so == "darwin":  # Linux ou macOS
            subprocess.Popen(["xdg-open", file_path])  # Usado no Linux e macOS
        elif so == "windows":  # Windows
            subprocess.Popen(["notepad", file_path])  # Notepad para Windows
        else:
            print(f"Operating system not supported for opening files.")
            return -3
        
        print(f"File {file_path} opened with default editor.")
        return 0
    
    except Exception as e:
        print(f"Error trying to open file: {e}")
        return -2

    return 0

def compare_texts(texto1, texto2, program="meld", filetype="txt",suffix1="input",suffix2="output"):
    """
    Compara dois textos utilizando um programa externo de comparação, como o Meld.
    
    Parâmetros:
    texto1 (str): Primeiro texto a ser comparado.
    texto2 (str): Segundo texto a ser comparado.
    program (str, opcional): Nome do programa de comparação de arquivos (padrão: "meld").
    filetype (str, opcional): Extensão do arquivo temporário a ser criado (padrão: "tex").
    
    Retorna:
    None: Apenas abre a ferramenta de comparação de arquivos.
    """
    # Cria arquivos temporários para armazenar os textos
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix="."+suffix1+"."+filetype) as temp1, \
         tempfile.NamedTemporaryFile(delete=False, mode="w", suffix="."+suffix2+"."+filetype) as temp2:
        
        temp1.write(texto1)
        temp2.write(texto2)
        
        temp1_path = temp1.name
        temp2_path = temp2.name

    # Executa o Meld sem bloquear a execução do script
    subprocess.Popen([program, temp1_path, temp2_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

