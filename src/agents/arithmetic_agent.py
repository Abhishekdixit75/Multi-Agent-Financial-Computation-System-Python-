from tools.arithmetic_tools import add, subtract, divide

class ArithmeticAgent:
    def run(self, input_data: dict) -> dict:
        try:
            operation = input_data["operation"]
            a = input_data["value"]
            b = input_data["operand"]

            if operation == "add":
                result = add(a, b)
            elif operation == "subtract":
                result = subtract(a, b)
            elif operation == "divide":
                result = divide(a, b)
            else:
                raise ValueError("Invalid arithmetic operation")

            return {
                "value": result,
                "agent": "ArithmeticAgent",
                "status": "success",
                "message": "Arithmetic operation successful"
            }

        except Exception as e:
            return {
                "value": None,
                "agent": "ArithmeticAgent",
                "status": "failed",
                "message": str(e)
            }
    