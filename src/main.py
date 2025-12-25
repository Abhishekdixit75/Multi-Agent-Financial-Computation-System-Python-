# Step 1: Agent Design & Logic Explanation

from agents.percentage_agent import PercentageAgent
from agents.arithmetic_agent import ArithmeticAgent
from agents.audit_agent import AuditAgent

if __name__ == "__main__":
    percentage_agent = PercentageAgent()
    arithmetic_agent = ArithmeticAgent()
    audit_agent = AuditAgent()

    input_data = {
        "value": 200,
        "percentage": 10
    }

    input_data_arithmetic = {
        "value": 200,
        "operand": 0,
        "operation": "divide"
    }

    input_data_audit = {
        "value": 200,
    }

    output = percentage_agent.run(input_data)
    output_arithmetic = arithmetic_agent.run(input_data_arithmetic)
    output_audit = audit_agent.run(input_data_audit)
    print(output)
    print(output_arithmetic)
    print(output_audit)