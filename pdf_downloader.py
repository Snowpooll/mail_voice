from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def find_preview_link(url, link_text="プレビュー"):
    driver = webdriver.Safari()  # またはChrome(), Firefox() など、使用するブラウザに合わせて変更
    try:
        driver.get(url)
        driver.implicitly_wait(10)  # 秒
        preview_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, link_text))
        )
        return preview_link.get_attribute('href')
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None
    finally:
        driver.quit()

def download_pdf(url, file_path="downloaded_file.pdf"):
    if url:
        print("プレビューリンク:", url)
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print("ファイルが正常にダウンロードされました。")
        else:
            print("ファイルのダウンロードに失敗しました。ステータスコード:", response.status_code)
    else:
        print("プレビューリンクが見つかりませんでした。")

