
from hsn_validator import HSNValidator  

hsn_validator = HSNValidator()


result = hsn_validator.validate_hsn_code('0101')
print("Single HSN Code Validation Result:", result)


codes = ['0101', '9999', 'abcd']
results = hsn_validator.validate_multiple_hsn_codes(codes)
print("Multiple HSN Codes Validation Results:", results)
