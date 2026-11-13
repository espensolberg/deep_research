from dataclasses import dataclass
import logging
import os

import gradio as gr
from dotenv import load_dotenv
from research_manager import RefinementContext, ResearchManager
from styles import CSS, JS, EXAMPLES, HEADER_HTML
from writer_agent import ReportData

load_dotenv(override=True)

logger = logging.getLogger(__name__)
MAX_SEARCH_ITER = int(os.getenv("MAX_SEARCH_ITER", "5"))
if MAX_SEARCH_ITER < 1:
    raise ValueError("MAX_SEARCH_ITER must be a positive integer")


@dataclass
class Investigation:
    original_query: str = ""
    refinements: tuple[str, ...] = ()
    latest_report: str = ""
    completed_rounds: int = 0
    running: bool = False


async def run(query: str, investigation: Investigation, refine: bool = False):
    query = query.strip()
    if not query:
        raise gr.Error("Enter a follow-up question." if refine else "Enter a research question.")
    if investigation.running:
        raise gr.Error("Wait for the current research round to finish.")
    if refine and not investigation.completed_rounds:
        raise gr.Error("Run an investigation before refining it.")
    if refine and investigation.completed_rounds >= MAX_SEARCH_ITER:
        raise gr.Error("This investigation has reached its search limit. Start a new one to continue.")

    context = None
    if refine:
        context = RefinementContext(
            investigation.original_query,
            investigation.refinements,
            investigation.latest_report,
        )

    investigation.running = True
    try:
        yield {run_button: gr.update(interactive=False), refine_button: gr.update(interactive=False)}
        async for update in ResearchManager().run_iteration(query, context):
            if isinstance(update, ReportData):
                if refine:
                    investigation.refinements += (query,)
                    investigation.completed_rounds += 1
                else:
                    investigation.original_query = query
                    investigation.refinements = ()
                    investigation.completed_rounds = 1
                investigation.latest_report = update.markdown_report
                yield {report: update.markdown_report, follow_up: ""}
            else:
                yield {progress: update}
        yield {progress: ""}
    except Exception:
        logger.exception("Research round failed")
        yield {progress: "The research round could not finish. Try again."}
    finally:
        investigation.running = False

    rounds = investigation.completed_rounds
    remaining = rounds < MAX_SEARCH_ITER
    message = f"Search rounds used: {rounds} of {MAX_SEARCH_ITER}."
    if not remaining:
        message += " Start a new investigation to continue."
    yield {
        run_button: gr.update(interactive=True),
        refinement_panel: gr.update(visible=rounds > 0),
        round_count: message,
        follow_up: gr.update(interactive=remaining),
        refine_button: gr.update(interactive=remaining),
    }


async def refine_search(query: str, investigation: Investigation):
    async for update in run(query, investigation, refine=True):
        yield update


with gr.Blocks(title="Deep Research") as ui:
    investigation = gr.State(Investigation())
    gr.HTML(HEADER_HTML)

    with gr.Column(elem_classes="dr-composer"):
        with gr.Row(elem_classes="dr-query-row"):
            query_textbox = gr.Textbox(
                placeholder="Type a research question...",
                show_label=False,
                container=False,
                autofocus=True,
                elem_id="dr-query",
                scale=5,
            )
            run_button = gr.Button("Investigate", variant="primary", elem_id="dr-run", scale=1)

        gr.Examples(
            examples=EXAMPLES,
            inputs=query_textbox,
            label="Try one",
            example_labels=[
                "Most popular AI Agent frameworks in 2026",
                "Commercial uses of Agentic AI in 2026",
                "Celebrities who don't like cheese",
            ],
            elem_id="dr-examples",
        )

    progress = gr.Markdown(elem_classes="dr-research-status")
    report = gr.Markdown(elem_id="dr-report")
    with gr.Column(visible=False, elem_classes=["dr-composer", "dr-refinement"]) as refinement_panel:
        round_count = gr.Markdown(elem_classes="dr-research-status")
        with gr.Row(elem_classes="dr-query-row"):
            follow_up = gr.Textbox(
                label="Refine this investigation",
                placeholder="Ask a follow-up question or narrow the scope...",
                container=False,
                elem_id="dr-follow-up",
                scale=5,
            )
            refine_button = gr.Button("Refine search", elem_id="dr-refine", scale=1)

    outputs = [run_button, progress, report, refinement_panel, round_count, follow_up, refine_button]
    gr.on(
        [run_button.click, query_textbox.submit],
        fn=run,
        inputs=[query_textbox, investigation],
        outputs=outputs,
        concurrency_limit=None,
        show_progress_on=progress,
    )
    gr.on(
        [refine_button.click, follow_up.submit],
        fn=refine_search,
        inputs=[follow_up, investigation],
        outputs=outputs,
        concurrency_limit=None,
        show_progress_on=progress,
    )


if __name__ == "__main__":
    ui.launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base(font=[gr.themes.GoogleFont("Nunito"), "system-ui", "sans-serif"]),
    )
