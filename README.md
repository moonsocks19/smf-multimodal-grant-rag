# SMF GRANT ADVISORY ASSISTANT — Multimodal Enterprise RAG

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![Hugging Face Transformers](https://img.shields.io/badge/%F0%9F%A4%97%20Transformers-FFD21E?logoColor=black)
![FAISS](https://img.shields.io/badge/Vector%20Store-FAISS-green)
![Rank-BM25](https://img.shields.io/badge/Lexical%20Search-BM25-yellow)
![Whisper](https://img.shields.io/badge/Audio%2FAudio-Whisper-black)
![Gradio](https://img.shields.io/badge/UI-Gradio-F97316?logo=gradio&logoColor=white)
![Groq](https://img.shields.io/badge/Inference-Groq%20Llama%203.1-F55036)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

A production-grade, four-modality **Retrieval-Augmented Generation (RAG)** assistant designed for
the **Singapore Manufacturing Federation (SMF)**. Built to guide SME manufacturers through complex
Singapore government enterprise schemes (EDG, PSG, MRA, EEG, SkillsFuture, EFS, and the upcoming
EDGE framework), the assistant unifies **Text PDFs**, **Scanned Visual Flowcharts (OCR)**, **Hotline
Audio (Whisper ASR)**, and **Video Case Studies** into a single hybrid retrieval engine.

> *"Is the assistant any good?" is not an operational question.* In government grant advisory,
> evaluation must resolve into three measurable properties: **Knowledgeability** (does it find what
> the corpus knows?), **Faithfulness** (is every single claim traceable to a cited passage?), and
> **Trustworthiness** (is it clean, and silent when it should be?). Signing a commercial contract
> before grant approval violates the commencement rule and costs an SME their entire co-funding, so a
> wrong answer destroys trust while an abstention costs only one phone call.

---

> [!NOTE]
> **Data Privacy & Synthetic Case Study Notice**  
> To protect enterprise member confidentiality under the Personal Data Protection Act (PDPA), company
> case study cards (`KBV02`), testimonial videos, and member records are **curated synthetic data**.
> All government grant advisory notes reflect actual Singapore enterprise schemes and co-funding
> criteria (Enterprise Singapore / Business Grants Portal).

---

## What it does
- 🌐 **Four-Modality Multimodal Corpus** — ingests and indexes across four formats:
  1. *Text PDFs:* Official grant scheme guidelines (EDG, PSG, MRA, EEG, SFEC, EFS, CCP).
  2. *Visual PDFs (OCR):* Scanned utilization reviews, routing flowcharts, rejection audit tables.
  3. *Audio Recordings (Whisper ASR):* Advisory hotline recordings and webinar briefings.
  4. *Video Testimonials (Video OCR + ASR):* Factory case studies with aligned speech and on-screen text.
- 🔍 **Hybrid Dense + Sparse Retrieval** — fuses semantic vectors (`all-MiniLM-L6-v2` via FAISS) with
  lexical keyword scoring (BM25Okapi) using reciprocal rank fusion ($\alpha = 0.8$).
- ⚡ **Cross-Encoder Reranking** — re-scores candidate chunks with `ms-marco-MiniLM-L-6-v2`, achieving
  a **1.000 Hit Rate**, lifting Recall@5 from $0.548 \rightarrow \mathbf{0.618}$, and MRR to $\mathbf{0.917}$.
- 🎯 **Confidence Floor & Controlled Abstention** — enforces an empirical similarity threshold ($0.40$)
  that allows the system to gracefully refuse out-of-domain queries rather than hallucinating figures.
- 📑 **Exact Multimodal Citations** — validates that every generated sentence attributes its claims to
  exact source filenames, page numbers, or audio/video timestamps (`[S1]`, `[S2]`).
- 🛡️ **Role-Based PII Isolation** — features dual operational modes (Public Member vs. Advisory Officer)
  with automatic tripwires preventing leakage of confidential company records.

## Architecture
```
User Query ──▶ [Query Classifier / Expansion]
                         │
                         ▼
             Hybrid Retrieval (k=20)
       ┌─────────────────┴─────────────────┐
       ▼                                   ▼
 [Dense FAISS Search]              [Sparse BM25 Search]
       │                                   │
       └─────────────────┬─────────────────┘
                         ▼
             Reciprocal Rank Fusion (α=0.8)
                         │
                         ▼
         [Cross-Encoder Reranker] (Top-5 Chunks)
                         │
                         ▼
        Confidence Threshold Check (Score >= 0.40?)
               /                     \
             YES                      NO
              ▼                        ▼
    Context-Grounded LLM         Polite Refusal
   (llama-3.1-8b / Qwen2.5)      (Human Escalation)
              │
              ▼
    Attributed Answer with Modality Citations
    [PDF p.2] · [Audio 01:24] · [Video 00:45]
```

## Empirical Benchmark & Experimental Results

Evaluated on an audited 38-question test suite (29 retrieval-scored, 9 behavior-scored across 156 chunks,
57 source units, and 19,851 words):

| Configuration | Hit Rate | P@5 | Recall@5 | R-Norm | MRR | Latency | Key Characteristic |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Baseline (Dense FAISS)** | 0.966 | 0.455 | 0.548 | 0.733 | 0.798 | **7.0 ms** | Fast, but misses specific scheme acronyms |
| **Exp 1: Hybrid (BM25 + FAISS)** | 0.966 | 0.497 | 0.577 | 0.776 | 0.863 | 7.3 ms | Resolves lexical keyword queries |
| **Exp 2: Cross-Encoder Rerank** ★ | **1.000** | 0.510 | **0.618** | **0.806** | **0.917** | 39.5 ms | **Knowledgeability winner** (perfect hit rate) |
| **Exp 3: Rewriting + Threshold (0.40)**| 0.828 | 0.589 | 0.456 | 0.736 | 0.770 | 8.2 ms | Trades recall for correct abstention (0.333) |
| **Exp 4: Combined Pipeline** | 0.862 | **0.607** | 0.551 | 0.792 | 0.862 | 41.2 ms | **Trustworthiness winner** (1.000 clean compliance) |

*(Citation validity: **1.000** across all evaluated configurations).*

## Run it
Requires **Python 3.10 – 3.12**.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

- **Precomputed artifacts included:** FAISS indices (`artifacts/faiss_index.bin`), chunk embeddings
  (`artifacts/chunk_embeddings.npy`), and Whisper/OCR extraction caches are bundled directly in the repo.
  The application runs locally **without needing to re-extract audio/video or OCR**.
- **LLM generation mode:**
  - *Live mode:* Export `GROQ_API_KEY="your-key"` to generate responses via `llama-3.1-8b-instant`.
  - *Mock demonstration mode:* If launched without a Groq key, the application automatically runs in
    deterministic mock mode with real hybrid retrieval, citation parsing, and role guardrails.
- **Formal research report:** Full 14-page project report with architecture proofs and failure audits
  available in [`docs/SMF_Grant_Advisory_Report.pdf`](docs/SMF_Grant_Advisory_Report.pdf).

## Project structure
| Path | Role |
|------|------|
| `app.py` | Standalone Gradio 3-tab application (Member Mode, Admin Mode, Threshold Sandbox) |
| `rag_pipeline.py` | Multimodal hybrid retrieval engine (FAISS+BM25), cross-encoder reranker, and role policy |
| `artifacts/` | Precomputed vector indices, embeddings, and Whisper/OCR extraction caches |
| `data/eval/` | 38-question benchmark test set and answer key (`test_questions.csv`) |
| `data/results/` | Empirical metric comparison tables and per-question latency records |
| `knowledge_base/` | 4-modality corpus: Text PDFs, Visual PDFs, Audio MP3s, and Video MP4s |
| `docs/` | Formal 14-page project report (`SMF_Grant_Advisory_Report.pdf`) |
| `notebooks/` | Master clean pipeline (`01_build_and_evaluate.ipynb`), evidence run, and demo notebook |
| `requirements.txt` | Python dependencies |

## Tech
Python · PyTorch · Sentence Transformers (`all-MiniLM-L6-v2`) · FAISS · Rank-BM25 · Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) · OpenAI Whisper · Tesseract OCR · Gradio · Groq

## Limitations & further work
- **Abstention boundary:** Calibrated thresholding achieves 0.333 abstention on 0.5B models; scaling to
  larger reasoning models further improves out-of-domain detection.
- **ASR proper-noun phonetic drift:** Speech recognition occasionally mishears regional names
  (*Tanjung* $\rightarrow$ *Tenjong*); handled via phonetic guardrails.
- **Multi-document recall budget:** Capped at 5 slots in real-time latency budgets.

## License
MIT — see [LICENSE](LICENSE).
