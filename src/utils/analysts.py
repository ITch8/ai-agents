"""Constants and utilities for the trade decision framework."""

from src.agents.market_agent import market_agent
from src.agents.customer_agent import customer_agent
from src.agents.product_agent import product_agent
from src.agents.supply_agent import supply_agent
from src.agents.profit_agent import profit_agent
from src.agents.data_analysis_agent import data_analysis_agent
from src.agents.case_analysis_agent import case_analysis_agent

# Define agent configuration - single source of truth
ANALYST_CONFIG = {
    "market": {
        "display_name": "Market Agent",
        "description": "Market opportunity specialist",
        "investing_style": "Evaluates market demand, growth trend, and market-entry timing for export business.",
        "agent_func": market_agent,
        "type": "expert",
        "order": 0,
    },
    "customer": {
        "display_name": "Customer Agent",
        "description": "Customer acquisition specialist",
        "investing_style": "Assesses channels, conversion, and customer acquisition scalability in foreign trade.",
        "agent_func": customer_agent,
        "type": "expert",
        "order": 1,
    },
    "product": {
        "display_name": "Product Agent",
        "description": "Product competitiveness specialist",
        "investing_style": "Examines product differentiation, substitution risk, and export product advantage.",
        "agent_func": product_agent,
        "type": "expert",
        "order": 2,
    },
    "supply": {
        "display_name": "Supply Agent",
        "description": "Supply chain specialist",
        "investing_style": "Evaluates sourcing stability, delivery risk, and scalability in supply chain operations.",
        "agent_func": supply_agent,
        "type": "expert",
        "order": 3,
    },
    "profit": {
        "display_name": "Profit Agent",
        "description": "Profit model specialist",
        "investing_style": "Assesses margin structure, cost pressure, and long-term profit sustainability.",
        "agent_func": profit_agent,
        "type": "expert",
        "order": 4,
    },
    "data_analysis": {
        "display_name": "Data Analysis Agent",
        "description": "Data synthesis specialist",
        "investing_style": "Builds structured evidence from constraints, assumptions, and measurable indicators.",
        "agent_func": data_analysis_agent,
        "type": "analysis",
        "order": 5,
    },
    "case_analysis": {
        "display_name": "Case Analysis Agent",
        "description": "Case reasoning specialist",
        "investing_style": "Uses analogical reasoning with typical trade scenarios and failure patterns.",
        "agent_func": case_analysis_agent,
        "type": "analysis",
        "order": 6,
    },
}

# Derive ANALYST_ORDER from ANALYST_CONFIG for backwards compatibility
ANALYST_ORDER = [(config["display_name"], key) for key, config in sorted(ANALYST_CONFIG.items(), key=lambda x: x[1]["order"])]


def get_analyst_nodes():
    """Get the mapping of analyst keys to their (node_name, agent_func) tuples."""
    return {key: (f"{key}_agent", config["agent_func"]) for key, config in ANALYST_CONFIG.items()}


def get_agents_list():
    """Get the list of agents for API responses."""
    return [
        {
            "key": key,
            "display_name": config["display_name"],
            "description": config["description"],
            "investing_style": config["investing_style"],
            "order": config["order"]
        }
        for key, config in sorted(ANALYST_CONFIG.items(), key=lambda x: x[1]["order"])
    ]
