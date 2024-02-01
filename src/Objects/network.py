import json
from .GraphObjects.Nodes.company import Company
from .GraphObjects.Nodes.officer import Officer
from .GraphObjects.Relationships.appointment import Appointment
from .GraphObjects.Relationships.doppelganger import Doppelganger
from ..scripts import companies_house_api as cha
import pandas as pd


class Network:

    def __init__(self, officers=None, companies=None, appointments=None, doppelgangers=None):
        self.officers = {} if officers is None else officers
        self.companies = {} if companies is None else companies
        self.appointments = [] if appointments is None else appointments
        self.doppelgangers = [] if doppelgangers is None else doppelgangers

    def get_officer(self, officer_id):
        if officer_id in self.officers.keys():
            return self.officers[officer_id]
        else:
            return None

    def render_create_cypher(self):

        nodes = []

        for company in self.companies.values():
            nodes.append(company.render_create_clause())

        for officer in self.officers.values():
            nodes.append(officer.render_create_clause())

        nodes_string = ''

        for i in range(len(nodes)):
            if i > 0:
                nodes_string += ', '

            nodes_string += '{node}'.format(node=nodes[i])

        cypher_string = '''
        CREATE {nodes}
        '''.format(nodes=nodes_string)

        for appointment in self.appointments:
            cypher_string += '\n {clause}'.format(clause=appointment.render_create_clause())

        for doppelganger in self.doppelgangers:
            cypher_string += '\n {clause}'.format(clause=doppelganger.render_create_clause())
        return cypher_string

    def to_dataframes(self):
        df_dict = {'officers': pd.DataFrame([o.to_flat_dict() for o in self.officers.values()]).drop(
            columns=['items', 'links_self']),
            'companies': pd.DataFrame(c.to_flat_dict() for c in self.companies.values()),
            'appointments': pd.DataFrame([a.to_flat_dict() for a in self.appointments]),
            'doppelgangers': pd.DataFrame([d.to_flat_dict() for d in self.doppelgangers])
        }
        return df_dict

    def save_csvs(self, directory_path):
        dfs = self.to_dataframes()

        for attr, df in dfs.items():
            path = directory_path + '/{attr}.csv'.format(attr=attr)
            df.to_csv(path, index=False)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def save_json(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self, f, default=lambda o: o.__dict__,
                      sort_keys=True, ensure_ascii=False)

    def save_xlsx(self, path):

        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        dfs = self.to_dataframes()

        for sheet, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet, index=False)

        writer.close()

    @classmethod
    def load_json(cls, path):
        with open(path) as f:
            data = json.load(f)
        return cls(appointments=[Appointment(**appointment) for appointment in data['appointments']],
                   companies={company_number: Company(**company) for company_number, company in
                              data['companies'].items()},
                   officers={officer_id: Officer(**officer) for officer_id, officer in data['officers'].items()},
                   doppelgangers=[Doppelganger(**doppelganger) for doppelganger in data['doppelgangers']]
                   )

    @classmethod
    def start_from_officer(cls, officer_id, requests_count, appointments_limit=100):

        core_officer, requests_count = Officer.pull_data_and_init(officer_id=officer_id, requests_count=requests_count,
                                                                  appointments_limit=appointments_limit,

                                                                  )

        network = cls(officers={core_officer.officer_id: core_officer}, companies={}, appointments=[])

        new_companies, requests_count = network.process_officer_appointments(officer=core_officer,
                                                                             requests_count=requests_count)

        network.add_companies_to_network(new_companies)

        return network, requests_count

    def add_companies_to_network(self, new_companies):

        for company in new_companies:
            self.companies[company.company_number] = company

    def make_doppelganger_connection(self, parent_node_name, child_node_name):

        self.doppelgangers.append(Doppelganger(parent_node_name, child_node_name, **{}))

    def expand_network(self, appointments_limit, requests_count, layers=1):
        new_companies = self.companies.values()

        for i in range(layers):
            print("Network layer {0}".format(i))
            if len(new_companies) == 0:
                print('Reached Network Limit')
                break
            companies = []
            for company in new_companies:
                officer_ids, requests_count = cha.get_company_officer_ids(company_number=company.company_number,
                                                                          appointments_limit=appointments_limit,
                                                                          requests_count=requests_count
                                                                          )
                for officer_id in officer_ids:
                    if officer_id not in self.officers.keys():
                        officer, requests_count = Officer.pull_data_and_init(officer_id=officer_id,
                                                                             requests_count=requests_count,
                                                                             appointments_limit=appointments_limit)
                        if len(officer.items) == 0:
                            officer.manually_add_appointment_item(company_number=company.company_number)
                        self.officers[officer_id] = officer
                        officer_companies, requests_count = self.process_officer_appointments(officer, requests_count)
                        companies += officer_companies

            self.add_companies_to_network(companies)

            new_companies = companies
        return requests_count

    def process_officer_appointments(self, officer, requests_count):

        new_companies = []

        for item in officer.items:
            company_number = item['appointed_to']['company_number']
            if company_number not in self.companies.keys():
                company, requests_count = Company.pull_data_and_init(company_number, requests_count)
                new_companies.append(company)
            else:
                company = self.companies[company_number]

            appointment = Appointment(parent_node_name=officer.node_name(), child_node_name=company.node_name(), **item)
            self.appointments.append(appointment)

        return new_companies, requests_count

    @classmethod
    def start(cls, officer_ids, requests_count, appointments_limit):

        core_officers = {}

        for officer_id in officer_ids:
            core_officer, requests_count = Officer.pull_data_and_init(officer_id=officer_id,
                                                                      appointments_limit=appointments_limit,
                                                                      requests_count=requests_count)
            core_officers[officer_id] = core_officer

        network = cls(officers=core_officers, companies={}, appointments=[])

        print(len(network.officers.values()))

        new_companies = []

        for officer in network.officers.values():
            officer_new_companies, requests_count = network.process_officer_appointments(officer=officer,
                                                                                         requests_count=requests_count)
            new_companies += officer_new_companies

        network.add_companies_to_network(new_companies)

        return network, requests_count
