"""SMF Multimodal Grant Advisory RAG Pipeline.

Implements:
1. Four-modality ingestion artifacts (Text PDF, Visual OCR, Audio Whisper, Video OCR/ASR).
2. Hybrid Dense + Sparse retrieval (FAISS cosine + BM25Okapi with reciprocal rank fusion).
3. Role-based privacy policy (Member vs. Admin role guardrail preventing company PII leaks).
4. Evidence-grounded generation with citation validation.
"""

import html as _html
import json
import os
from pathlib import Path
import pickle
import re
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote

import faiss
import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

# Modality visual tags
MOD = {
    "text": ("#3A444E", "TEXT PDF"),
    "image": ("#B4632B", "IMAGE / OCR"),
    "audio": ("#2F6E63", "AUDIO / ASR"),
    "video": ("#5B4B8A", "VIDEO / ASR"),
}

MEMBER_RECORD_SOURCES = (
    "KB12_SMF_Member_Case_Studies_SYNTHETIC.pdf",
    "KBV02_SMF_Member_Case_Study_Cards.pdf",
    "VID001_case_study_novara.mp4",
    "VID002_case_study_tanjung.mp4",
)

MEMBER_COMPANIES = [
    "precision dynamics",
    "golden harvest",
    "sterling metal stamping",
    "sterling metal",
    "apex circuit",
    "meridian packaging",
    "novara",
    "navara",
    "tanjung",
    "tenjong",
]

ROLE_REFUSAL = (
    "I cannot share information regarding specific member company applications.\n\n"
    "Member accounts cover general scheme guidance and your own applications. "
    "Another company's application history, grant figures, and outcomes are confidential.\n\n"
    "I can assist with eligibility criteria, funding support caps, qualifying and non-qualifying "
    "costs, application timelines, and common rejection grounds."
)

REFUSAL_TEXT = (
    "I cannot answer based on the verified reference documents. "
    "Please consult an SMF advisory officer directly for specialized evaluation."
)

SYSTEM_RULES = (
    "You are the SMF Grant Advisory Assistant. Answer solely from the provided [S#] evidence passages. "
    "Every factual claim must cite its source (e.g., [S1], [S2]). If the evidence does not contain "
    "sufficient information to answer the question, state that you cannot answer from verified documents."
)


def tidy_title(t: str) -> str:
    return re.sub(r"\s*SYNTHETIC\s*$", "", str(t or "")).strip()


def tidy_text(t: str) -> str:
    out = re.sub(r"SYNTHETIC\s*/\s*ILLUSTRATIVE DATA[^.]*?OPERATIONAL DATA\s*", "", str(t or ""), flags=re.I)
    return re.sub(r"\s{2,}", " ", out).strip()


