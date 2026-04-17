import json

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.graph.state import AgentState, show_agent_reasoning
from src.utils.llm import call_llm
from src.utils.progress import progress


class SupplyOutput(BaseModel):
    stability: str = Field(description="高 / 中 / 低")
    key_risks: list[str] = Field(description="关键风险")
    scalable: bool = Field(description="是否可规模化")
    suggestions: list[str] = Field(description="建议")
    confidence: float = Field(description="0-1 置信度")


def supply_agent(state: AgentState, agent_id: str = "supply_agent"):
    question = state["data"]["question"]
    progress.update_status(agent_id, None, "Analyzing supply chain")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是外贸供应链专家。"),
            (
                "human",
                "问题：{question}\n\n输出字段：stability, key_risks, scalable, suggestions, confidence。",
            ),
        ]
    ).invoke({"question": question})

    result = call_llm(prompt, SupplyOutput, agent_name=agent_id, state=state)
    payload = result.model_dump()
    state["data"]["agent_outputs"][agent_id] = payload

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(payload, "Supply Agent")

    progress.update_status(agent_id, None, "Done")
    return {"messages": state["messages"] + [HumanMessage(content=json.dumps(payload, ensure_ascii=False), name=agent_id)], "data": state["data"]}
