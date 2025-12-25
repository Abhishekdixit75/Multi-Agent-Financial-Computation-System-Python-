# Step 0: Simple test to verify environment and agent framework

# A simple test agent
def test_agent(input_value: int) -> int:
    return input_value * 2

if __name__ == "__main__": # Our main block
    print("\n-------Step 0-------")
    input_value = 5
    output_value = test_agent(input_value)

    print(f"Input: {input_value}")
    print(f"Output: {output_value}\n")