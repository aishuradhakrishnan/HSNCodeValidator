import pandas as pd
import os

class HSNValidator:
    def __init__(self, data_file_path=None):
        """
        Initialize the HSNValidator class.
        
        Args:
            data_file_path (str): The path to the HSN master dataset (Excel file).
                                  Defaults to a relative path if not provided.
        """
        self.data_file_path = data_file_path or os.path.join(os.path.dirname(__file__),  'data', 'HSN_SAC.xlsx')
        self.df = self.load_master_data()

    def load_master_data(self):
        """Loads the master data from an Excel file."""
        try:
            df = pd.read_excel(self.data_file_path, dtype=str)
            print("Columns in the dataframe:", df.columns)  
            df.columns = df.columns.str.strip()  
        
            if 'HSNCode' not in df.columns:
                raise KeyError('HSNCode column is missing in the dataset.')
        
            df['HSNCode'] = df['HSNCode'].astype(str)
            return df
        except Exception as e:
            raise FileNotFoundError(f"Error loading master data: {str(e)}")


    def validate_hsn_code(self, hsn_code):
        """
        Validates an HSN code against the master dataset.

        Args:
            hsn_code (str): The HSN code to validate

        Returns:
            dict: Validation result with valid status and additional info
        """
    
        if not hsn_code.isdigit():
            return {'valid': False, 'reason': 'Invalid format: HSN code must contain only digits'}

        if len(hsn_code) not in [2, 4, 6, 8]:
            return {'valid': False, 'reason': 'Invalid format: HSN code must be 2, 4, 6, or 8 digits long'}

        
        exact_match = self.df[self.df['HSNCode'] == hsn_code]
        if not exact_match.empty:
            return {
                'valid': True,
                'description': exact_match.iloc[0]['Description'],
                'validation_type': 'exact_match'
            }

        
        if len(hsn_code) > 2:
            
            parent_codes = [hsn_code[:i] for i in range(2, len(hsn_code) + 1, 2)]
            for parent in parent_codes:
                parent_match = self.df[self.df['HSNCode'] == parent]
                if not parent_match.empty:
                    return {
                        'valid': True,
                        'description': parent_match.iloc[0]['Description'],
                        'validation_type': 'hierarchical_match',
                        'parent_code': parent
                    }

        
        return {'valid': False, 'reason': 'Code not found in master data'}

    def validate_multiple_hsn_codes(self, hsn_codes):
        """
        Validates multiple HSN codes.

        Args:
            hsn_codes (list): List of HSN codes to validate

        Returns:
            dict: Dictionary with validation results for each code
        """
        results = {}
        for code in hsn_codes:
            results[code] = self.validate_hsn_code(code)
        return results
