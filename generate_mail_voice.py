import subprocess
import pygame
import time

def generate_and_play_audio_from_text(file_path):
    # テキストファイルからテキストを読み込む
    with open(file_path, 'r') as file:
        text = file.read()

    # JSONファイルを作成するためのcurlコマンド
    command_json = [
        "curl", "-s", "-X", "POST",
        "http://{server_ip}/audio_query?speaker=1",
        "--get", "--data-urlencode", f"text={text}"
    ]

    # 音声ファイルを作成するためのcurlコマンド
    command_audio = [
        "curl", "-s", "-H", "Content-Type: application/json", "-X", "POST",
        "-d", "@query.json", "http://{server_ip}/synthesis?speaker=1"
    ]

    # JSONファイルと音声ファイルを作成
    with open('query.json', 'w') as file:
        subprocess.run(command_json, stdout=file)
    with open('audio_output.wav', 'wb') as file:
        subprocess.run(command_audio, stdout=file)

    # Pygameで音声ファイルを再生
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound("audio_output.wav")
    sound.play()
    while pygame.mixer.get_busy():
        time.sleep(0.1)

# email_body.txtから音声を生成して再生
generate_and_play_audio_from_text('email_body.txt')
