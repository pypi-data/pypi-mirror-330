# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 11:23:51 2025
@author: Yoichi Takenaka
"""
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
#%%
class DeBERTaEmotionPredictor:
    """
    DeBERTa を用いて日本語テキストの感情推定を行うクラスです。
    8つの感情（Joy, Sadness, Anticipation, Surprise, Anger, Fear, Disgust, Trust）
    に対する学習済みモデルを用いて、入力テキストの推論結果（推定ラベルと
    肯定クラスの確信度）をDataFrame形式で返します。
    """
    
    def __init__(self, model_dir="models", em_list=None, device=None):
        # 使用デバイスの設定
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        self.cpu_device = torch.device("cpu")
        
        # 感情リスト（指定がなければデフォルトの8感情を使用）
        if em_list is None:
            self.em_list = ["Joy", "Sadness", "Anticipation", "Surprise", 
                            "Anger", "Fear", "Disgust", "Trust"]
        else:
            self.em_list = em_list

        # 英語の感情名と日本語の対応表
        self.emotion_translation = {
            "Joy": "喜び",
            "Sadness": "悲しみ",
            "Anticipation": "期待",
            "Surprise": "驚き",
            "Anger": "怒り",
            "Fear": "恐れ",
            "Disgust": "嫌悪",
            "Trust": "信頼"
        }


        # Hugging Face Hubのユーザー名
        self.username = "YoichiTakenaka"
                        
        # トークナイザーとモデルのロード
        self.tokenizer, self.models = self._load_models()
    
    def _load_models(self):
        """
        共通トークナイザーと、各感情の学習済みモデルをロードする内部メソッド。
        各モデルは初期状態では CPU に配置し、推論時にGPUへ移動します。
        """
        tokenizer_repo = f"{self.username}/deverta-v3-japanese-large-Joy"        
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_repo)

        models = {}
        for i,em in enumerate(self.em_list):
            print(f"Start Donloading... {em}  {i+1}/{len(self.em_list)}")
            
            model_repo = f"{self.username}/deverta-v3-japanese-large-{em}"
            model = AutoModelForSequenceClassification.from_pretrained(model_repo)            
            model.to(self.cpu_device)
            model.eval()
            models[em] = model
        return tokenizer, models

    def predict_emotions(self, texts, max_length=128):
        """
        入力テキスト（単一文字列、リスト、またはpandas Series）に対して
        8感情の推論を一括で実施し、結果をDataFrameとして返すメソッドです。
        
        出力DataFrameは各行が1文に対応し、列は次の順序になります：
          "text" → 各感情の predicted_label → 各感情の positive_probability
        
        Parameters:
            texts (str or list[str] or pandas.Series): 推論対象のテキスト
            max_length (int): トークン化時の最大長（デフォルト128）
        
        Returns:
            pandas.DataFrame: 推論結果をまとめたDataFrame
        """
        # 単一文字列の場合はリストに変換
        if isinstance(texts, str):
            texts = [texts]
        # pandas Seriesの場合はリストに変換
        elif hasattr(texts, 'tolist'):
            texts = texts.tolist()
        
        # すべてのテキストを一括でトークナイズし、GPUに転送
        encodings = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
        encodings = {key: val.to(self.device) for key, val in encodings.items()}
        
        # 結果を保持するDataFrameの初期化
        df = pd.DataFrame({"text": texts})
        
        # 各感情モデルについて一括推論を実施
        for em in self.em_list:
            print(f"感情：{em} の推論を開始")
            model = self.models[em]
            model.to(self.device)
            with torch.no_grad():
                outputs = model(**encodings)
                probs = F.softmax(outputs.logits, dim=-1)
                predicted_labels = torch.argmax(probs, dim=-1).cpu().numpy().tolist()
                positive_probs = probs[:, 1].cpu().numpy().tolist()
            
            # 結果をDataFrameに追加
            df[f"{em}_predicted_label"] = predicted_labels
            df[f"{em}_positive_probability"] = positive_probs
            
            model.to(self.cpu_device)
            torch.cuda.empty_cache()
        
        # 列順を "text" → 各感情の predicted_label → 各感情の positive_probability に並べ替え
        ordered_columns = ["text"]
        for em in self.em_list:
            ordered_columns.append(f"{em}_predicted_label")
        for em in self.em_list:
            ordered_columns.append(f"{em}_positive_probability")
        
        return df[ordered_columns]
    
    def show_emotions(self, df: pd.DataFrame) -> None:
        """
        DataFrame から感情ラベルが 1 である感情を抽出し、テキストごとの感情を表示するメソッド。
        """
        predicted_cols = [col for col in df.columns if col.endswith('_predicted_label')]
        emotion_names = [col.replace('_predicted_label', '') for col in predicted_cols]
        
        for idx, row in df.iterrows():
            text = row['text']
            emotions = [self.emotion_translation[emotion] for emotion, col in zip(emotion_names, predicted_cols) if row[col] == 1]
#            emotions = [emotion for emotion, col in zip(emotion_names, predicted_cols) if row[col] == 1]
            emotions_str = ", ".join(emotions) if emotions else "nan"
            print(f"{text}: {emotions_str}")    
    

# __main__ 部分はデバッグや直接実行時のテスト用
if __name__ == "__main__":
    # クラスのインスタンスを生成 
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
    #感情の推定
    df_result = predictor.predict_emotions(sample_texts)
    
    predictor.show_emotions(df_result)
    #データフレームには各感情の有無、そしてsoftmax関数による確率値が格納されています
    print(df_result)

