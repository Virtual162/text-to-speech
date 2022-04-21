#事前にpip install経由で必要なsoftware packageはpandasとibm-watsonです。
#もしCSVの代わりにExceファイルを使いたい場合は、openpyxlもpip経由でインストールする必要があります。 

from ast import Or
from asyncio.windows_events import NULL
import json, pandas as pd
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

print('start')
# 認証情報
with open("./auth.json",'r') as auth:
    auth_info = json.load(auth)
    apikey= auth_info['apikey']
    url=auth_info['url']

#Text-to-speech向けのCSVファイルの読み取り、CSVファイルの保存先'CSV OR Excel File Location'を変更してください。
#もしExcelファイルを使いたい場合は、事前にPip install openpyxlをインストールし、以下の「pd.read_csv」を「pd.read_excel」に切り替えて、Excelファイルの保存先を入力してください。
TTS_Dataset = pd.read_csv(r'CSV OR Excel File Location'', header= 'infer')
#データセットの行数の確認
df = TTS_Dataset
length =len(TTS_Dataset)
print(length)
#データセットの最初の５行の確認（ヘッダー付き）
print(TTS_Dataset.head())

#オーディオファイル名欄の入力と確認（行数に合わせて出力されるオーディオファイル名が作成されます。）
df.insert(0,"AudioFileName",[f'audio{i}.mp3' for i in range(1, len(df) + 1)])
print(TTS_Dataset.head())

#setup service  
authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

# 音声に変換したい文章とデータ確認
for x in range(length):
    #print(df.Text[x])
    if df.Text[x].isdigit() == True:
        print("ERROR:テキスト桁に数字が入っています。再度確認してください。")
        break
    if df.AudioFileName[x] == NULL  or not df.AudioFileName[x].endswith(('.mp3')):
        print('ERROR:出力するオーディオファイル名が記載されていないか、「.mp3」フォーマットがファイル名に入っていません')
        break
    # 音声ファイル作成。音声の言語と発音を変えたい場合は「voice='○○'」パラメーターをWatson Text To Speechの言語のオプションから選んで変更する事ができます。
    # Watson Text To Speech対処言語リストURL：https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-voices
    with open(df.AudioFileName[x], 'wb') as audio_file: 
        res = tts.synthesize(df.Text[x], accept='audio/mp3', voice='ja-JP_EmiV3Voice').get_result()
        audio_file.write(res.content)
        print("入力データの「"+ df.Text[x] + "」用のファイルを作成中")
#完成してファイルはユーザーの/Docments/text-to-speech-main/フォルダーに保存されます。
print("全てのオーディオファイルは「text-to-speech-main」フォルダーに保存されています。これでスクリプトは終了になります。")
