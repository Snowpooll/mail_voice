import fitz
from playsound import playsound
import configparser
import subprocess
import pygame
import time

# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read('config.ini')
server_ip = config['Settings']['server_ip']
label_id = config['Settings']['label_id']
notification_sound = config['Settings']['notification_sound']
pdf_notification_sound = config['Settings']['pdf_notification_sound']


# テキストから音声を生成して再生する関数
def generate_and_play_audio_from_text(text):
    command_json = [
        "curl", "-s", "-X", "POST",
        f"http://{server_ip}/audio_query?speaker=1",
        "--get", "--data-urlencode", f"text={text}"
    ]
    command_audio = [
        "curl", "-s", "-H", "Content-Type: application/json", "-X", "POST",
        "-d", "@query.json", f"http://{server_ip}/synthesis?speaker=1"
    ]
    with open('query.json', 'w') as file:
        subprocess.run(command_json, stdout=file)
    with open('audio_output.wav', 'wb') as file:
        subprocess.run(command_audio, stdout=file)
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound("audio_output.wav")
    sound.play()
    while pygame.mixer.get_busy():
        time.sleep(0.1)

# PDFファイルから文字数をカウントする関数
def count_pdf_characters(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return len(text)

# メールの処理を行う関数
def process_email(service, label_id):
    from gmail_utils import gmail_get_latest_unread_message_body
    from pdf_downloader import find_preview_link, download_pdf

    body, urls = gmail_get_latest_unread_message_body(service, label_id)
    if body:
        # playsound('notice.wav')
        playsound(notification_sound)
        generate_and_play_audio_from_text(body)
        if urls:
            for url in urls:
                preview_url = find_preview_link(url)
                if preview_url:
                    download_pdf(preview_url, "downloaded_file.pdf")
                    char_count = count_pdf_characters("downloaded_file.pdf")
                    if char_count >= 100:
                        # playsound('notice_pdf.wav')
                        playsound(pdf_notification_sound)
                else:
                    print("プレビューリンクが見つかりませんでした。")
        else:
            print("メールにURLが見つかりませんでした。")
    else:
        print("未読メールはありません。")
