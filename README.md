---
title: deep_research
app_file: app.py
sdk: gradio
sdk_version: 6.14.0
---

## Search refinements

After the first report, users can ask a follow-up question to refine the current
investigation. Each follow-up uses the previous report and runs fresh web searches.
Starting a new investigation resets its round counter.

Set `MAX_SEARCH_ITER=5` in the environment or `.env` to configure the number of
completed rounds per investigation. The default is five, including the initial
round. Set it to `1` to allow only the initial round.
