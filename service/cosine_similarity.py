import numpy as np

class similarity:
    def cosine_similarity(self, query_vec, rows, top_k: int = 5):
        if not rows:
            return []

        q = np.asarray(query_vec, dtype=np.float32)
        m = np.asarray([r.embeded_chunk for r in rows], dtype=np.float32)

        sims = (m @ q) / (np.linalg.norm(m, axis=1) * np.linalg.norm(q) + 1e-10)
        best = np.argsort(sims)[::-1][:top_k]

        return [(rows[i], float(sims[i])) for i in best]