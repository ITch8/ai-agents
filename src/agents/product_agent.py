import json

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.graph.state import AgentState, show_agent_reasoning
from src.utils.llm import call_llm
from src.utils.progress import progress


class ProductOutput(BaseModel):
    competitiveness: str = Field(description="强 / 中 / 弱")
    key_issues: list[str] = Field(description="主要问题")
    differentiation: list[str] = Field(description="差异化机会")
    risks: list[str] = Field(description="风险点")
    confidence: float = Field(description="0-1 置信度")


def product_agent(state: AgentState, agent_id: str = "product_agent"):
    question = state["data"]["question"]
    progress.update_status(agent_id, None, "Analyzing product competitiveness")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是外贸产品竞争分析专家。"),
            (
                "human",
                "问题：{question}\n\n输出字段：competitiveness, key_issues, differentiation, risks, confidence。",
            ),
        ]
    ).invoke({"question": question})

    result = call_llm(prompt, ProductOutput, agent_name=agent_id, state=state)
    payload = result.model_dump()
    state["data"]["agent_outputs"][agent_id] = payload

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(payload, "Product Agent")

    progress.update_status(agent_id, None, "Done")
    return {"messages": state["messages"] + [HumanMessage(content=json.dumps(payload, ensure_ascii=False), name=agent_id)], "data": state["data"]}
