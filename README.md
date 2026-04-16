# Foreign Trade Decision System

This project is a multi-agent decision system for foreign trade opportunities. It helps you evaluate whether a product/export direction is worth doing by decomposing decisions into key dimensions.

Current framework:

1. Market Agent - judges market demand, trend, competition intensity, and entry window
2. Customer Agent - evaluates channels, acquisition cost, conversion difficulty, and scalability
3. Product Agent - evaluates product competitiveness and differentiation opportunity
4. Supply Agent - evaluates supply chain stability and delivery risk
5. Profit Agent - evaluates margin structure and long-term profitability
6. Data Analysis Agent - turns expert outputs into measurable validation indicators
7. Case Analysis Agent - derives success/failure patterns from comparable scenarios
8. Trade Decision Agent - produces the final recommendation and action path

Decision chain:

```text
输入问题（外贸决策）
  ↓
专家 Agent 层（外贸角色）
  ↓
分析 Agent 层（数据 / 案例）
  ↓
决策 Agent（最终建议）
```

[![Twitter Follow](https://img.shields.io/twitter/follow/virattt?style=social)](https://twitter.com/virattt)

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended as commercial or legal advice
- No guarantee of business outcomes
- Creator assumes no liability for business losses

By using this software, you agree to use it solely for learning purposes.

## Table of Contents
- [How to Install](#how-to-install)
- [How to Run](#how-to-run)
  - [⌨️ Command Line Interface](#️-command-line-interface)
  - [🖥️ Web Application](#️-web-application)
- [How to Contribute](#how-to-contribute)
- [Feature Requests](#feature-requests)
- [License](#license)

## How to Install

Before running the system, install dependencies and set up your API keys.

### 1. Clone the Repository

```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

### 2. Set up API keys

Create a `.env` file for your API keys:
```bash
# Create .env file for your API keys (in the root directory)
cp .env.example .env
```

Open and edit the `.env` file to add your API keys:
```bash
# For running LLMs hosted by openai (gpt-4o, gpt-4o-mini, etc.)
OPENAI_API_KEY=your-openai-api-key

# Optional: add any domain data API keys you need
# YOUR_DATA_API_KEY=your-data-api-key
```

**Important**: You must set at least one LLM API key (e.g. `OPENAI_API_KEY`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY`, or `DEEPSEEK_API_KEY`).

## How to Run

### ⌨️ Command Line Interface

Run the foreign trade decision engine directly in terminal.

#### Quick Start

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

#### Run the Decision Engine
```bash
poetry run python -m src.main --question "我要不要做LED灯出口"
```

You can also specify `--ollama` to use a local model.

```bash
poetry run python -m src.main --question "我要不要做手机壳出口" --ollama
```

You can select a subset of agents:

```bash
poetry run python -m src.main --question "我要不要做工业设备出口" --analysts market,customer,product,supply,profit,data_analysis,case_analysis
```

### 🖥️ Web Application

Use the web app in `app/` if you prefer visual workflows.

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

**Important**: Please keep your pull requests small and focused.  This will make it easier to review and merge.

## Feature Requests

If you have a feature request, please open an [issue](https://github.com/virattt/ai-hedge-fund/issues) and make sure it is tagged with `enhancement`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
