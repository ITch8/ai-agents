import json

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.graph.state import AgentState, show_agent_reasoning
from src.utils.llm import call_llm
from src.utils.progress import progress


class CustomerOutput(BaseModel):
    feasibility: str = Field(description="高 / 中 / 低")
    channels: list[str] = Field(description="主要获客渠道")
    challenges: list[str] = Field(description="获客难点")
    strategy: list[str] = Field(description="建议策略")
    confidence: float = Field(description="0-1 置信度")


def customer_agent(state: AgentState, agent_id: str = "customer_agent"):
    question = state["data"]["question"]
    progress.update_status(agent_id, None, "Analyzing customer acquisition")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是外贸客户开发专家，聚焦渠道、转化、获客成本与规模化。"),
            (
                "human",
                "问题：{question}\n\n输出字段：feasibility, channels, challenges, strategy, confidence。",
            ),
        ]
    ).invoke({"question": question})

    result = call_llm(prompt, CustomerOutput, agent_name=agent_id, state=state)
    payload = result.model_dump()
    state["data"]["agent_outputs"][agent_id] = payload

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(payload, "Customer Agent")

    progress.update_status(agent_id, None, "Done")
    return {"messages": state["messages"] + [HumanMessage(content=json.dumps(payload, ensure_ascii=False), name=agent_id)], "data": state["data"]}
