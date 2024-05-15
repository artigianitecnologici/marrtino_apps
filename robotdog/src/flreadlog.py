from flask import Flask, render_template
import re

app = Flask(__name__)

def extract_values(log_content):
    # Definisci il pattern regex per estrarre i valori
    pattern = r'name:\s*"([^"]+)"\s+message:\s*"([^"]+)"\s+hardware_id:\s*"([^"]+)"(?:\s+values:\s*(.*?)(?=^\s*(?:name:|$)))?'
    
    # Trova tutte le corrispondenze nel log
    matches = re.finditer(pattern, log_content, re.DOTALL | re.MULTILINE)
    
    # Lista per memorizzare i risultati
    results = []
    
    # Estrae i valori per ogni corrispondenza
    for match in matches:
        status_name = match.group(1)
        message = match.group(2)
        hardware_id = match.group(3)
        values_str = match.group(4)
        
        # Estrae i valori dei parametri
        values = {}
        if values_str:
            param_pattern = r'-\s+key:\s*"([^"]+)"\s+value:\s*"([^"]+)"'
            param_matches = re.finditer(param_pattern, values_str)
            for param_match in param_matches:
                key = param_match.group(1)
                value = param_match.group(2)
                values[key] = value
        
        # Aggiungi i risultati alla lista
        results.append({
            "status_name": status_name,
            "message": message,
            "hardware_id": hardware_id,
            "values": values
        })
    
    return results

@app.route('/')
def index():
    # Apri il file di log e leggi il contenuto
    with open('diag.txt', 'r') as file:
        log_content = file.read()
    
    # Estrai i valori dal contenuto del log
    extracted_values = extract_values(log_content)
    
    # Prepara i dati per la tabella HTML
    table_data = {}
    for result in extracted_values:
        hardware_id = result["hardware_id"]
        if hardware_id not in table_data:
            table_data[hardware_id] = {}
        for key, value in result["values"].items():
            if key not in table_data[hardware_id]:
                table_data[hardware_id][key] = []
            table_data[hardware_id][key].append(value)
    
    # Ritorna il template HTML con i dati
    return render_template('index.html', table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)
