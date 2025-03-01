import os
from pathlib import Path
import pandas as pd
import numpy as np
import re
import emoji
import nltk
from nltk.tokenize import word_tokenize
import requests

from airosentris.logger.Logger import Logger


class DataPreprocessor:
    def __init__(self, 
                 stopword_url='https://raw.githubusercontent.com/khanzafa/machine-learning/refs/heads/main/stopword.txt', 
                 kamus_alay_url='https://raw.githubusercontent.com/khanzafa/machine-learning/refs/heads/main/kamus_alay.csv'):
        self.logger = Logger(__name__)
        
        self.stopword_url = stopword_url
        self.kamus_alay_url = kamus_alay_url

        self.logger.info("🚀 Initializing DataPreprocessor...")
        
        nltk.download('punkt', quiet=True)

        self.list_stopwords = self.load_stopwords()
        self.normalize_word_dict = self.load_kamus_alay()

        self.logger.info("✅ DataPreprocessor initialized successfully.")

    def load_stopwords(self):
        """Load stopwords from URL."""
        self.logger.info(f"📥 Fetching stopwords from {self.stopword_url}")
        try:
            response = requests.get(self.stopword_url, timeout=10)
            response.raise_for_status()
            stopwords = response.text.splitlines()
            self.logger.info(f"✅ Stopwords loaded successfully ({len(stopwords)} words).")
            return stopwords
        except requests.RequestException as e:
            self.logger.error(f"❌ Failed to load stopwords: {e}")
            return []

    def load_kamus_alay(self):
        """Load 'kamus alay' from URL and create dictionary."""
        self.logger.info(f"📥 Fetching kamus alay from {self.kamus_alay_url}")
        try:
            response = requests.get(self.kamus_alay_url, timeout=10)
            response.raise_for_status()
            import io
            kamus_alay = pd.read_csv(io.StringIO(response.text))
            normalize_dict = dict(zip(kamus_alay.iloc[:, 0], kamus_alay.iloc[:, 1]))
            self.logger.info(f"✅ Kamus alay loaded successfully ({len(normalize_dict)} entries).")
            return normalize_dict
        except requests.RequestException as e:
            self.logger.error(f"❌ Failed to load kamus alay: {e}")
            return {}

    def repeatchar_clean(self, text):
        """Clean repeated characters using regex."""
        return re.sub(r"(.)\1{2,}", r"\1", text)

    def clean_text(self, text):
        """Cleans text from unnecessary characters."""
        try:
            original_text = text  # Store original for debugging if needed
            text = text.lower()
            text = re.sub(r"\n", " ", text)
            text = emoji.demojize(text)
            text = re.sub(r":[A-Za-z_-]+:", " ", text)
            text = re.sub(r"([xX;:]'?[dDpPvVoO3)(])", " ", text)
            text = re.sub(r"(https?:\/\/\S+|www\.\S+)", "", text)
            text = re.sub(r"@[^\s]+[\s]?", " ", text)
            text = re.sub(r"#(\S+)", r"\1", text)
            text = re.sub(r"[^a-zA-Z,.?!]+", " ", text)
            text = self.repeatchar_clean(text)
            text = re.sub(r"[ ]+", " ", text).strip()

            # self.logger.debug(f"🔹 Cleaned text: '{original_text[:30]}...' → '{text[:30]}...'")  # Show only first 30 chars for preview
            return text
        except Exception as e:
            self.logger.error(f"❌ Error cleaning text: {e}")
            return ""

    def normalize_text(self, text):
        """Normalize text using 'kamus alay'."""
        try:
            tokens = word_tokenize(text)
            normalized_tokens = [self.normalize_word_dict.get(token, token) for token in tokens]
            normalized_text = " ".join(normalized_tokens)

            # self.logger.debug(f"🔹 Normalized text: '{text[:30]}...' → '{normalized_text[:30]}...'")
            return normalized_text
        except Exception as e:
            self.logger.error(f"❌ Error normalizing text: {e}")
            return text

    def preprocess(self, df, clean=True, normalize=True):
        """
        Preprocess dataframe by cleaning and normalizing text.

        Args:
            df (pd.DataFrame): Input dataframe with a 'text' column.
            clean (bool): If True, perform text cleaning.
            normalize (bool): If True, apply text normalization.

        Returns:
            pd.DataFrame: Processed dataframe.
        """
        if not isinstance(df, pd.DataFrame):
            self.logger.error("❌ Input is not a pandas DataFrame.")
            return df
        
        try:
            df_pp = df.copy()
            self.logger.info(f"🛠️ Starting preprocessing on {len(df)} records...")

            if clean:
                self.logger.info("🧼 Cleaning text...")
                df_pp["text"] = pd.Series(df_pp["text"]).apply(self.clean_text)
            
            if normalize:
                self.logger.info("🔄 Normalizing text...")
                df_pp["text"] = pd.Series(df_pp["text"]).apply(self.normalize_text)
            
            # Replace empty texts with NaN and drop
            df_pp["text"] = df_pp["text"].replace("", np.nan)
            df_pp.dropna(subset=["text"], inplace=True)

            self.logger.info(f"✅ Preprocessing complete. Final record count: {len(df_pp)}")
            return df_pp
        except Exception as e:
            self.logger.error(f"❌ Error during preprocessing: {e}")
            return df
