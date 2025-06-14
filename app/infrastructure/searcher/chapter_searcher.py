from app.domain.entity.chapter_entity import ChapterEntity
from app.application.service.searcher import Searcher
from sentence_transformers import SentenceTransformer
from typing import List
import faiss
import pickle
import os

class ChapterSearcher(Searcher):
    def __init__(self):
        self.path_prefix = 'data/model/'
        self.model = SentenceTransformer("intfloat/multilingual-e5-base")
        self.index = None
        self.chapter_meta: List[ChapterEntity] = []
        
    def builded(self):
        return os.path.exists(self.path_prefix + 'chapter.index') \
            and os.path.exists(self.path_prefix + 'chapter_meta.pkl')

    def build_index(self, chapters: List[ChapterEntity]):
        texts = [f'BAB {v.chapter_number} - Nama {v.name} - Ringkasan {v.summary}' for v in chapters]
        embeddings = self.model.encode(texts, convert_to_numpy=True)

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.chapter_meta = chapters

        faiss.write_index(self.index, self.path_prefix + 'chapter.index')
        with open(self.path_prefix + 'chapter_meta.pkl', "wb") as f:
            pickle.dump(chapters, f)

    def load_index(self):
        self.index = faiss.read_index(self.path_prefix + 'chapter.index')
        with open(self.path_prefix + 'chapter_meta.pkl', "rb") as f:
            self.chapter_meta = pickle.load(f)

    def search(self, query: str, top_k=3) -> List[ChapterEntity]:
        q_emb = self.model.encode([query])
        D, I = self.index.search(q_emb, top_k)
        return [self.chapter_meta[i] for i in I[0]]