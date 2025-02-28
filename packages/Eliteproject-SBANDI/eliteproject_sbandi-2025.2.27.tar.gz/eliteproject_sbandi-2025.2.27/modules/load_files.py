# Funzione per il caricamento dei file di log e la creazione di un DataFrame OTTIMIZZATO

from modules.config import os, pd, csv

from modules.fimport import path_output

def parse_log_file(file_path):
    """Legge un file di log e restituisce una lista di tuple con i dati estratti."""
    data = []
    try:
        with open(file_path, 'r', encoding='latin1') as file:
            reader = csv.reader(file, delimiter='\t')
            for parts in reader:
                if len(parts) >= 6:
                    timestamp, level, source, id_info, code, message = parts[:6]
                    date, time = timestamp.split('T') if 'T' in timestamp else (timestamp, '')

                    # Processamento ottimizzato del tempo
                    time = time.split('+')[0]  # Rimuove il fuso orario
                    if '.' in time:
                        time_main, ms_tz = time.split('.')
                        time = f"{time_main}.{ms_tz[:3]}"

                    data.append((date, time, level, source, id_info, code.strip(), message.strip()))
    except Exception as e:
        print(f"Errore durante la lettura di {file_path}: {e}")
    
    return data

def load_file(file_name):
    try:
        data = []

        if file_name == 'Merged Logs Default&Debug':
            files_to_load = ['Surgery-Default.log', 'Surgery-Debug.log']
            data = [entry for file in files_to_load for entry in parse_log_file(os.path.join(path_output, file))]

        elif file_name == 'Merged Logs Default&Debug + Historical data':
            log_files = [
                os.path.join(path_output, f) for f in os.listdir(path_output)
                if f.startswith(("Surgery-Default.log", "Surgery-Debug.log"))
            ]
            data = [entry for file_path in log_files for entry in parse_log_file(file_path)]

        else:
            data = parse_log_file(os.path.join(path_output, file_name))

        # Creazione DataFrame direttamente da una lista di tuple
        df = pd.DataFrame(data, columns=['Date', 'Time', 'Level', 'Source', 'ID Info', 'Code', 'Message'])

        # Conversione della data in datetime per un ordinamento più veloce
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
        df = df.sort_values(by=["DateTime"], ascending=True).drop(columns=['DateTime'])

        return df

    except Exception as e:
        print(f"Unable to read file: {e}")
        return pd.DataFrame()