from app.domain.entity.verse_translation_entity import VerseTranslationEntity
from app.application.service.searcher import Searcher
from sentence_transformers import SentenceTransformer
from typing import List
import faiss
import pickle
import os

class VerseTranslationSearcher(Searcher):
    def __init__(self):
        self.path_prefix = 'data/model/'
        self.model = SentenceTransformer("intfloat/multilingual-e5-base")
        self.index = None
        self.verse_meta: List[VerseTranslationEntity] = []
        
    def builded(self):
        return os.path.exists(self.path_prefix + 'verse.index') \
            and os.path.exists(self.path_prefix + 'verse_meta.pkl')

    def build_index(self, verses: List[VerseTranslationEntity]):
        texts = [f"passage: {v.content}" for v in verses]
        embeddings = self.model.encode(texts, convert_to_numpy=True)

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.verse_meta = verses

        faiss.write_index(self.index, self.path_prefix + 'verse.index')
        with open(self.path_prefix + "verse_meta.pkl", "wb") as f:
            pickle.dump(verses, f)

    def load_index(self):
        self.index = faiss.read_index(self.path_prefix + 'verse.index')
        with open(self.path_prefix + "verse_meta.pkl", "rb") as f:
            self.verse_meta = pickle.load(f)

    def search(self, query: str, top_k=3) -> List[VerseTranslationEntity]:
        query = f"query: {query}"
        q_emb = self.model.encode([query])
        D, I = self.index.search(q_emb, top_k)
        return [self.verse_meta[i] for i in I[0]]