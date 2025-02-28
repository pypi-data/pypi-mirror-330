from modules.config import os, ET
from modules.fimport import path_output

def show_sim():
    """
    Read and parsing SIM.xml; show content in an HTML string.

    Returns:
        str: Stringa HTML with file data of SIM.xml.
    """
    # Percorso completo del file SIM.xml
    sim_file = os.path.join(path_output, "SIM.xml")
    
    # Verifica che il file SIM.xml esista
    if not os.path.isfile(sim_file):
        raise FileNotFoundError(f"file SIM.xml not found in directory: {sim_file}")
    
    # XML file parsing 
    tree = ET.parse(sim_file)
    root = tree.getroot()

    markdown_content = "# System Information\n\n"
    
    # Show main data
    markdown_content += f"**USB Serial Number**: {root.find('USBSerialNum').text}\n\n"
    markdown_content += f"**Gesak Level**: {root.find('GesakLevel').text}\n\n"
    markdown_content += f"**System Serial Number**: {root.find('SystemSerialNum').text}\n\n"
    markdown_content += f"**Unique ID**: {root.find('UniqueID').text}\n\n"

    # Product Type
    product = root.find("ProductType/Product")
    model = root.find("ProductType/Model")
    version = root.find("ProductType/Version")
    markdown_content += "## Product Type\n"
    markdown_content += f"- **Product**: {product.text if product is not None else 'N/A'}\n"
    markdown_content += f"- **Model**: {model.text if model is not None else 'N/A'}\n"
    markdown_content += f"- **Version**: {version.text if version is not None else 'N/A'}\n\n"

    # C-Arm Identification
    c_arm = root.find("CArmIdentification")
    markdown_content += "## C-Arm Identification\n"
    markdown_content += f"- **C-Arm Barcode**: {c_arm.find('CArmBarCode').text}\n"
    markdown_content += f"- **C-Arm Type**: {c_arm.find('CArmType').text}\n"
    markdown_content += f"- **Detector Type**: {c_arm.find('DetectorType').text}\n"
    markdown_content += f"- **Collimator Type**: {c_arm.find('CollimatorType').text}\n"
    markdown_content += f"- **Package Name**: {c_arm.find('PkgName').text}\n"
    markdown_content += f"- **Package UUID**: {c_arm.find('PkgUUID').text}\n\n"

    # Manufacture Info
    manufacture_info = root.find("ManufactureInfo")
    markdown_content += "## Manufacture Information\n"
    markdown_content += f"- **Manufacturing Code**: {manufacture_info.find('ManufacturingCode').text}\n"
    markdown_content += f"- **Year of Manufacture**: {manufacture_info.find('YearOfMnf').text}\n"
    markdown_content += f"- **Location of Manufacture**: {manufacture_info.find('LocOfMnf').text}\n\n"

    # Costed Options
    costed_options = root.find("CostedOptions")
    markdown_content += "## Costed Options\n"
    for option in costed_options:
        markdown_content += f"- **{option.tag}**: {option.text}\n"

    # Power Options
    markdown_content += "## Power Options\n"
    for option in root.findall("Power/Option"):
        voltage = option.find("Voltage").text
        current = option.find("Current").text
        location = option.find("Location").text
        markdown_content += f"- **Option {option.get('id')}**: {voltage}V, {current}A, Location: {location}\n"

    return markdown_content

