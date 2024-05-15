from flask import Flask, render_template
import re

app = Flask(__name__)

def extract_values(log_content):
    pattern = r'name:\s*"([^"]+)"\s+message:\s*"([^"]+)"\s+hardware_id:\s*"([^"]+)"(?:\s+values:\s*(.*?)(?=^\s*(?:name:|$)))?'
    matches = re.finditer(pattern, log_content, re.DOTALL | re.MULTILINE)
    results = []
    for match in matches:
        status_name = match.group(1)
        message = match.group(2)
        hardware_id = match.group(3)
        values_str = match.group(4)
        values = {}
        if values_str:
            param_pattern = r'-\s+key:\s*"([^"]+)"\s+value:\s*"([^"]+)"'
            param_matches = re.finditer(param_pattern, values_str)
            for param_match in param_matches:
                key = param_match.group(1)
                value = param_match.group(2)
                values[key] = value
        results.append({
            "hardware_id": hardware_id,
            "values": values
        })
    return results

@app.route('/')
def index():
    with open('diag.txt', 'r') as file:
        log_content = file.read()
    extracted_values = extract_values(log_content)
    all_keys = set()
    for result in extracted_values:
        all_keys.update(result["values"].keys())
    sorted_keys = sorted(all_keys)
    return render_template('indexcol.html', extracted_values=extracted_values, sorted_keys=sorted_keys)

if __name__ == '__main__':
    app.run(debug=True)
