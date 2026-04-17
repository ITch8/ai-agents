import json
import os
from dataclasses import dataclass
from pathlib import Path

from src.main import run_trade_decision


@dataclass
class BenchmarkCase:
    name: str
    question: str
    expected_keywords: list[str]


CASES = [
    BenchmarkCase("测试1 红海低利润", "我要不要做：手机壳（低价批发，走阿里国际站）", ["不建议", "测试", "红海", "利润"]),
    BenchmarkCase("测试2 高门槛工业品", "我要不要做：工业自动化设备出口", ["门槛", "谨慎", "可做", "客户"]),
    BenchmarkCase("测试3 合规敏感", "我要不要做：无品牌保健品出口到欧美", ["不建议", "合规", "风险"]),
    BenchmarkCase("测试4 流量利润冲突", "我要不要做：低价LED灯，走量模式", ["获客", "利润", "冲突", "同质化"]),
    BenchmarkCase("测试5 供应链冲突", "我要不要做：定制家具出口", ["供应链", "交付", "谨慎"]),
    BenchmarkCase("测试6 高利润难获客", "我要不要做：高端医疗设备出口", ["获客", "高利润", "谨慎"]),
    BenchmarkCase("测试7 资源限制", "我只有10万预算，没有外贸经验，要不要做B2B出口？", ["不建议", "小单", "风险"]),
    BenchmarkCase("测试8 渠道选择", "我要做宠物用品，应该选阿里国际站还是独立站？", ["阿里国际站", "独立站", "建议"]),
    BenchmarkCase("测试9 选品", "我想做外贸，应该选什么产品？", ["筛选", "竞争", "差异化"]),
    BenchmarkCase("测试10 扩张", "我现在做一个产品月利润2万，要不要扩大规模？", ["扩张", "现金流", "供应链"]),
    BenchmarkCase("测试11 综合", "我在中国，有供应链资源，想做外贸，预算20万，目标是1年赚到50万，应该怎么做？", ["步骤", "渠道", "产品", "风险"]),
]


SELECTED_ANALYSTS = [
    "market",
    "customer",
    "product",
    "supply",
    "profit",
    "data_analysis",
    "case_analysis",
]

MODEL_NAME = os.getenv("BENCHMARK_MODEL_NAME", "gpt-4.1")
MODEL_PROVIDER = os.getenv("BENCHMARK_MODEL_PROVIDER", "OpenAI")


def score_case(case: BenchmarkCase, result: dict) -> dict:
    final_decision = result.get("final_decision", {}) or {}
    all_text = json.dumps(final_decision, ensure_ascii=False)
    keyword_hits = [k for k in case.expected_keywords if k in all_text]

    outputs = result.get("agent_outputs", {}) or {}
    role_diversity = len(outputs.keys()) >= 7
    actionable = len(final_decision.get("action_plan", []) or []) >= 2

    score = 0
    score += min(5, len(keyword_hits))
    score += 2 if role_diversity else 0
    score += 3 if actionable else 0

    return {
        "case": case.name,
        "question": case.question,
        "score": score,
        "keyword_hits": keyword_hits,
        "role_diversity": role_diversity,
        "actionable": actionable,
        "final_decision": final_decision,
    }


def run_benchmark():
    report = []
    for case in CASES:
        try:
            result = run_trade_decision(
                question=case.question,
                selected_analysts=SELECTED_ANALYSTS,
                model_name=MODEL_NAME,
                model_provider=MODEL_PROVIDER,
            )
            report.append(score_case(case, result))
        except Exception as exc:
            report.append(
                {
                    "case": case.name,
                    "question": case.question,
                    "error": str(exc),
                    "score": 0,
                }
            )

    output_path = Path("benchmark_results.json")
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Benchmark finished with {MODEL_PROVIDER}/{MODEL_NAME}, report written to {output_path}")


if __name__ == "__main__":
    run_benchmark()
