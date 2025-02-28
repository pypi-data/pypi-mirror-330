from pii_scanner.check_digit_warehouse.validators import VALIDATORS

def validate_check_digit(identifier, country=None):
    """
    Validate an identifier dynamically based on input and country.
    """
    country_validators = {}
    generic_validators = VALIDATORS.get("Generic", {})
    
    if country:
        country = country.upper()
        country_validators = VALIDATORS.get(country, {})
    
    # Check within the specified country and generic validators first
    for doc_type, validator in {**country_validators, **generic_validators}.items():
        try:
            if validator(identifier):
                return {
                    "success": True,
                    "type": doc_type,
                }
        except Exception:
            continue

    # # If not validated, fallback to checking all validators
    # for global_country, validators in VALIDATORS.items():
    #     if global_country == "Generic":
    #         continue
    #     for doc_type, validator in validators.items():
    #         try:
    #             if validator(identifier):
    #                 return {
    #                     "success": True,
    #                     "type": doc_type,
    #                     "message": f"Valid {doc_type} for {global_country}."
    #                 }
    #         except Exception:
    #             continue

    return None

# Example Usage
if __name__ == "__main__":
    examples = [
        ("22AAAAA0000A1Z5", "IN"),   # GSTIN
        ("123-45-6789", "US"),      # SSN
        ("4111111111111111", "US"), # Credit Card
        ("GB33BUKB20201555555555", "UK"),  # IBAN
        ("12345678901", "BR"),      # CPF
        ("9791234567890", None),    # ISBN (generic)
        ("123456789012", "BR"),     # RG
        ("FR1234567890", "FR"),     # SIREN
        ("IT1234567890", "IT"),     # Codice Fiscale
        # Add more test cases here...
    ]

    identifier = "DKHPG2140H"
    country = "IN"
    result = validate_identifier(identifier, country)
    print(f"Identifier: {identifier}, Country: {country or 'Generic'} -> {result}")
