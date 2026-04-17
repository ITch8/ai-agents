import json

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.graph.state import AgentState, show_agent_reasoning
from src.utils.llm import call_llm
from src.utils.progress import progress


class CaseAnalysisOutput(BaseModel):
    comparable_cases: list[str] = Field(description="可类比案例")
    failure_patterns: list[str] = Field(description="典型失败模式")
    success_patterns: list[str] = Field(description="典型成功模式")
    practical_advice: list[str] = Field(description="可执行建议")
    confidence: float = Field(description="0-1 置信度")


def case_analysis_agent(state: AgentState, agent_id: str = "case_analysis_agent"):
    question = state["data"]["question"]
    expert_outputs = state["data"]["agent_outputs"]
    progress.update_status(agent_id, None, "Synthesizing case analysis")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是外贸案例分析 Agent，负责用经验案例发现成败模式。"),
            (
                "human",
                "问题：{question}\n\n专家输出：{expert_outputs}\n\n输出字段：comparable_cases, failure_patterns, success_patterns, practical_advice, confidence。",
            ),
        ]
    ).invoke(
        {
            "question": question,
            "expert_outputs": json.dumps(expert_outputs, ensure_ascii=False),
        }
    )

    result = call_llm(prompt, CaseAnalysisOutput, agent_name=agent_id, state=state)
    payload = result.model_dump()
    state["data"]["agent_outputs"][agent_id] = payload

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(payload, "Case Analysis Agent")

    progress.update_status(agent_id, None, "Done")
    return {"messages": state["messages"] + [HumanMessage(content=json.dumps(payload, ensure_ascii=False), name=agent_id)], "data": state["data"]}
