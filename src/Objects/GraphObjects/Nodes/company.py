from .node import Node
from src.scripts import companies_house_api as cha


class Company(Node):

    def __init__(self, **kwargs):
        super(Company, self).__init__()
        self.company_number = None
        self.company_name = None
        self.__dict__.update(kwargs)

    def render_unique_label(self):
        unique_label = '{name}_{id}'.format(name=self.company_name.replace(' ', '_'), id=self.company_number)
        return unique_label

    @property
    def node_id(self):
        return self.company_number

    @classmethod
    def pull_data_and_init(cls, company_number, requests_count):
        result, requests_count = cha.get_company(company_number, requests_count)

        if result is not None:
            result['company_name'] = cls.clean_name(name=result['company_name'])

            return cls(**result), requests_count
        else:
            return None, requests_count

    @property
    def name(self):
        return self.company_name
