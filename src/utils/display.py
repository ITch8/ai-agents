from colorama import Fore, Style
from tabulate import tabulate
import json


def print_trade_decision_output(result: dict) -> None:
    """Print formatted foreign trade decision results."""
    question = result.get("question", "")
    final_decision = result.get("final_decision", {})
    agent_outputs = result.get("agent_outputs", {})

    print(f"\n{Fore.WHITE}{Style.BRIGHT}FOREIGN TRADE DECISION{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Question:{Style.RESET_ALL} {question}")

    table_data = []
    for agent_name, payload in agent_outputs.items():
        if agent_name == "trade_decision_agent":
            continue
        confidence = payload.get("confidence", "-")
        table_data.append(
            [
                agent_name.replace("_agent", "").replace("_", " ").title(),
                f"{confidence:.2f}" if isinstance(confidence, (float, int)) else str(confidence),
                json.dumps(payload, ensure_ascii=False),
            ]
        )

    if table_data:
        print(f"\n{Fore.WHITE}{Style.BRIGHT}AGENT OUTPUTS:{Style.RESET_ALL}")
        print(
            tabulate(
                table_data,
                headers=[f"{Fore.WHITE}Agent", "Confidence", "Output"],
                tablefmt="grid",
                colalign=("left", "right", "left"),
            )
        )

    decision_rows = [
        ["Final Decision", final_decision.get("final_decision", "")],
        ["Core Reasons", json.dumps(final_decision.get("core_reasons", []), ensure_ascii=False)],
        ["Biggest Risk", final_decision.get("biggest_risk", "")],
        ["Action Plan", json.dumps(final_decision.get("action_plan", []), ensure_ascii=False)],
        ["Confidence", final_decision.get("confidence", "")],
    ]
    print(f"\n{Fore.WHITE}{Style.BRIGHT}FINAL RECOMMENDATION:{Style.RESET_ALL}")
    print(tabulate(decision_rows, tablefmt="grid", colalign=("left", "left")))


def print_trading_output(result: dict) -> None:
    """Backward-compatible alias for legacy imports."""
    print_trade_decision_output(result)
