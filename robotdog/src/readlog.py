import re

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

def main():
    # Apri il file di log e leggi il contenuto
    with open('diag.txt', 'r') as file:
        log_content = file.read()
    
    # Estrai i valori dal contenuto del log
    extracted_values = extract_values(log_content)
    
    # Stampa i risultati
    for result in extracted_values:
        print("Status Name:", result["status_name"])
        print("Message:", result["message"])
        print("Hardware ID:", result["hardware_id"])
        print("Values:")
        for key, value in result["values"].items():
            print("  {}: {}".format(key, value))
        print()

if __name__ == "__main__":
    main()
