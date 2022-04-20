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

#Text-to-speech向けのCSVファイルの読み取り。CSVファイルの保存先"CSV Location"を変更してください
TTS_Dataset = pd.read_csv("CSV Location", header= 'infer')
print(TTS_Dataset.head())

#setup service
authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

# 音声に変換したい文章とデータ確認
df = TTS_Dataset
length =len(TTS_Dataset)
print(length)
TextDataList = df.Text
for x in range(length):
    print(df.Text[x])
    if df.Text[x].isdigit() == True:
        print('ERROR:テキスト桁に数字が入っています。再度確認してください。')
        break
    if df.AudioFileName[x] == NULL  or not df.AudioFileName[x].endswith(('.mp3')):
        print('ERROR:出力するオーディオファイル名が記載されていないか、「.mp3」フォーマットがファイル名に入っていません')
        break
    # 音声ファイル作成
    with open(df.AudioFileName[x], 'wb') as audio_file:  #expected str, bytes or os.PathLike object, not list
        res = tts.synthesize(df.Text[x], accept='audio/mp3', voice='ja-JP_EmiV3Voice').get_result()
        audio_file.write(res.content)
        # Windowsでは完成してファイルはユーザーの/Docments/text-to-speech-main/フォルダーに保存されます。
        print('全てのオーディオファイルは「text-to-speech-main」フォルダーに保存されています。')
print('end')
