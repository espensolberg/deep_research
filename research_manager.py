from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
import asyncio
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class RefinementContext:
    original_query: str
    prior_refinements: tuple[str, ...]
    previous_report: str


class ResearchManager:

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        async for update in self.run_iteration(query):
            yield update.markdown_report if isinstance(update, ReportData) else update

    async def run_iteration(self, query: str, context: RefinementContext | None = None):
        """Yield progress messages and the completed report for one investigation round."""
        research_brief = query
        if context is not None:
            research_brief = json.dumps({
                "original_query": context.original_query,
                "prior_refinements": context.prior_refinements,
                "latest_refinement": query,
                "previous_report": context.previous_report,
            }, ensure_ascii=False)

        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield f"Starting research. Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            search_plan = await self.plan_searches(research_brief)
            yield f"Searches planned, starting {len(search_plan.searches)} searches..."
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            report = await self.write_report(research_brief, search_results)
            if context is None:
                yield "Report written, sending email..."
                await self.send_email(report)
                yield "Email sent, research complete"
            yield report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        result = await Runner.run(planner_agent, f"Research brief: {query}")
        return result.final_output

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        tasks = [self.search(item) for item in search_plan.searches]
        return await asyncio.gather(*tasks)

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input_message = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await Runner.run(search_agent, input_message)
        return result.final_output

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        input_message = f"Research brief: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input_message)
        return result.final_output
    
    async def send_email(self, report: ReportData) -> None:
        await Runner.run(email_agent, report.markdown_report)
