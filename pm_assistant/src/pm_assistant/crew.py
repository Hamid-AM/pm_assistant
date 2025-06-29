import os
import yaml

from pathlib import Path
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process

#Load environment variables
load_dotenv()

#Paths to config files
BASE_DIR = Path(__file__).resolve().parent
AGENTS_PATH = BASE_DIR / "config" / "agents.yaml"
TASKS_PATH = BASE_DIR / "config" / "tasks.yaml"

#Tool registry
def get_tool_registry(user_feedback_path: str = None):
    from tools.serper_search_tool import SerperSearchTool
    from crewai_tools import ScrapeWebsiteTool, FileReadTool

    registry = {
        "SerperSearchTool": SerperSearchTool,
        "ScrapeWebsiteTool": ScrapeWebsiteTool(),
    }

    if user_feedback_path:
        registry["FileReadTool"] = FileReadTool() #tool to Read user feedback file

    return registry

#Function to build agents from YAML
def load_agents(tool_registry, shared_context = ""):
    with open(AGENTS_PATH, "r") as f:
        agents_yaml = yaml.safe_load(f)

    agents = {}
    for key, agent in agents_yaml.items():
        agent_tools = [tool_registry[t] for t in agent.get("tools", []) if t in tool_registry]
        agents[key] = Agent(
            role=agent["role"],
            goal=agent["goal"],
            backstory=agent["backstory"] + f"\n\n-- \n Product Context {shared_context}",
            tools=agent_tools,
            verbose=True,  # Show progress in terminal
        )
    return agents

#Function to build tasks from YAML
def load_tasks(agent_map, pm_goal, feedback_file, output_format="md", max_urls=3):
    with open(TASKS_PATH, "r") as f:
        tasks_yaml = yaml.safe_load(f)

    tasks = []

    for key, task in tasks_yaml.items():
        # inject dynamic values into task descriptions
        description = task["description"].format(
            pm_goal=pm_goal,
            feedback_file=feedback_file,
            max_urls=max_urls,
        )

        output_file = None

        if key == "final_report":
            output_file = f"final_report.{output_format}"

        # Other tasks just build off prior context
        task_obj = Task(
            agent=agent_map[task["agent"]],
            description=description,
            expected_output=task["expected_output"],
            output_file=output_file,
        )
        tasks.append(task_obj)

    return tasks

#Main crew builder
def create_pm_assistant_crew(pm_goal: str,
                             user_feedback_file: str = None,
                             product_context_file: str = None):

    # Load product background once
    try:
        with open(product_context_file, "r", encoding="utf-8") as f:
            product_context = f.read().strip()
    except FileNotFoundError:
        print(f"[WARN] Product context file not found at: {product_context_file}")
        product_context = ""
    except Exception as e:
        print(f"[ERROR] Failed to load product context: {e}")
        product_context = ""
    # Load tool registry with optional user feedback file 
    tool_registry = get_tool_registry(user_feedback_file)
    # Load agents from YAML config
    # and inject product context into their backstories
    # This allows agents to reference product context in their tasks and discussions
    agents = load_agents(tool_registry, shared_context=product_context)

    tasks = load_tasks(
                        agents,
                        pm_goal=pm_goal,
                        feedback_file=user_feedback_file,
                        output_format="md",
                        max_urls=3
                        )

    # Sequential Crew: task 1 → task 2 → task 3 → final report
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    return crew

