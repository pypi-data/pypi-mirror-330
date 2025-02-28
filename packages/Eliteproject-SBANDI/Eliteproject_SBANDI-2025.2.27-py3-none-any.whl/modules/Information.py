from modules.config import os, ET
from modules.fimport import path_output

# Funzione per estrarre informazioni da Surgery-Default.log
def get_software_build_version():
    log_file = os.path.join(path_output, 'Surgery-Default.log')
    try:
        with open(log_file, 'r', encoding='latin1') as file:
            for idx, line in enumerate(file, start=1):  # Aggiunge l'indice per debug
                if 'Software Build Version' in line:
                    print(f"DEBUG: Trovato a riga {idx}: {line.strip()}")
                    version_info = line.split('Software Build Version:')[1].strip()
                    # Troncamento a "Software Part Number" se presente
                    if 'Software Part Number' in version_info:
                        version_info = version_info.split('Software Part Number')[0].strip()
                    return version_info
    except Exception as e:
        print(f"Errore durante la lettura di Surgery-Default.log: {e}")
    return "N/A"

# Funzione per estrarre informazioni da SIM.xml
def get_sim_info():
    sim_file = os.path.join(path_output, 'SIM.xml')
    info = {"SystemSerialNum": "N/A", "DetectorType": "N/A", "Product": "N/A"}
    try:
        tree = ET.parse(sim_file)
        root = tree.getroot()
        
        # Estrazione SystemSerialNum (direttamente alla radice)
        system_serial_num = root.find("SystemSerialNum")
        if system_serial_num is not None and system_serial_num.text:
            info["SystemSerialNum"] = system_serial_num.text.strip()
        
        # Estrazione DetectorType (sotto CArmIdentification)
        c_arm_identification = root.find("CArmIdentification")
        if c_arm_identification is not None:
            detector_type = c_arm_identification.find("DetectorType")
            if detector_type is not None and detector_type.text:
                info["DetectorType"] = detector_type.text.strip()
        
        # Estrazione Product (sotto ProductType)
        product_type = root.find("ProductType")
        if product_type is not None:
            product = product_type.find("Product")
            if product is not None and product.text:
                info["Product"] = product.text.strip()

    except Exception as e:
        print(f"Errore durante la lettura di SIM.xml: {e}")
    return info