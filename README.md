# Product Manager Assistant v1.0

A modular AI-driven product discovery assistant using [CrewAI](https://docs.crewai.com) and custom tools.

## What It Does

PM Assistant is a multi-agent pipeline that helps Product Managers:
- Run market research on competitors
- Analyze user feedback
- Generate product requirements
- Deliver a structured final report

All done through AI agents using structured prompts, tool integration, and task chaining.

## Project Structure

```
pm_assistant/
│
├── knowledge/                # Domain context & user feedback
│   ├── product_context.md #example of product context file
│   ├── kapsul_user_feedback.md #example of product feedback file
│   └── user_preference.txt
│
├── src/pm_assistant/         # Core application logic
│   ├── config/
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   ├── tools/
│   │   ├── serper_search_tool.py
│   │   ├── custom_tool.py
│   │   └── test_serper_tool.py
│   ├── crew.py
│   ├── main.py
│   └── final_report.md       # Output file
│
├── requirements.txt
├── pyproject.toml
└── .gitignore
```
##  Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/pm-assistant.git
cd pm-assistant/src/pm_assistant
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

Inside the `pm_assistant/` folder:

```env
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
```

## Run the Assistant

From the root `pm_assistant/` folder:

```bash
python main.py \
  --prompt "Explore the feasibility of adding AI features to Kapsul" \
  --feedback "./knowledge/kapsul_user_feedback.md" \
  --context "./knowledge/product_context.md"
```

## How It Works

- YAML files define the agents and tasks
- Tools like search and file reading are registered dynamically
- The `Crew` executes tasks in sequence
- Output is saved as `final_report.md`

## Features

- Dynamic, multi-agent workflow using CrewAI
- Task prompts inject PM goal + external files
- Custom tool support (Serper, Scraping, FileRead)
- Output structured for reuse
- Extendable tool registry and agent system

## Sample Inputs

- `knowledge/product_context.md`: Context for your product (e.g. Kapsul)
- `knowledge/kapsul_user_feedback.md`: Raw user quotes and feedback

## Roadmap

- [ ] Web interface
- [ ] Vector memory for persistent product understanding
- [ ] PDF/JSON report generation
- [ ] Modular UI preferences for agents/tasks

.. and much more

## Author

Built by [Abdelhamid Ameziane](https://www.linkedin.com/in/abdelhamid-ameziane/)

Contributions are welcome! feel free to fork and improve 🚀
