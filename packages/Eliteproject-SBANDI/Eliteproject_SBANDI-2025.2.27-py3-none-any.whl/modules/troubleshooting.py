from modules.config import os, pd

def load_troubleshooting_csv(file_path):
    """
    Load troubleshooting.csv in Pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path, delimiter=';', encoding='latin1')
        return df
    except Exception as e:
        print(f"Errore during file CSV load: {e}")
        return pd.DataFrame()

# CSV path
csv_path = os.path.join(os.path.dirname(__file__), "troubleshooting.csv")

# Create DataFrame
troubleshooting_df = load_troubleshooting_csv(csv_path)