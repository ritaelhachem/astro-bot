def calculate(expression: str):
    try:
        result = eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
