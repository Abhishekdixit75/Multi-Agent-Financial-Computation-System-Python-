from tools.audit_tools import validate_value

class AuditAgent:
    def run(self, input_data: dict) -> dict:
        try:
            value = input_data["value"]
            validate_value(value)

            return {
                "value": value,
                "agent": "AuditAgent",
                "status": "success",
                "message": "Audit passed"
            }

        except Exception as e:
            return {
                "value": None,
                "agent": "AuditAgent",
                "status": "failed",
                "message": str(e)
            }
