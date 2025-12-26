from crewai import Agent, Task, Crew, Process
from agents.percentage_agent import PercentageAgent
from agents.arithmetic_agent import ArithmeticAgent
from agents.audit_agent import AuditAgent


percentage_agent_logic = PercentageAgent()
arithmetic_agent_logic = ArithmeticAgent()
audit_agent_logic = AuditAgent()


# CrewAI Agents
percentage_agent = Agent(
    role="PercentageAgent",
    goal="Execute Python function only. Do not generate text.",
    backstory="This agent strictly runs Python logic and returns structured output.",
    allow_delegation=False,
    verbose=False,
    llm=None
)

arithmetic_agent = Agent(
    role="ArithmeticAgent",
    goal="Execute Python function only. Do not generate text.",
    backstory="This agent strictly performs arithmetic using Python logic.",
    allow_delegation=False,
    verbose=False,
    llm=None
)

audit_agent = Agent(
    role="AuditAgent",
    goal="Validate Python output only. Do not generate text.",
    backstory="This agent validates results and logs status using Python logic.",
    allow_delegation=False,
    verbose=False,
    llm=None
)


# Initial Input
initial_data = {
    "value": 1000,
    "percentage": 10
}


# Custom Runnable Task
from typing import Callable, Any, Optional
from crewai.tasks.task_output import TaskOutput

class RunnableTask(Task):
    function: Optional[Callable] = None

    def execute_sync(
        self,
        agent: Optional[Agent] = None,
        context: Optional[Any] = None,
        tools: Optional[list] = None,
    ) -> TaskOutput:
        """
        Execute the task synchronously.
        If a python function is provided, run it directly.
        Otherwise, fallback to standard CrewAI execution.
        """
        if self.function:
            # Handle context argument if the function expects it
            import inspect
            sig = inspect.signature(self.function)
            
            if 'context' in sig.parameters:
                raw_result = self.function(context=context)
            else:
                raw_result = self.function()

            # Convert result to string for raw output, assuming JSON for structured
            # CrewAI usually expects a string in .raw
            result_str = str(raw_result)
            
            # Print the JSON output as requested
            import json
            if isinstance(raw_result, dict):
                print(json.dumps(raw_result, indent=2), flush=True)
            else:
                print(result_str, flush=True)
            
            task_output = TaskOutput(
                description=self.description,
                agent=self.agent.role if self.agent else "Unknown",
                raw=result_str,
                json_dict=raw_result if isinstance(raw_result, dict) else None,
                output_format="json" if isinstance(raw_result, dict) else "raw"
            )
            
            self.output = task_output
            return task_output
        
        return super().execute_sync(agent=agent, context=context, tools=tools)


# Task 1: PercentageAgent
def percentage_task_logic():
    result = percentage_agent_logic.run(initial_data)
    result["base_value"] = initial_data["value"]
    return result

percentage_task = RunnableTask(
    description="Calculate percentage of the given value",
    agent=percentage_agent,
    expected_output="Structured percentage result from Python function",
    function=percentage_task_logic,
    use_tools_only=True
)


# Task 2: ArithmeticAgent
def arithmetic_task_logic(context=None):
    # Bypass context and use direct task output
    # percentage_task.output is a TaskOutput object. We need the raw result to parse or the json_dict if available.
    # Our RunnableTask returns a TaskOutput with .json_dict populated for dict results.
    
    prev_output = percentage_task.output
    
    if hasattr(prev_output, 'json_dict') and prev_output.json_dict:
        data = prev_output.json_dict
    elif hasattr(prev_output, 'raw'):
        # Fallback to evaluating raw string if json_dict is missing (shouldn't be with our RunnableTask)
        try:
             import ast
             data = ast.literal_eval(prev_output.raw)
        except:
             raise ValueError("Could not parse previous task output")
    else:
        raise ValueError("Previous task output has no data")

    percentage_output = data["value"]
    base_value = data["base_value"]

    arithmetic_input = {
        "value": base_value,
        "operation": "add",
        "operand": percentage_output
    }

    return arithmetic_agent_logic.run(arithmetic_input)

arithmetic_task = RunnableTask(
    description="Add calculated percentage to base value",
    agent=arithmetic_agent,
    expected_output="Structured arithmetic result from Python function",
    function=arithmetic_task_logic,
    use_tools_only=True,
    context=[percentage_task]  # Explicitly pass dependency for context
)


# Task 3: AuditAgent
def audit_task_logic(context=None):
    # Bypass context and use direct task output
    prev_output = arithmetic_task.output
    
    if hasattr(prev_output, 'json_dict') and prev_output.json_dict:
        arithmetic_output = prev_output.json_dict
    elif hasattr(prev_output, 'raw'):
        import ast
        arithmetic_output = ast.literal_eval(prev_output.raw)
    else:
        raise ValueError("Previous task output has no data")

    audit_result = audit_agent_logic.run(arithmetic_output)

    if audit_result["status"] != "PASS":
        # raise RuntimeError("Audit failed. Stopping execution.")
        pass # Don't crash for now, let it return

    return audit_result

audit_task = RunnableTask(
    description="Audit the final result",
    agent=audit_agent,
    expected_output="Validated final output from Python function",
    function=audit_task_logic,
    use_tools_only=True,
    context=[arithmetic_task]
)

# Crew Orchestration
crew = Crew(
    agents=[percentage_agent, arithmetic_agent, audit_agent],
    tasks=[percentage_task, arithmetic_task, audit_task],
    process=Process.sequential,
    verbose=False,
    llm=None
)

if __name__ == "__main__":
    print("\n--- Step 2: Sequential Agent Orchestration ---\n")
    result = crew.kickoff()
    
    print("\nFinal Output:")
    print(result)