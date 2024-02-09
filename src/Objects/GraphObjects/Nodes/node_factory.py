from .officer import Officer
from .company import Company
from .regulated_donee import RegulatedDonee

node_factory = {'Officer': Officer,
                'Company': Company,
                'RegulatedDonee': RegulatedDonee
                }
