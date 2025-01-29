def tprint(text):
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    else:
        return "Error: tprint requires text to be enclosed in quotes."

def tadd(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {e}"
