"""SMF Multimodal Grant Advisory Assistant — Web Application.

A 3-tab Gradio terminal:
1. Member Advisory: Public mode with role-based PII masking.
2. Advisory Officer: Internal admin mode with full application history.
3. Confidence Floor Sandbox: Interactive threshold slider demonstrating abstention trade-offs.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple

import gradio as gr

from rag_pipeline import MOD, MultimodalRAGPipeline, tidy_text, tidy_title

CSS = """
:root {
  --ink: #111827; --muted: #4B5563; --paper: #F8FAFC; --card: #FFFFFF;
  --line: #E2E8F0; --brand: #0284C7; --warn: #D97706; --danger: #DC2626; --safe: #16A34A;
}
.gradio-container { background: var(--paper) !important; font-family: 'Inter', system-ui, sans-serif; }
#hero {
  display: flex; align-items: center; gap: 14px; padding: 20px 24px; margin-bottom: 12px;
  background: #0F172A; border-radius: 12px; color: #fff;
}
#hero .badge-icon {
  width: 42px; height: 42px; border-radius: 10px; background: var(--brand);
  display: flex; align-items: center; justify-content: center; font-size: 22px;
}
#hero h1 { font-size: 19px; margin: 0; font-weight: 650; letter-spacing: .2px; }
#hero p { margin: 3px 0 0; font-size: 13px; color: #94A3B8; }
.panel-card { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 18px; margin-bottom: 12px; }
.source-card {
  border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; margin-bottom: 8px;
  background: #FFFFFF; font-size: 13px; line-height: 1.5;
}
.source-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.badge { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 700; color: #fff; }
.eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 8px;
}
footer { display: none !important; }
"""

HERO = """
<div id='hero'>
  <div class='badge-icon'>📑</div>
  <div>
    <h1>SMF Grant Advisory Assistant — Multimodal RAG</h1>
    <p>Four-Modality Enterprise RAG · Text PDFs · Visual OCR · Audio Whisper · Video Transcripts · Role-Based Privacy</p>
  </div>
