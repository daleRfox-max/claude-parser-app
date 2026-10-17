import pandas as pd
import json

def sanitize_spreadsheet(file_buffer, file_type):
    """Ingests and cleans Excel or CSV files to preserve types and spaces."""
    try:
        if file_type == "xlsx":
            df = pd.read_excel(file_buffer, dtype=str)
        else:
            df = pd.read_csv(file_buffer, dtype=str)
        
        cleaned_rows = []
        for index, row in df.iterrows():
            row_dict = {
                str(k).strip(): (str(v).strip() if pd.notna(v) else None) 
                for k, v in row.to_dict().items()
            }
            row_dict["_original_row_index"] = index + 2
            cleaned_rows.append(row_dict)
            
        return cleaned_rows
    except Exception as e:
        raise ValueError(f"Error parsing file: {str(e)}")
