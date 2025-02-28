from modules.config import os, tarfile, bz2, shutil
from tkinter import filedialog

print("Elite Log Viewer rev.2025-02-28 developed by Stefano Bandini")

# Select compress log file 
filename = filedialog.askopenfilename(filetypes=(("gz Files", ("*.gz", "*.bz2")), ("All Files", "*.*")))
path_base = os.path.expanduser("~/Documents/Elite_Log_output") # if not working well try eventually with os.path.expanduser("~/") 
# print(path_base)
folder_output = os.path.splitext(os.path.splitext(filename)[0])[0]
# print(folder_output)
folder_name = os.path.basename(folder_output)  # Extract folder name
# print(folder_name)
path_output = os.path.join(path_base, folder_name)
# print(path_output)

if not filename:  # verify if file is selected
    print('No file selected.')
else:
    # output path
    print(path_output)
    if not os.path.exists(path_output):
        os.makedirs(path_output, exist_ok=True)
        #print(f"Output folder: {path_output}")
        #print(f"File selected: {filename}")
    else:
        print(f"Folder {path_output} already exist.")
        # path_output = os.path.expanduser("~/Documents/Elite_Log_output")+folder_output
        # print(path_output)
        shutil.rmtree(path_output)  # Delete the entire directory
        os.makedirs(path_output, exist_ok=True)  # Recreate the directory

    try:
        # Estrazione dei file
        if filename.endswith('tar.gz'):
            with tarfile.open(filename, 'r:gz') as tar:
                tar.extractall(path=path_output, numeric_owner=False, filter='data')
        elif filename.endswith('tar'):
            with tarfile.open(filename, 'r:') as tar:
                tar.extractall(path=path_output, numeric_owner=False, filter='data')    
        else:
            print("File not supported.")

        # Leggi i file .log prima della decompressione
        existing_logs = set(f for f in os.listdir(path_output) if f.endswith('.log'))
            
        # Decompressione dei file .bz2 con aggiunta di .log
        new_logs = []
        for root, _, files in os.walk(path_output):
            for file in files:
                if file.endswith('.bz2'):
                    bz2_file_path = os.path.join(root, file)
                    decompressed_file_path = os.path.splitext(bz2_file_path)[0] + ".log"  # Aggiunge .log

                    # Decomprime il file
                    with bz2.BZ2File(bz2_file_path, 'rb') as bz2_file:
                        with open(decompressed_file_path, 'wb') as decompressed_file:
                            decompressed_file.write(bz2_file.read())

                    print(f"File expand: {decompressed_file_path}")

                    # Elimina il file .bz2
                    os.remove(bz2_file_path)
                    print(f"File bz2 eliminato: {bz2_file_path}")

        # Lista aggiornata dei file .log
        updated_logs = set(f for f in os.listdir(path_output) if f.endswith('.log'))

        # Identifica solo i nuovi file
        new_logs = list(updated_logs - existing_logs)
        
    except Exception as e:
        print(f"Errore: {e}")