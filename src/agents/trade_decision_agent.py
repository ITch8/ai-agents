import json

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.graph.state import AgentState, show_agent_reasoning
from src.utils.llm import call_llm
from src.utils.progress import progress


class FinalDecisionOutput(BaseModel):
    final_decision: str = Field(description="建议做 / 不做 / 小规模测试")
    core_reasons: list[str] = Field(description="核心理由，最多3条")
    biggest_risk: str = Field(description="最大风险")
    action_plan: list[str] = Field(description="建议行动路径")
    confidence: float = Field(description="0-1 置信度")


def trade_decision_agent(state: AgentState, agent_id: str = "trade_decision_agent"):
    question = state["data"]["question"]
    all_outputs = state["data"]["agent_outputs"]
    progress.update_status(agent_id, None, "Generating final decision")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是外贸决策委员会负责人。你不是简单平均，而是基于权重做权衡。"
                "权重：客户获取 > 利润 > 市场 > 产品 > 供应链。"
                "必须识别专家之间的冲突点，并给出可执行动作，禁止空话。",
            ),
            (
                "human",
                "问题：{question}\n\n各 Agent 输出：{outputs}\n\n"
                "要求：\n"
                "1) final_decision 只能是：建议做 / 不建议做 / 小规模测试\n"
                "2) core_reasons 必须包含支持与反对的权衡点（最多3条）\n"
                "3) action_plan 至少3步，且每步可执行\n"
                "4) biggest_risk 具体到一个失败场景\n\n"
                "输出字段：final_decision, core_reasons, biggest_risk, action_plan, confidence。",
            ),
        ]
    ).invoke({"question": question, "outputs": json.dumps(all_outputs, ensure_ascii=False)})

    result = call_llm(prompt, FinalDecisionOutput, agent_name=agent_id, state=state)
    payload = result.model_dump()
    state["data"]["agent_outputs"][agent_id] = payload

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(payload, "Trade Decision Agent")

    progress.update_status(agent_id, None, "Done")
    return {"messages": state["messages"] + [HumanMessage(content=json.dumps(payload, ensure_ascii=False), name=agent_id)], "data": state["data"]}
