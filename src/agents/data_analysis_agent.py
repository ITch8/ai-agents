import json

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.graph.state import AgentState, show_agent_reasoning
from src.utils.llm import call_llm
from src.utils.progress import progress


class DataAnalysisOutput(BaseModel):
    key_metrics: list[str] = Field(description="应重点验证的数据指标")
    missing_data: list[str] = Field(description="当前缺失数据")
    validation_plan: list[str] = Field(description="数据验证步骤")
    confidence: float = Field(description="0-1 置信度")


def data_analysis_agent(state: AgentState, agent_id: str = "data_analysis_agent"):
    question = state["data"]["question"]
    expert_outputs = state["data"]["agent_outputs"]
    progress.update_status(agent_id, None, "Synthesizing data analysis")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是外贸决策中的数据分析 Agent，负责把专家观点转化为可验证证据。"),
            (
                "human",
                "问题：{question}\n\n专家输出：{expert_outputs}\n\n输出字段：key_metrics, missing_data, validation_plan, confidence。",
            ),
        ]
    ).invoke(
        {
            "question": question,
            "expert_outputs": json.dumps(expert_outputs, ensure_ascii=False),
        }
    )

    result = call_llm(prompt, DataAnalysisOutput, agent_name=agent_id, state=state)
    payload = result.model_dump()
    state["data"]["agent_outputs"][agent_id] = payload

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(payload, "Data Analysis Agent")

    progress.update_status(agent_id, None, "Done")
    return {"messages": state["messages"] + [HumanMessage(content=json.dumps(payload, ensure_ascii=False), name=agent_id)], "data": state["data"]}