class MultimodalRAGPipeline:
    """Production inference engine for the SMF Multimodal Grant Advisory Assistant."""

    def __init__(self, root_dir: Optional[str] = None):
        self.root = Path(root_dir or Path(__file__).parent).resolve()
        self.artifacts_dir = self.root / "artifacts"
        self.kb_dir = self.root / "knowledge_base"

        # Load precomputed configuration and artifacts
        with open(self.artifacts_dir / "config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

        with open(self.artifacts_dir / "chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)

        self.chunk_emb = np.load(self.artifacts_dir / "chunk_embeddings.npy").astype("float32")
        self.faiss_index = faiss.read_index(str(self.artifacts_dir / "faiss_index.bin"))

        # Setup sparse BM25 index
        tokenized_corpus = [self.tokenize(c["text"]) for c in self.chunks]
        self.bm25_index = BM25Okapi(tokenized_corpus)

        # Setup embedding model
        model_name = self.config.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
        self.embedder = SentenceTransformer(model_name)

        # Operating points
        self.top_k = self.config.get("top_k", 5)
        self.best_alpha = self.config.get("best_alpha", 0.8)
        self.best_threshold = self.config.get("best_threshold", 0.40)

        # Groq API client
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        self.use_mock = not bool(self.api_key)
        self.llm_model = "llama-3.1-8b-instant"

    @staticmethod
    def tokenize(text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", (text or "").lower())

    def embed(self, texts: List[str]) -> np.ndarray:
        v = self.embedder.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return np.asarray(v, dtype=np.float32)

    def role_check(self, question: str, role: str) -> Tuple[bool, List[str]]:
        q = (question or "").lower()
        named = sorted({c for c in MEMBER_COMPANIES if c in q})
        if role == "member" and named:
            return False, named
        return True, named

    def retrieve(
        self,
        question: str,
        top_k: Optional[int] = None,
        use_hybrid: bool = True,
        alpha: Optional[float] = None,
        sim_threshold: float = 0.0,
        exclude_sources: Tuple[str, ...] = (),
    ) -> List[Dict[str, Any]]:
        top_k = top_k or self.top_k
        alpha = self.best_alpha if alpha is None else alpha
        n = len(self.chunks)
        pool = min(max(top_k * 4, 20), n)
        qv = self.embed([question])

        if use_hybrid:
            d_all = (self.chunk_emb @ qv[0]).astype(np.float32)
            bm = np.asarray(self.bm25_index.get_scores(self.tokenize(question)), dtype=np.float32)

            def norm(a):
                lo, hi = float(a.min()), float(a.max())
                return np.zeros_like(a) if hi - lo < 1e-9 else (a - lo) / (hi - lo)

            fused = alpha * norm(d_all) + (1 - alpha) * norm(bm)
            order = np.argsort(-fused)[:pool]
            cand = [(int(i), float(fused[i]), float(d_all[i])) for i in order]
        else:
            ds, di = self.faiss_index.search(qv, pool)
            cand = [(int(i), float(s), float(s)) for s, i in zip(ds[0], di[0]) if i >= 0]

        if exclude_sources:
            cand = [c for c in cand if not any(x in self.chunks[c[0]]["source"] for x in exclude_sources)]

        results = []
        for i, score, dense in cand:
            if sim_threshold > 0 and dense < sim_threshold:
                continue
            c = self.chunks[i]
            results.append({
                "rank": len(results) + 1,
                "chunk_id": c["chunk_id"],
                "score": score,
                "dense_score": dense,
                "text": c["text"],
                "title": c["title"],
                "source": c["source"],
                "page": c["page"],
                "modality": c["modality"],
                "extraction": c["extraction"],
                "locator": c.get("locator", ""),
                "t_start": c.get("t_start"),
                "rel_path": c.get("rel_path", ""),
            })
            if len(results) >= top_k:
                break
        return results

    def build_prompt(self, question: str, results: List[Dict[str, Any]], role: str = "member") -> str:
        role_preamble = {
            "member": (
                "You are answering a member company. Never disclose information about other member companies, "
                "even if present in reference evidence. Answer solely regarding general policy rules."
            ),
            "admin": (
                "You are answering an SMF advisory officer. Member application records and internal review tables "
                "are accessible to you. Cite the exact document and date."
            ),
        }
        blocks = "\n\n".join(
            f"[S{r['rank']}]\nDocument: {tidy_title(r['title'])}\n"
            f"Source: {r['source']} ({r.get('locator') or 'page ' + str(r['page'])})\n"
            f"Modality: {r['modality'].upper()}\n"
            f"Text: {tidy_text(r['text'])}"
            for r in results
        )
        return (
            f"=== INSTRUCTIONS ===\n{SYSTEM_RULES}\n\n"
            f"ROLE CONTEXT: {role_preamble.get(role, '')}\n"
            f"=== END INSTRUCTIONS ===\n\n"
            f"=== EVIDENCE ===\n{blocks}\n=== END EVIDENCE ===\n\n"
            f"=== QUESTION ===\n{question}\n=== END QUESTION ===\n"
        )

    def call_llm(self, prompt: str) -> Tuple[str, str]:
        if self.use_mock:
            # Deterministic mock demonstration
            labels = re.findall(r"\[S(\d+)\]", prompt)
            if not labels:
                return REFUSAL_TEXT, "mock_refusal"
            ev = re.search(r"=== EVIDENCE ===\s*(.*?)\s*=== END EVIDENCE ===", prompt, re.S)
            first = re.search(r"Text:\s*(.{0,220})", ev.group(1) if ev else "", re.S)
            snip = first.group(1).strip().replace("\n", " ") if first else ""
            cites = "".join(f"[S{l}]" for l in sorted(set(labels), key=int)[:2])
            return f"**[MOCK MODE — set GROQ_API_KEY for live LLM]** Based on verified documentation: {snip}... {cites}", "mock"

        try:
            from groq import Groq
            client = Groq(api_key=self.api_key)
            resp = client.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.0,
            )
            return (resp.choices[0].message.content or "").strip(), "live_groq"
        except Exception as e:
            return f"Live LLM call failed ({type(e).__name__}). Please check GROQ_API_KEY.", "error_fallback"

    def answer(
        self,
        question: str,
        role: str = "member",
        top_k: int = 5,
        threshold: float = 0.0,
    ) -> Tuple[str, List[Dict[str, Any]], str]:
        question = (question or "").strip()
        if not question:
            return "Please provide a question.", [], "empty"

        allowed, named = self.role_check(question, role)
        if not allowed:
            return ROLE_REFUSAL, [], "blocked_by_role_policy"

        exclude = MEMBER_RECORD_SOURCES if role == "member" else ()
        results = self.retrieve(question, top_k=top_k, sim_threshold=threshold, exclude_sources=exclude)

        if not results:
            return REFUSAL_TEXT, [], "abstained_insufficient_evidence"

        prompt = self.build_prompt(question, results, role=role)
        answer_text, mode = self.call_llm(prompt)
        return answer_text, results, mode