</div>
"""

MEMBER_PRESETS = [
    "What percentage of eligible costs does PSG support for local SMEs?",
    "Can a company claim EDG for work that commenced before the grant was approved?",
    "What are the main rejection reasons for grant applications?",
    "How much did Precision Dynamics claim under PSG?",  # Role check: triggers refusal
]

ADMIN_PRESETS = [
    "What was the outcome of Precision Dynamics' PSG application and what did it purchase?",
    "Why was Tanjung losing tenders before adopting the ERP system?",
    "Summarise the total grant utilisation and rejection rate from the review document.",
]

TRADE_OFF_PRESETS = [
    "What are the common rejection reasons and eligibility rules across schemes?",
    "Does SMF charge an administrative processing fee to unlock government grants?",
    "What are the specific requirements for the upcoming EDGE framework?",
]

PIPELINE = MultimodalRAGPipeline()


def render_sources_html(results: List[Dict]) -> str:
    if not results:
        return "<p style='color:#6B7280;font-size:13px;'>No evidence passages retrieved.</p>"

    html_parts = []
    for r in results:
        mod_color, mod_label = MOD.get(r["modality"], ("#4B5563", r["modality"].upper()))
        card = f"""
        <div class='source-card'>
          <div class='source-header'>
            <span><b>[S{r['rank']}] {tidy_title(r['title'])}</b></span>
            <span class='badge' style='background:{mod_color};'>{mod_label}</span>
          </div>
          <div style='color:#64748B;font-size:12px;margin-bottom:6px;'>
            Source: <code>{r['source']}</code> ({r.get('locator') or 'page ' + str(r['page'])}) · Similarity: {r['dense_score']:.3f}
          </div>
          <div style='color:#1E293B;'>{tidy_text(r['text'])}</div>
        </div>
        """
        html_parts.append(card)
    return "".join(html_parts)


def answer_ui(question: str, role: str, top_k: int, threshold: float):
    ans, results, mode = PIPELINE.answer(question, role=role, top_k=int(top_k), threshold=float(threshold))
    sources_html = render_sources_html(results)

    mods = sorted({r["modality"] for r in results})
    meta_info = f"Retrieved {len(results)} passage(s) across {len(mods)} modality(ies) · Mode: {mode}"
    return ans, sources_html, meta_info


def build_app():
    with gr.Blocks(css=CSS, title="SMF Multimodal Grant Advisory RAG") as demo:
        gr.HTML(HERO)

        with gr.Tabs():
            # Tab 1: Member Mode
            with gr.Tab("🏛️ 1. Member Advisory (Public Portal)"):
                gr.HTML(
                    "<div class='eyebrow'>Role: Member Company · Privacy Policy Enforced (Other companies' PII shielded)</div>"
                )
                with gr.Row():
                    with gr.Column(scale=3):
                        mem_dropdown = gr.Dropdown(MEMBER_PRESETS, label="Sample Member Questions", value=None)
                        mem_input = gr.Textbox(
                            label="Your Grant Question",
                            placeholder="Ask about EDG, PSG, MRA, SkillsFuture, or commencement rules...",
                            lines=2,
                        )
                        mem_btn = gr.Button("🔍 Query Grant Assistant", variant="primary")
                    with gr.Column(scale=1):
                        mem_top_k = gr.Slider(1, 8, value=5, step=1, label="Top-k Passages")
                        mem_thresh = gr.Slider(0.0, 0.6, value=0.0, step=0.05, label="Confidence Floor")

                mem_output = gr.Markdown(label="Attributed Response")
                mem_status = gr.HTML()
                mem_sources = gr.HTML(label="Retrieved Multimodal Evidence")

                def run_mem(q, k, th):
                    ans, src, meta = answer_ui(q, "member", k, th)
                    return ans, f"<p style='color:#475569;font-size:12px;'>{meta}</p>", src

                mem_dropdown.change(lambda x: x, mem_dropdown, mem_input)
                mem_btn.click(run_mem, [mem_input, mem_top_k, mem_thresh], [mem_output, mem_status, mem_sources])

            # Tab 2: Admin Mode
            with gr.Tab("💼 2. Advisory Officer (Admin Portal)"):
                gr.HTML(
                    "<div class='eyebrow'>Role: SMF Advisory Officer · Internal Review & Company Histories Accessible</div>"
                )
                with gr.Row():
                    with gr.Column(scale=3):
                        adm_dropdown = gr.Dropdown(ADMIN_PRESETS, label="Sample Officer Case Queries", value=None)
                        adm_input = gr.Textbox(
                            label="Officer Query",
                            placeholder="Look up company case studies, grant utilization stats, or rejection audit tables...",
                            lines=2,
                        )
                        adm_btn = gr.Button("🔍 Query Officer Records", variant="primary")
                    with gr.Column(scale=1):
                        adm_top_k = gr.Slider(1, 8, value=5, step=1, label="Top-k Passages")
                        adm_thresh = gr.Slider(0.0, 0.6, value=0.0, step=0.05, label="Confidence Floor")

                adm_output = gr.Markdown(label="Officer Assessment")
                adm_status = gr.HTML()
                adm_sources = gr.HTML(label="Cross-Modal Case Evidence")

                def run_adm(q, k, th):
                    ans, src, meta = answer_ui(q, "admin", k, th)
                    return ans, f"<p style='color:#475569;font-size:12px;'>{meta}</p>", src

                adm_dropdown.change(lambda x: x, adm_dropdown, adm_input)
                adm_btn.click(run_adm, [adm_input, adm_top_k, adm_thresh], [adm_output, adm_status, adm_sources])

            # Tab 3: Trade-off Sandbox
            with gr.Tab("⚖️ 3. Abstention & Threshold Sandbox"):
                gr.HTML(
                    "<div class='eyebrow'>Experiment 3b Demo: Drag confidence floor from 0.00 to 0.40 to observe graceful abstention</div>"
                )
                with gr.Row():
                    with gr.Column(scale=3):
                        to_dropdown = gr.Dropdown(TRADE_OFF_PRESETS, label="Select Boundary Cases", value=None)
                        to_input = gr.Textbox(
                            label="Boundary Query",
                            value="What are the common rejection reasons and eligibility rules across schemes?",
                            lines=2,
                        )
                        to_slider = gr.Slider(
                            0.0,
                            0.60,
                            value=0.40,
                            step=0.05,
                            label="Similarity Threshold (Floor >= 0.40 triggers abstention on weak evidence)",
                        )
                        to_btn = gr.Button("Test Threshold Effect", variant="secondary")
                    with gr.Column(scale=2):
                        gr.Markdown(
                            "**How the threshold works:**\n"
                            "- **Floor = 0.00:** Always returns top-k passages regardless of similarity score (maximizes recall).\n"
                            "- **Floor = 0.40 (Tuned):** Filters out weakly matching candidates. If no passages exceed 0.40, the system gracefully **abstains** rather than hallucinating."
                        )

                to_output = gr.Markdown(label="Response with Threshold")
                to_sources = gr.HTML(label="Filtered Evidence")

                def run_to(q, th):
                    ans, src, meta = answer_ui(q, "admin", 5, th)
                    return ans, src

                to_dropdown.change(lambda x: x, to_dropdown, to_input)
                to_btn.click(run_to, [to_input, to_slider], [to_output, to_sources])

    return demo


def main():
    app = build_app()
    app.launch(server_port=7863, share=False)


if __name__ == "__main__":
    main()
