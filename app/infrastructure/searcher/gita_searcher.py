import os
import pickle
from typing import List, Tuple

import faiss
from sentence_transformers import SentenceTransformer

from app.application.service.searcher import Searcher
from app.domain.entity.gita_entity import GitaEntity, MixedGitaEntity


class GitaSearcher(Searcher):
    def __init__(self):
        self.path_prefix = "data/model/"
        self.model = SentenceTransformer("intfloat/multilingual-e5-large")
        self.index = None
        self.verse_meta: List[GitaEntity | MixedGitaEntity] = []

    def builded(self):
        return os.path.exists(self.path_prefix + "gita.index") and os.path.exists(
            self.path_prefix + "gita_meta.pkl"
        )

    def build_index(self, gita: List[GitaEntity]) -> bool:
        texts = [
            f"passage: Bab {v.c_chapter_number} sloka {v.v_verse_number} mengatakan {v.vt_content}"
            for v in gita
        ]
        mixed_chunks, mixed_objects = self.chunk_verses(gita)
        texts += mixed_chunks
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.verse_meta = gita + mixed_objects

        faiss.write_index(self.index, self.path_prefix + "gita.index")
        with open(self.path_prefix + "gita_meta.pkl", "wb") as f:
            pickle.dump(self.verse_meta, f)

        return True

    def load_index(self) -> bool:
        self.index = faiss.read_index(self.path_prefix + "gita.index")
        with open(self.path_prefix + "gita_meta.pkl", "rb") as f:
            self.verse_meta = pickle.load(f)

        return True

    def search(self, query: str, top_k=3) -> List[GitaEntity | MixedGitaEntity]:
        query = f"query: {query}"
        q_emb = self.model.encode([query])
        D, I = self.index.search(q_emb, top_k)

        if D[0][0] > 0.44:
            return []

        seen_id = []
        output = []
        for i in I[0]:
            meta = self.verse_meta[i]
            meta_key = ""
            if isinstance(meta, MixedGitaEntity):
                meta_key = meta.label
            else:
                meta_key = f"{meta.c_chapter_number}-{meta.v_verse_number}"

            if meta_key not in seen_id:
                seen_id.append(meta_key)
                output.append(self.verse_meta[i])

        return output

    def chunk_verses(
        self, gita: List[GitaEntity], size: int = 3
    ) -> Tuple[List[str], List[MixedGitaEntity]]:
        chunks = []
        objects = []
        for i in range(0, len(gita), size):
            group = gita[i : i + size]
            text = "; ".join(
                [
                    f"BG {v.c_chapter_number}.{v.v_verse_number} - {v.vt_content}"
                    for v in group
                ]
            )
            chunks.append("passage: " + text)
            objects.append(
                MixedGitaEntity(
                    label="-".join("BG{v.c_chapter_number}.{v.v_verse_number}"),
                    gita=group,
                )
            )
        return chunks, objects
