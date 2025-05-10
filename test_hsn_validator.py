# Import the HSNValidator class from your module
from hsn_validator import HSNValidator  # Make sure the path is correct

# Initialize the validator with the default path to HSN master data
hsn_validator = HSNValidator()

# Validate a single HSN code
result = hsn_validator.validate_hsn_code('0101')
print("Single HSN Code Validation Result:", result)

# Validate multiple HSN codes
codes = ['0101', '9999', 'abcd']
results = hsn_validator.validate_multiple_hsn_codes(codes)
print("Multiple HSN Codes Validation Results:", results)
