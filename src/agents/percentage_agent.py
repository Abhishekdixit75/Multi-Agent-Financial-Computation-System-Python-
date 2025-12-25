from tools.percentage_tools import calculate_percentage

class PercentageAgent:
    def run(self, input_data: dict) -> dict:
        value = input_data["value"]
        percentage = input_data["percentage"]

        result = calculate_percentage(value, percentage)

        return {
            "value": result,
            "agent": "PercentageAgent",
            "status": "success",
            "message": "Percentage calculated successfully"
        }