import json

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.graph.state import AgentState, show_agent_reasoning
from src.utils.llm import call_llm
from src.utils.progress import progress


class ProfitOutput(BaseModel):
    profitability: str = Field(description="强 / 中 / 弱")
    revenue_sources: list[str] = Field(description="利润来源")
    cost_pressures: list[str] = Field(description="主要成本压力")
    risks: list[str] = Field(description="风险")
    confidence: float = Field(description="0-1 置信度")


def profit_agent(state: AgentState, agent_id: str = "profit_agent"):
    question = state["data"]["question"]
    progress.update_status(agent_id, None, "Analyzing profit model")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是外贸商业模型分析专家。"),
            (
                "human",
                "问题：{question}\n\n输出字段：profitability, revenue_sources, cost_pressures, risks, confidence。",
            ),
        ]
    ).invoke({"question": question})

    result = call_llm(prompt, ProfitOutput, agent_name=agent_id, state=state)
    payload = result.model_dump()
    state["data"]["agent_outputs"][agent_id] = payload

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(payload, "Profit Agent")

    progress.update_status(agent_id, None, "Done")
    return {"messages": state["messages"] + [HumanMessage(content=json.dumps(payload, ensure_ascii=False), name=agent_id)], "data": state["data"]}
