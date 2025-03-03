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

################################################################################

def load_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

################################################################################

def split_text(texto, max_size=10000, separators=["\n\n", " ", ".", ","]):
    partes = []
    inicio = 0

    while inicio < len(texto):
        if len(texto) - inicio <= max_size:
            partes.append(texto[inicio:])
            break

        fim = inicio + max_size
        melhor_corte = -1
        melhor_sep = ""

        for sep in separators:
            pos = texto.rfind(sep, inicio, fim)
            if pos > melhor_corte:
                melhor_corte = pos
                melhor_sep = sep

        if melhor_corte == -1:
            fim = inicio + max_size  # Corta no limite se nenhum separador for encontrado
        else:
            fim = melhor_corte + len(melhor_sep)  # Inclui o separador no corte

        partes.append(texto[inicio:fim])
        inicio = fim

    return partes
    
################################################################################
import re

EXTENSION = {
    "HTML": "html",
    "Markdown": "md",
    "LaTeX": "tex",
    "TXT": "txt"
}

def detect_formats(texto):
    """Retorna um dicionário com a probabilidade de o texto pertencer a cada formato"""

    formatos = {
        "HTML": 0,
        "Markdown": 0,
        "LaTeX": 0,
        "TXT": 0  # Será usado como complemento caso outros formatos tenham baixa contagem
    }

    # Padrões para cada formato
    padroes = {
        "HTML": [
            r"<\s*(html|body|p|a|div|span|h[1-6]|br|img|table|tr|td|th)[^>]*>"
        ],
        "Markdown": [
            r"(^|\n)(#+\s)",  # Títulos (#)
            r"(^|\n)(\* |\- |\d+\.)",  # Listas (*, -, 1.)
            r"(\*\*.*?\*\*|\*.*?\*)",  # Ênfase (**bold**, *italic*)
            r"(\[.*?\]\(.*?\))",  # Links [text](url)
            r"(\!\[.*?\]\(.*?\))"  # Imagens ![alt](url)
        ],
        "LaTeX": [
            r"\\(documentclass|begin|end|chapter|section|subsection|subsubsection|textsc|textbf|textit|frac|usepackage)",
            r"\$\$.*?\$\$",  # Modo matemático em bloco
            r"\$.*?\$",  # Modo matemático inline
        ]
    }

    # Contar ocorrências de cada padrão
    for formato, regex_list in padroes.items():
        for regex in regex_list:
            ocorrencias = len(re.findall(regex, texto, re.MULTILINE))
            formatos[formato] += ocorrencias

    # Se nenhum formato for identificado, assume-se TXT como 100%
    total_ocorrencias = sum(formatos.values())
    if total_ocorrencias == 0:
        formatos["TXT"] = 1.0
    else:
        # Normaliza os valores para serem probabilidades (soma 1.0)
        for formato in formatos:
            formatos[formato] /= total_ocorrencias

    return formatos
