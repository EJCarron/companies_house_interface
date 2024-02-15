from .officer import Officer
from .company import Company
from .regulated_donee import RegulatedDonee
from .officer_group import OfficerGroup

officer_str = Officer.__name__
company_str = Company.__name__
regulated_donee_str = RegulatedDonee.__name__
officer_group_str = OfficerGroup.__name__

officer = Officer
company = Company
regulated_donee = RegulatedDonee
officer_group = OfficerGroup

node_dict = {officer_str: Officer,
             company_str: Company,
             regulated_donee_str: RegulatedDonee,
             officer_group_str: OfficerGroup
             }
