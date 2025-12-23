from mcp.server.fastmcp import FastMCP
import os
import glob
from utils import log_info, log_error
from icd_service import ICDService
from drug_service import DrugService

# 1. Initialize the MCP Server
mcp = FastMCP("Taiwan-Smart-Health-Agent")

# 2. Configure data paths
# In Docker, we mount or copy data to /app/data
DATA_DIR = "/app/data"

# Automatically find the ICD-10 Excel file. 
# This handles the long filename issue dynamically.
excel_files = glob.glob(os.path.join(DATA_DIR, "*.xlsx"))
if excel_files:
    ICD_FILE_PATH = excel_files[0]
    log_info(f"Found ICD Excel file: {ICD_FILE_PATH}")
else:
    ICD_FILE_PATH = os.path.join(DATA_DIR, "default.xlsx")
    log_error("No Excel file found in data directory!")

# 3. Initialize Services
# We pass the paths so the services can manage their own SQLite databases.
log_info("Initializing Services...")

try:
    # ICD Service: Handles diagnosis and procedure codes (Excel -> SQLite)
    icd_service = ICDService(ICD_FILE_PATH, DATA_DIR)
    
    # Drug Service: Handles FDA APIs (JSON -> SQLite ETL)
    drug_service = DrugService(DATA_DIR)
    
except Exception as e:
    log_error(f"Critical error initializing services: {e}")
    # We continue, but tools might fail if services aren't ready

# ==========================================
# Group 1: ICD-10 Tools (Diagnosis & Procedures)
# ==========================================

@mcp.tool()
def search_medical_codes(keyword: str, type: str = "all") -> str:
    """
    Search for ICD-10-CM (Diagnosis) or ICD-10-PCS (Procedure) codes.
    
    Args:
        keyword: Search term (e.g., 'Diabetes', 'E11', 'Appendectomy', '子宮內膜異位').
        type: Filter by 'diagnosis', 'procedure', or 'all'. Default is 'all'.
    """
    log_info(f"Tool called: search_medical_codes with query='{keyword}', type='{type}'")
    return icd_service.search_codes(keyword, type)

@mcp.tool()
def infer_complications(code: str) -> str:
    """
    Infers potential complications or specific sub-conditions based on ICD hierarchy.
    Example: Input 'E11' (Type 2 Diabetes) -> Returns specific codes like E11.9, E11.2 (with kidney complications).
    
    Args:
        code: The base diagnosis code (e.g., 'E11', 'N80').
    """
    log_info(f"Tool called: infer_complications with code='{code}'")
    return icd_service.infer_complications(code)

@mcp.tool()
def get_nearby_codes(code: str) -> str:
    """
    Retrieves codes immediately preceding and following the target code.
    Useful for differential diagnosis context or seeing related severity levels.
    
    Args:
        code: The target diagnosis code.
    """
    log_info(f"Tool called: get_nearby_codes with code='{code}'")
    return icd_service.get_nearby_codes(code)

@mcp.tool()
def check_medical_conflict(diagnosis_code: str, procedure_code: str) -> str:
    """
    Retrieves detailed definitions to analyze potential conflicts between a diagnosis and a procedure.
    Allows the AI to check if a procedure is appropriate for a given diagnosis.
    
    Args:
        diagnosis_code: Patient's diagnosis code (e.g., 'N80.A0').
        procedure_code: Intended procedure code (e.g., '0UT90ZZ').
    """
    log_info(f"Tool called: check_medical_conflict ({diagnosis_code} vs {procedure_code})")
    return icd_service.get_conflict_info(diagnosis_code, procedure_code)

# ==========================================
# Group 2: Drug Tools (Taiwan FDA Data)
# ==========================================

@mcp.tool()
def search_drug_info(keyword: str) -> str:
    """
    Search for Taiwan FDA approved drugs by name (Chinese/English) or indication.
    Returns basic information including License ID, Name, and Indication.
    
    Args:
        keyword: Drug name or symptom (e.g., 'Panadol', '普拿疼', '頭痛').
    """
    log_info(f"Tool called: search_drug_info with query='{keyword}'")
    return drug_service.search_drug(keyword)

@mcp.tool()
def get_drug_details(license_id: str) -> str:
    """
    Get comprehensive details for a specific drug license ID.
    Includes: Ingredients, Usage, Appearance (shape/color), and Package Insert links.
    
    Args:
        license_id: The specific license ID found via search (e.g., '衛部藥製字第058498號').
    """
    log_info(f"Tool called: get_drug_details for ID='{license_id}'")
    return drug_service.get_details(license_id)

@mcp.tool()
def identify_unknown_pill(features: str) -> str:
    """
    Identify a pill based on visual features using the appearance database.
    
    Args:
        features: Keywords describing the pill (e.g., 'white circle YP', 'oval pink').
                  Include shape, color, and markings if visible.
    """
    log_info(f"Tool called: identify_unknown_pill with features='{features}'")
    return drug_service.identify_pill(features)

# ==========================================
# Group 3: Composite Analysis (The "Doctor Brain")
# ==========================================

@mcp.tool()
def analyze_treatment_plan(diagnosis_keyword: str, drug_keyword: str) -> str:
    """
    [Advanced] Analyze the correlation between a diagnosis and a drug.
    Fetches data from both ICD-10 and FDA Drug databases to help evaluate treatment appropriateness.
    
    Args:
        diagnosis_keyword: The condition or disease name/code (e.g., 'Diabetes', 'E11').
        drug_keyword: The medication name (e.g., 'Metformin').
    """
    log_info(f"Tool called: analyze_treatment with diagnosis='{diagnosis_keyword}', drug='{drug_keyword}'")
    
    # 1. Search ICD (broad search first)
    icd_result = icd_service.search_codes(diagnosis_keyword, type="diagnosis")
    
    # 2. Search Drug
    drug_result = drug_service.search_drug(drug_keyword)
    
    # 3. Combine results for the LLM to process
    return f"""
=== Comprehensive Analysis Context ===

[Context 1: Diagnosis Data (ICD-10)]
Query: {diagnosis_keyword}
Results:
{icd_result}

-------------------

[Context 2: Medication Data (Taiwan FDA)]
Query: {drug_keyword}
Results:
{drug_result}

-------------------
SYSTEM INSTRUCTION: 
Based on the above retrieved data, please analyze:
1. Does the medication's indication match the diagnosis?
2. Are there any obvious contraindications based on the drug category?
3. Provide a brief summary for a healthcare professional.
"""

# --- Start Server ---
if __name__ == "__main__":
    log_info("Server is starting...")
    mcp.run()