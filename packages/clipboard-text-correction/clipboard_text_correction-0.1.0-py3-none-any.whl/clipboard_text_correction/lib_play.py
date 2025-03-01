#!/usr/bin/python3

from gtts import gTTS
from playsound import playsound
import tempfile


def play_message(texto, lang="en"):
    # Cria um arquivo temporário para o MP3
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        caminho_temp = temp_audio.name  # Obtém o caminho do arquivo temporário

    # Gera o áudio e salva no arquivo temporário
    tts = gTTS(texto, lang=lang)
    tts.save(caminho_temp)

    # Reproduz o áudio
    playsound(caminho_temp)
