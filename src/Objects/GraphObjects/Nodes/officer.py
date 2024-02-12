from .node import Node
from ....scripts import companies_house_api as cha


class Officer(Node):
    def __init__(self, **kwargs):
        super(Officer, self).__init__()
        self.name = None
        self.officer_id = None
        self.items = None
        self.__dict__.update(kwargs)

    def manually_add_appointment_item(self, company_number):
        item = {'appointed_to': {'company_number': company_number}}
        self.items.append(item)
        return self

    def render_unique_label(self):

        unique_label = '{name}_{id}'.format(name=self.name.replace(' ', '_'), id=self.officer_id)
        return unique_label

    @property
    def node_id(self):
        return self.officer_id

    @classmethod
    def from_result(cls, result):

        result['officer_id'] = cha.extract_id_from_link(result['links']['self'])

        new_officer = cls(**result)

        return new_officer

    @classmethod
    def pull_data_and_init(cls, officer_id, appointments_limit, requests_count):

        result, requests_count = cha.get_officer(officer_id=officer_id, appointments_limit=appointments_limit,
                                                  requests_count=requests_count)

        if result is not None:
            if result is not None:
                result['name'] = cls.clean_name(dirty_name=result['name'])

            return cls.from_result(result), requests_count
        else:
            return None, requests_count
