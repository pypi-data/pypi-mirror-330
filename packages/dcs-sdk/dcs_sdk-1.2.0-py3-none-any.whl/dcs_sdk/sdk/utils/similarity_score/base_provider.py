#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import string
from abc import ABC, abstractmethod
from collections import defaultdict

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from dcs_sdk.sdk.config.config_loader import SimilarityConfig

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")


class SimilarityScoreProvider(ABC):
    def preprocess_text(self, text: str, methods: list[str]) -> set:
        """Applies preprocessing steps dynamically before tokenization."""
        if "lower_case" in methods:
            text = text.lower()
        if "remove_punctuation" in methods:
            text = text.translate(str.maketrans("", "", string.punctuation))
        if "remove_stop_words" in methods:
            stop_words = set(stopwords.words("english"))
            text = " ".join(word for word in text.split() if word not in stop_words)
        if "remove_extra_whitespaces" in methods:
            text = " ".join(text.split())

        tokens = set(word_tokenize(text))
        return tokens

    @abstractmethod
    def fuzzy_match(self, str1: set, str2: set) -> float:
        """Computes a similarity score between two sets of tokens."""
        pass

    def add_text_similarity(self, key: str, data: dict, fields: list, similarity: SimilarityConfig):
        """Adds text similarity scores for the given fields inside the meta dictionary
        and determines if they are a match based on the threshold."""

        grouped_data = defaultdict(list)
        for item in data:
            grouped_data[item[key]].append(item)

        for _, items in grouped_data.items():
            if len(items) == 2:
                source, target = items

                source.setdefault("meta", {}).setdefault("scores", {})
                target.setdefault("meta", {}).setdefault("scores", {})

                for field in fields:
                    source_text = self.preprocess_text(source.get(field, ""), similarity.pre_processing)
                    target_text = self.preprocess_text(target.get(field, ""), similarity.pre_processing)
                    similarity_score = self.fuzzy_match(source_text, target_text)

                    match_status = "match" if similarity_score >= similarity.threshold else "not matched"

                    score_key = f"{field}"
                    source["meta"]["scores"][score_key] = {"score": similarity_score, "status": match_status}
                    target["meta"]["scores"][score_key] = {"score": similarity_score, "status": match_status}

        return data
