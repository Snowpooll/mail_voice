# mail_voice
Read unread Gmail text with URL removed. If there is a link in the text, open it with selenium and download the PDF.

特別支援学校のお知らせがCocooによりメールで送られてくるため  
Gmailでラベルを作成し、未読のメールを読み上げるようにしています。  
メール内の本文をvoicevox で読み上げ、  
文章内にURLがある場合 selenimでダウンロードし  
PDFの文字数が１００文字以下なら読み上げ、  
それ以上ならPDFを確認するように音声が流れます。

## 動作環境
M1 MacbookAir 16GB で動作しています、  

音声の作成に voicevox の docker が必要になります  
`docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest`  
で取得しています

動作させるには

バックグランドでの起動で
-d オプションをつけて  
`docker run -d  -p '192.168.1.69:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest`  
というように起動させます  
IPアドレス部分はご自身のマシンのIPに変えてください
