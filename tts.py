pip install ibm-watson
pip install pandas
import json, pandas as pd
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

print('start')
# 認証情報
with open("./auth.json",'r') as auth:
    auth_info = json.load(auth)
    apikey= auth_info['apikey']
    url=auth_info['url']

#Text-to-speech向けのCSVファイルの読み取り
TTS_Dataset = pd.read_csv("filepath or URL")
TTS_TextData= pd.DataFrame(data=TTS_Dataset, columns=['Text', 'AudioFileName'])
if TTS_TextData['Text'].str == True:
    print ("テキストデータに文字以外の物はありません")　#Text only contains str values

# 音声に変換したい文章
text='ちなみに、先ほど探していたのは、こちらの資料でしょう。'

# setup service
authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

# 音声ファイル作成
# Windowsでは完成してファイルはユーザーの/Docments/text-to-speech-main/フォルダーに保存されます。
with open('./audio.mp3', 'wb') as audio_file: 　# audio file name should match the name in the \
    # 'AudioFileName' column for each row of data in the 'text column'
    res = tts.synthesize(text, accept='audio/mp3', voice='ja-JP_EmiV3Voice').get_result()
    audio_file.write(res.content)
    print("全てのオーディオファイルはユーザーの/Docments/text-to-speech-main/フォスターに保存されています。")

