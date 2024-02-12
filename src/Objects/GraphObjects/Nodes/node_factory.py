from .officer import Officer
from .company import Company
from .regulated_donee import RegulatedDonee

officer_str = Officer.__name__
company_str = Company.__name__
regulated_donee_str = RegulatedDonee.__name__

officer = Officer
company = Company
regulated_donee = RegulatedDonee

node_dict = {officer_str: Officer,
             company_str: Company,
             regulated_donee_str: RegulatedDonee
             }
