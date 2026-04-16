import json

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.graph.state import AgentState, show_agent_reasoning
from src.utils.llm import call_llm
from src.utils.progress import progress


class MarketOutput(BaseModel):
    verdict: str = Field(description="做 / 谨慎 / 不做")
    core_reasons: list[str] = Field(description="核心理由，最多3条")
    market_risks: list[str] = Field(description="市场风险")
    confidence: float = Field(description="0-1 置信度")


def market_agent(state: AgentState, agent_id: str = "market_agent"):
    question = state["data"]["question"]
    progress.update_status(agent_id, None, "Analyzing market opportunity")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是外贸市场机会专家。请严格输出结构化结果，避免空话。",
            ),
            (
                "human",
                "问题：{question}\n\n请判断是否值得进入，并输出：verdict, core_reasons, market_risks, confidence。",
            ),
        ]
    ).invoke({"question": question})

    result = call_llm(prompt, MarketOutput, agent_name=agent_id, state=state)
    payload = result.model_dump()
    state["data"]["agent_outputs"][agent_id] = payload

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(payload, "Market Agent")

    progress.update_status(agent_id, None, "Done")
    return {"messages": state["messages"] + [HumanMessage(content=json.dumps(payload, ensure_ascii=False), name=agent_id)], "data": state["data"]}
