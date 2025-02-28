"""Download structures and query information of CoRE MOF Database.
"""

try:
    from ccdc import io
    csd_reader = io.EntryReader('CSD')
except:
    print("You need to install CSD software with the license if you want to download all structures")

import os, json, requests, zipfile
from ase.io import read
from pymatgen.io.ase import AseAtomsAdaptor

from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

package_directory = os.path.abspath(__file__).replace("structure.py","")

files_to_download = {
                    'data/CSD/list_coremof_csd_unmodified_20250227.json': 'https://raw.githubusercontent.com/mtap-research/CoRE-MOF-Tools/main/7-data4API/CSD/list_coremof_csd_unmodified_20250227.json',
                    'data/detail_of_CR.json': 'https://raw.githubusercontent.com/mtap-research/CoRE-MOF-Tools/main/7-data4API/detail_of_CR.json',
                    'data/detail_of_NCR.json': 'https://raw.githubusercontent.com/mtap-research/CoRE-MOF-Tools/main/7-data4API/detail_of_NCR.json',
                    'data/CSD/CR_CSD_REFCODE.json': 'https://raw.githubusercontent.com/mtap-research/CoRE-MOF-Tools/main/7-data4API/CSD/CR_CSD_REFCODE.json',
                    'data/CSD/NCR_CSD_REFCODE.json': 'https://raw.githubusercontent.com/mtap-research/CoRE-MOF-Tools/main/7-data4API/CSD/NCR_CSD_REFCODE.json',
                    'data/SI/CR.zip': 'https://raw.githubusercontent.com/mtap-research/CoRE-MOF-Tools/main/7-data4API/SI/CR.zip',
                    'data/SI/NCR.zip': 'https://raw.githubusercontent.com/mtap-research/CoRE-MOF-Tools/main/7-data4API/SI/NCR.zip'
                    }

for file_name, url in files_to_download.items():
    
    file_path = os.path.join(package_directory, file_name)
    directory = os.path.dirname(file_path) 

    if not os.path.exists(directory):
        os.makedirs(directory)
        
    if not os.path.exists(file_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {file_name} to {file_path}")
        else:
            print(f"Failed to download {file_name} from {url}")
    else:
        pass


def make_primitive_p1(filename):


    """make primitive and make P1.

    Args:
        filename (str): path to your structure.

    Returns:
        cif:
            -   CIF after making primitive and make P1.   
    """     

    atoms = read(filename)
    structure_= AseAtomsAdaptor.get_structure(atoms)
    
    sga = SpacegroupAnalyzer(structure_)
    structure_prep = sga.get_primitive_standard_structure(international_monoclinic=True, keep_site_properties=False)
    structure_prep.to(filename=filename)
    

class download_from_SI():

    """download structures that we got from supporting information.

    Args:
        output_folder (str): path to save structures.

    Returns:
        cif
            -   CoRE MOF SI dataset.   
    """

    def __init__(self, output_folder="./CoREMOF2024DB"):
        
        self.SI_path = package_directory+'/data/SI/'
        self.output = output_folder
        self.run()

    def run(self):

        """start to run. 
        """
            
        CR_files = self.list_zip(self.SI_path+"CR.zip")
        NCR_files = self.list_zip(self.SI_path+"NCR.zip")
     
        os.makedirs(self.output+"/CR/", exist_ok=True)
        os.makedirs(self.output+"/NCR/", exist_ok=True)

        for file in CR_files[:]:
            self.get_from_SI(self.SI_path+"CR.zip", file, self.output)
        for file in NCR_files[:]:
            self.get_from_SI(self.SI_path+"NCR.zip", file, self.output)

    def list_zip(self, zip_path):

        """list of files from a ZIP.

        Args:
            zip_path (str): path to ZIP.

        Returns:
            List:
                -   name list from a ZIP.  
        """
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            return file_list
    
    def get_from_SI(self, zip_path, entry, output_folder):

        """unzip files from a ZIP.

        Args:
            zip_path (str): path to ZIP.
            entry (str): name of structure.
            output_folder (str): path to save structures. 
        """
                
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            if entry in file_list:
                zip_ref.extract(entry, output_folder)
            
def download_from_CSD(refcode, output_folder="./CoREMOF2024DB"):

    """download structures from CSD, you need to install [CSD python API](https://downloads.ccdc.cam.ac.uk/documentation/API/installation_notes.html) with licence.

    Args:
        refcode (str): path to refcode.
        output_folder (str): path to save structures.

    Returns:
        cif:
            -   downloading CIF.  
    """

    cryst = csd_reader.crystal(refcode)
    data = cryst.to_string('cif')
    f = open(os.path.join(output_folder, refcode+'.cif'),'w')
    f.write(data)
    f.close()

def get_list_CSD():

    """get the name list of structures from CSD.

    Returns:
        List:
            -   CR dataset from CSD.
            -   NCR dataset from CSD.
            -   unmodified dataset from CSD.
    """
            
    CSD_path = package_directory+'/data/CSD/'
    CR_json = CSD_path + "/CR_CSD_REFCODE.json"
    NCR_json  = CSD_path + "/NCR_CSD_REFCODE.json"
    CSD_unmodified_json  = CSD_path + "/list_coremof_csd_unmodified_20250227.json"

    with open (CR_json, "r") as CR_f:
        CSD_CR = json.load(CR_f)
        
    with open (NCR_json, "r") as NCR_f:
        CSD_NCR = json.load(NCR_f)

    with open (CSD_unmodified_json, "r") as CSD_unmodified_f:
        CSD_unmodified = json.load(CSD_unmodified_f)

    return CSD_CR, CSD_NCR, CSD_unmodified


def information(dataset, entry):

    """get information of CoRE MOF database.

    Args:
        dataset (str): name of subset.
        entry (str): name of structure

    Returns:
        Dictionary:
            -   properties, DOI, issues and so on. 
    """     

    CR_data_path = package_directory+'/data/detail_of_CR.json'
    NCR_data_path = package_directory+'/data/detail_of_NCR.json'

    with open (CR_data_path, "r") as CR_f:
        CR_data = json.load(CR_f)
        
    with open (NCR_data_path, "r") as NCR_f:
        NR_data = json.load(NCR_f)
    
    if dataset == "CR-ASR":
        print("unit:\n", CR_data["unit"])
        query_data = CR_data["ASR"]
    elif dataset == "CR-FSR":
        print("unit:\n", CR_data["unit"])
        query_data = CR_data["FSR"]
    elif dataset == "CR-Ion":
        print("unit:\n", CR_data["unit"])
        query_data = CR_data["Ion"]
    elif dataset == "NCR":
        query_data = NR_data

    return query_data[entry]