import os
import pickle
from typing import List

import faiss
from sentence_transformers import SentenceTransformer

from app.application.service.searcher import Searcher
from app.domain.entity.gita_entity import GitaEntity


class GitaSearcher(Searcher):
    def __init__(self):
        self.path_prefix = "data/model/"
        self.model = SentenceTransformer("intfloat/multilingual-e5-base")
        self.index = None
        self.verse_meta: List[GitaEntity] = []

    def builded(self):
        return os.path.exists(self.path_prefix + "gita.index") and os.path.exists(
            self.path_prefix + "gita_meta.pkl"
        )

    def build_index(self, gita: List[GitaEntity]):
        print(gita)
        texts = [f"passage: {v.vt_content}" for v in gita]
        embeddings = self.model.encode(texts, convert_to_numpy=True)

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.verse_meta = gita

        faiss.write_index(self.index, self.path_prefix + "gita.index")
        with open(self.path_prefix + "gita_meta.pkl", "wb") as f:
            pickle.dump(gita, f)

    def load_index(self):
        self.index = faiss.read_index(self.path_prefix + "gita.index")
        with open(self.path_prefix + "gita_meta.pkl", "rb") as f:
            self.verse_meta = pickle.load(f)

    def search(self, query: str, top_k=3) -> List[GitaEntity]:
        query = f"query: {query}"
        q_emb = self.model.encode([query])
        D, I = self.index.search(q_emb, top_k)

        seen_id = []
        output = []
        for i in I[0]:
            meta = self.verse_meta[i]
            meta_key = f"{meta.c_chapter_number}-{meta.v_verse_number}"
            if meta_key not in seen_id:
                seen_id.append(meta_key)
                output.append(self.verse_meta[i])

        return output
