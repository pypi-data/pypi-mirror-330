
from stdnum.in_ import aadhaar, gstin, pan, vid
from stdnum.us import ssn
from stdnum import luhn, iban
from stdnum.ean import is_valid as is_valid_ean
from stdnum.imei import is_valid as is_valid_imei
from stdnum.isbn import is_valid as is_valid_isbn
from stdnum.dk import cpr
from stdnum.fr import siren, siret
from stdnum.it import codicefiscale
from stdnum.pl import pesel 
from stdnum.be import vat
from stdnum.au import abn
from stdnum.br import cpf


# Comprehensive Expanded Validators Mapping
VALIDATORS = {
    "IN": {
        "GST_NUMBER": gstin.is_valid,
        "AADHAAR_CARD": aadhaar.is_valid,
        "PAN_CARD": pan.is_valid,
        "VOTERID": vid.is_valid,
        "PASSPORT": lambda x: len(x) == 8,
    },
    "US": {
        "SSN": ssn.is_valid,
        "EIN": lambda x: len(x) == 9,
        "ITIN": lambda x: x.startswith("9") and len(x) == 9,
        "CreditCard": luhn.is_valid,
        "DRIVER_LICENSE": lambda x: len(x) >= 5,
        "PASSPORT": lambda x: len(x) == 9,
    },
    "AU": {
        "ABN": abn.is_valid,
        "TFN": lambda x: len(x) in (8, 9),
        "Medicare": lambda x: len(x) == 10,
        "DRIVER_LICENSE": lambda x: len(x) >= 6,
    },
    "BE": {
        "VAT": vat.is_valid,
        "BIS": lambda x: len(x) == 11,
        "DRIVER_LICENSE": lambda x: len(x) >= 6,
        # Add more identifiers here...
    },
    "BR": {
        "CPF": cpf.is_valid,
        "CNPJ": lambda x: len(x) == 14,
        "RG": lambda x: len(x) in [7, 9],
        "TituloEleitoral": lambda x: len(x) == 12,
        "PASSPORT": lambda x: len(x) == 8,
        # Add more identifiers here...
    },
    "IT": {
        "CodiceFiscale": codicefiscale.is_valid,
        "VAT": vat.is_valid,
        "PASSPORT": lambda x: len(x) == 9,
    },
    "PL": {
        "PESEL": pesel.is_valid,
        "VAT": vat.is_valid,
        "PASSPORT": lambda x: len(x) >= 8,
    },
    "DK": {
        "CPR": cpr.is_valid,
        # Add more identifiers here...
    },
    "FR": {
        "SIREN": siren.is_valid,
        "SIRET": siret.is_valid,
        "PASSPORT": lambda x: len(x) == 9,
        # Add more identifiers here...
    },
    "Generic": {
        "IBAN": iban.is_valid,
        "EAN": is_valid_ean,
        "IMEI": is_valid_imei,
        "ISBN": is_valid_isbn,
        "CreditCard": luhn.is_valid
    },
}