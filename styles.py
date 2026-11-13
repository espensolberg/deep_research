from base64 import b64encode
from pathlib import Path

EXAMPLES = [
    "Most popular AI Agent frameworks in 2026",
    "Most commercially successful Agentic AI implementations in 2026",
    "Celebrities who don't like cheese",
]

logo_path = Path(__file__).with_name("assets") / "squirrel-professor.png"
logo_data = b64encode(logo_path.read_bytes()).decode("ascii")

HEADER_HTML = f"""
<header class="dr-brand">
    <div class="dr-mark">
        <img src="data:image/png;base64,{logo_data}" alt="" width="100" height="100">
    </div>
    <div class="dr-titles">
        <h1>Deep Research</h1>
        <p>Multi-search web investigation</p>
    </div>
</header>
"""

CSS = """
:root {
    color-scheme: dark;
    --dr-bg: #080b0e;
    --dr-surface: #101a21;
    --dr-field: #0c151c;
    --dr-border: #2a424a;
    --dr-text: #edf5f4;
    --dr-muted: #a9bdc5;
    --dr-blue: #98d0f4;
    --dr-green: #a3d8b4;
    --dr-radius: 18px;
}

html, body, gradio-app {
    background: var(--dr-bg) !important;
}

.gradio-container {
    --body-background-fill: var(--dr-bg);
    --body-text-color: var(--dr-text);
    --body-text-color-subdued: var(--dr-muted);
    --block-background-fill: var(--dr-surface);
    --block-border-color: var(--dr-border);
    --border-color-primary: var(--dr-border);
    --background-fill-primary: var(--dr-surface);
    --background-fill-secondary: var(--dr-field);
    --link-text-color: var(--dr-blue);
    --link-text-color-hover: var(--dr-green);

    max-width: 1024px !important;
    min-height: 100vh !important;
    margin: 0 auto !important;
    padding: clamp(1rem, 5vw, 3.75rem) clamp(1rem, 4vw, 2rem) 4rem !important;
    background: var(--dr-bg) !important;
    color: var(--dr-text) !important;
    font-family: Nunito, system-ui, sans-serif !important;
}

.dr-brand {
    display: flex;
    align-items: center;
    gap: clamp(0.85rem, 3vw, 1.65rem);
    padding: clamp(1rem, 4vw, 2rem);
    margin-bottom: 0.7rem;
    border: 1px solid var(--dr-border);
    border-radius: 26px;
    background: radial-gradient(ellipse at 100% 0%, #234438 0%, transparent 68%),
                linear-gradient(120deg, #152d40, #111e29 70%);
}

.dr-mark {
    display: grid;
    place-items: center;
    flex: 0 0 auto;
    width: clamp(66px, 13vw, 116px);
    aspect-ratio: 1;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #456260;
    border-radius: 24%;
    background: #102520;
}

.dr-mark img {
    display: block;
    width: 100%;
    height: auto;
}

.dr-titles h1 {
    color: var(--dr-text);
    font-size: clamp(1.65rem, 5.5vw, 3.35rem);
    font-weight: 800;
    letter-spacing: -0.045em;
    line-height: 1.05;
    margin: 0;
}

.dr-titles p {
    color: var(--dr-muted);
    font-size: clamp(0.85rem, 2vw, 1rem);
    margin: 0.45rem 0 0;
}

.dr-composer {
    padding: clamp(1rem, 3vw, 1.6rem) !important;
    border: 1px solid var(--dr-border) !important;
    border-radius: 24px !important;
    background: var(--dr-surface) !important;
    gap: 0.75rem !important;
}

.dr-query-row {
    gap: 0.75rem !important;
    align-items: stretch !important;
}

#dr-query, #dr-query > div, #dr-query .wrap, #dr-query .form, #dr-query .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

#dr-query :is(textarea, input) {
    background: var(--dr-field) !important;
    color: var(--dr-text) !important;
    border: 1px solid #486575 !important;
    border-radius: var(--dr-radius) !important;
    padding: 0.95rem 1.1rem !important;
    font: inherit !important;
    line-height: 1.5 !important;
    min-height: 54px !important;
    box-shadow: none !important;
}

#dr-query :is(textarea, input)::placeholder {
    color: var(--dr-muted) !important;
    opacity: 1;
}

#dr-run {
    background: linear-gradient(115deg, #97c7ed, #9cd4af) !important;
    color: #0b2424 !important;
    border: 1px solid transparent !important;
    border-radius: var(--dr-radius) !important;
    min-height: 54px;
    min-width: 132px !important;
    padding: 0.8rem 1.3rem !important;
    font-family: inherit !important;
    font-weight: 800 !important;
    box-shadow: none !important;
}

#dr-run:hover {
    background: linear-gradient(115deg, #afd8f6, #b4e5c3) !important;
}

#dr-query :is(textarea, input):focus,
#dr-run:focus-visible,
#dr-examples :is(td, button):focus-visible,
#dr-report a:focus-visible {
    outline: 2px solid var(--dr-blue) !important;
    outline-offset: -2px !important;
}

#dr-examples, #dr-examples > div, #dr-examples .wrap, #dr-examples .block {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

#dr-examples thead {
    display: none !important;
}

#dr-examples :is(table, tbody, tr) {
    background: transparent !important;
    border: none !important;
}

#dr-examples :is(table, tbody) {
    display: block !important;
    width: 100% !important;
}

#dr-examples tr {
    display: flex !important;
    flex-wrap: wrap;
    gap: 0.45rem;
}

#dr-examples :is(td, button) {
    background: #172b2b !important;
    color: var(--dr-green) !important;
    border: 1px solid #355850 !important;
    border-radius: 14px !important;
    padding: 0.55rem 0.8rem !important;
    font-family: inherit !important;
    font-size: 0.875rem !important;
    white-space: normal !important;
    text-align: left !important;
    box-shadow: none !important;
}

#dr-examples :is(td, button):hover {
    background: #203e38 !important;
    border-color: var(--dr-green) !important;
}

#dr-report {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    color: var(--dr-text) !important;
    box-shadow: none !important;
    min-width: 0;
}

#dr-report .prose {
    color: var(--dr-text) !important;
    overflow-wrap: anywhere;
}

#dr-report div.prose:has(:is(p, h1, h2, h3, ul, ol, pre, blockquote, table)) {
    margin-top: 0.85rem;
    padding: clamp(1rem, 3vw, 1.7rem);
    background: var(--dr-surface);
    border: 1px solid var(--dr-border);
    border-radius: 24px;
    overflow-x: auto;
}

#dr-report :is(h1, h2, h3, h4, h5, h6, strong) {
    color: var(--dr-text) !important;
}

#dr-report h2 { color: var(--dr-green) !important; }
#dr-report p, #dr-report li { line-height: 1.7; }

#dr-report a {
    color: var(--dr-blue) !important;
    text-decoration: underline;
    text-underline-offset: 3px;
}

#dr-report a:hover { color: var(--dr-green) !important; }

#dr-report :is(pre, code, blockquote) {
    color: var(--dr-text) !important;
    background: var(--dr-field) !important;
    border-radius: 10px;
}

#dr-report blockquote {
    border-inline-start: 3px solid var(--dr-green) !important;
    padding: 0.7rem 1rem;
}

#dr-report table {
    border-collapse: separate;
    border-spacing: 0;
    border: 1px solid var(--dr-border);
    border-radius: 12px;
    overflow: hidden;
}

#dr-report :is(th, td) {
    border: 0 !important;
    border-bottom: 1px solid var(--dr-border) !important;
    padding: 0.55rem 0.8rem;
    text-align: left;
}

#dr-report th {
    background: var(--dr-field);
    color: var(--dr-blue);
}

.gradio-container footer { display: none !important; }

@media (max-width: 700px) {
    .dr-query-row { flex-direction: column !important; }
    #dr-query, #dr-run { width: 100% !important; min-width: 0 !important; }
}
"""

JS = """
() => {
    const focus = () => {
        const el = document.querySelector("#dr-query textarea, #dr-query input");
        if (el) { el.focus(); return true; }
        return false;
    };
    if (!focus()) {
        let tries = 0;
        const i = setInterval(() => {
            if (focus() || ++tries > 20) clearInterval(i);
        }, 100);
    }
}
"""
