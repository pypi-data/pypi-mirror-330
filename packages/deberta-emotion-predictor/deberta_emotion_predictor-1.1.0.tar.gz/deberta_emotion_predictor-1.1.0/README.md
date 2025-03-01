# DeBERTa Emotion Predictor

This package provides a DeBERTa-based model for predicting emotions in Japanese text.


DeBERTa Emotion Predictor は、ファインチューニング済みの DeBERTa モデルを用いて日本語テキストの感情推定を行う Python パッケージです。8 つの感情（Joy, Sadness, Anticipation, Surprise, Anger, Fear, Disgust, Trust）に対するそれぞれのモデルを利用し、各テキストに対する感情の予測ラベルと肯定クラスの確信度を簡単に取得できます。

## Install(インストール)

pip を使います。

```bash
pip install deberta-emotion-predictor
```

##　Usage (おためし利用)

```python
from deberta_emotion_predictor import DeBERTaEmotionPredictor
predictor = DeBERTaEmotionPredictor()
result = predictor.predict_emotions("今日はとても嬉しい！")
predictor.show_emotions(result)
```

注）Hugging-face から８種類のDeBERTaをダウンロードするため、初回起動に大変時間がかかります。二回目以降の実行から速くなります。

データフレームも入力できます。

```python
import pandas as pd
from deberta_emotion_predictor import DeBERTaEmotionPredictor

# model_dir は、言語モデルとトークナイザがある場所を指しています
predictor = DeBERTaEmotionPredictor()

# サンプルテキスト（リスト形式）
sample_texts = [
    "そうだ 京都、行こう。",
    "がんばるひとの、がんばらない時間。",
    "わたしらしくをあたらしく",
    "ピースはここにある。",
    "結婚しなくても幸せになれるこの時代に、私は、あなたと結婚したいのです。",
    "これからの地球のために一肌、脱ぎました。",
    "自分は、きっと想像以上だ。",
    "ハローしあわせ。",
    "日本を、1枚で。"
]
res_df = predictor.predict_emotions(sample_texts)

predictor.show_emotions(res_df)
```

なお動作には torch, transformers, pandas　が必要です。

```bash
pip install torch 
pip install transformers
pip install pandas 
```

また、GPUを使用するには、NVIDIA GPUドライバー等のインストールが必要です。
こちらは、他の資料を参照してください。


## 特徴

- **８感情の推定**  
  各感情ごとにファインチューニング済みのモデルを利用し、テキストの感情推定を行います。

- **柔軟な入力形式**  
  単一のテキスト、テキストのリスト、または pandas Series を入力として受け付け、結果を DataFrame 形式で返します。

- **効率的な推論**  
  GPU メモリの使用量を抑えるため、必要なときだけモデルを GPU にロードする設計になっています。


## 使用方法

以下は、パッケージの基本的な使い方の例です:


### テキストの渡し方(リスト)
```python
sample_texts = [
    "そうだ 京都、行こう。",
    "がんばるひとの、がんばらない時間。"
]
result_df = predictor.predict_emotions(sample_texts)
predictor.show_emotions(result_df)
```

### 単一のテキストの場合
```python
result_single = predictor.predict_emotions("新しい朝が来た。")
print(result_single)
```

### 出力されるデータフレーム

出力されるデータフレームには、各感情の有無をあらわす８つの列、及び各感情の確率値が格納されています。

```python
print(result_df)
```

## ディレクトリ構成
```
deberta_emotion_predictor/         
├── README.md                      # この説明ファイル
├── deberta_emotion_predictor.py   # DeBERTaEmotionPredictor クラスの実装
│   └── tokenizer_DeBERTa_v3_large/ #トークナイザー
├── setup.py
├── pyproject.toml
├── README.md
├── LICENSE
└── usage.py                       
```
## 必要環境
- Python 3.6 以上
- PyTorch
- transformers
- pandas

## License
Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

Copyright (c) 2025 Yoichi Takenaka

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License.
To view a copy of this license, visit https://creativecommons.org/licenses/by-sa/4.0/

This project is based on:
- DeBERTa (https://huggingface.co/microsoft/deberta-v3-large), licensed under the MIT License.
- DeBERTa Japanese Model (https://huggingface.co/globis-university/deberta-v3-japanese-large), licensed under the CC BY-SA 4.0 License.

Any modifications or derivative works must also be distributed under the same CC BY-SA 4.0 License.


