import json
import sys

from .GraphObjects.Nodes.company import Company
from .GraphObjects.Nodes.officer import Officer
from .GraphObjects.Relationships.appointment import Appointment
from .GraphObjects.Relationships.doppelganger import Doppelganger
from .GraphObjects.Relationships.relationship import Relationship
from ..scripts import companies_house_api as cha
import pandas as pd
from .GraphObjects.Nodes.node import Node
from .GraphObjects.Nodes import node_factory
from .GraphObjects.Relationships import relationship_factory


class Network:
    clear_network_strings = ('match (a) -[r] -> () delete a, r', 'match (a) delete a',)

    def __init__(self, nodes=None, relationships=None):
        self.nodes = {} if nodes is None else nodes
        self.relationships = [] if relationships is None else relationships

    def get_nodes_of_type(self, node_type):

        found_nodes = {}

        for node_id, node in self.nodes.items():
            if isinstance(node, node_type):
                found_nodes[node_id] = node

        return found_nodes

    def get_relationship_of_type(self, relationship_type):
        found_relationships = []

        for relationship in self.relationships:
            if isinstance(relationship, relationship_type):
                found_relationships.append(relationship)

        return found_relationships

    @property
    def officers(self):
        return self.get_nodes_of_type(node_factory.officer)

    @property
    def companies(self):
        return self.get_nodes_of_type(node_factory.company)

    @property
    def regulated_donees(self):
        return self.get_nodes_of_type(node_factory.RegulatedDonee)

    @property
    def appointments(self):
        return self.get_relationship_of_type(relationship_factory.appointment)

    @property
    def donations(self):
        return self.get_relationship_of_type(relationship_factory.donation)

    @property
    def doppelgangers(self):
        return self.get_relationship_of_type(relationship_factory.doppelganger)

    def get_officer(self, officer_id):
        self.officers.get(officer_id, None)

    def get_company(self, company_number):
        self.companies.get(company_number, None)

    def add_officer(self, officer):
        self.add_node(officer, node_factory.officer)

    def add_company(self, company):
        self.add_node(company, node_factory.company)

    def add_regulated_donee(self, regulated_donee):
        self.add_node(regulated_donee, node_factory.regulated_donee)

    def add_node(self, node, node_type=None):
        if isinstance(node, Node if node_type is None else node_type):
            if node.node_id not in self.nodes.keys():
                self.nodes[node.node_id] = node
                return True
            else:
                return False
        else:
            print('Internal Error, tried to add none node to network nodes list')
            sys.exit()

    def add_appointment(self, appointment):
        self.add_relationship(appointment, relationship_factory.appointment)

    def add_doppelganger(self, doppelganger):
        self.add_relationship(doppelganger, relationship_factory.doppelganger)

    def add_donation(self, donation):
        self.add_relationship(donation, relationship_factory.donation)

    def add_relationship(self, relationship, relationship_type=None):
        if isinstance(relationship, Relationship if relationship_type is None else relationship_type):
            self.relationships.append(relationship)
        else:
            print('Internal Error, tried to add none relationship to network relationships list')

    def render_create_cypher(self):

        nodes = []

        for node in self.nodes.values():
            clause = node.render_create_clause()
            nodes.append(clause)

        nodes_string = ''

        for i in range(len(nodes)):
            if i > 0:
                nodes_string += ', '

            nodes_string += '{node}'.format(node=nodes[i])

        cypher_string = '''
        CREATE {nodes}
        '''.format(nodes=nodes_string)

        for relationship in self.relationships:
            cypher_string += '\n {clause}'.format(clause=relationship.render_create_clause())

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

        return cls(relationships=[relationship_factory.relationship_dict[relationship['relationship_type']]
                                  (**relationship) for relationship in data.get('relationships', [])],
                   nodes={node_id: node_factory.node_dict[node['node_type']](**node) for node_id, node in
                          data.get('nodes', {}).items()}
                   )

    @classmethod
    def init_officers(cls, officer_ids, appointments_limit, requests_count):
        core_officers = {}

        for officer_id in officer_ids:
            print(officer_id)
            core_officer, requests_count = Officer.pull_data_and_init(officer_id=officer_id,
                                                                      appointments_limit=appointments_limit,
                                                                      requests_count=requests_count)
            if core_officer is None:
                print('{0} officer id does not exist'.format(officer_id))
                continue

            core_officers[officer_id] = core_officer

        return core_officers, requests_count

    @classmethod
    def init_companies(cls, company_numbers, requests_count):
        companies = {}
        for company_number in company_numbers:
            company, requests_count = Company.pull_data_and_init(company_number, requests_count)

            if company is None:
                print("{0} company number does not exist".format(company_number))
                continue
            companies[company_number] = company
        return companies, requests_count

    @classmethod
    def start(cls, officer_ids, company_numbers, requests_count, appointments_limit=100):
        print("getting officers")
        core_officers, requests_count = cls.init_officers(officer_ids=officer_ids, requests_count=requests_count,
                                                          appointments_limit=appointments_limit)
        print("{0} officers fetched".format(len(core_officers.values())))
        print("getting companies")
        core_companies, requests_count = cls.init_companies(company_numbers=company_numbers,
                                                            requests_count=requests_count)
        print("{0} companies fetched".format(len(core_companies.values())))
        if len(core_officers.values()) == 0 and len(core_companies.values()) == 0:
            print("Nothing to work with")
            sys.exit()

        network = cls(nodes={**core_officers, **core_companies})

        requests_count = network.process_new_officers(requests_count)

        return network, requests_count

    def process_new_officers(self, requests_count):
        print("processing new officers")

        new_companies = []

        for officer in self.officers.values():
            officer_new_companies, requests_count = self.process_officer_appointments(officer=officer,
                                                                                      requests_count=requests_count)
            new_companies += officer_new_companies

        self.add_companies_to_network(new_companies)

        return requests_count

    def add_companies_to_network(self, new_companies):

        for company in new_companies:
            self.add_company(company)

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
                        self.add_officer(officer)
                        officer_companies, requests_count = self.process_officer_appointments(officer, requests_count)
                        companies += officer_companies

            self.add_companies_to_network(companies)

            new_companies = companies
        return requests_count

    def process_officer_appointments(self, officer, requests_count):
        print("processing {0}'s appointments".format(officer.name))
        new_companies = []

        for item in officer.items:
            company_number = item['appointed_to']['company_number']
            if company_number not in self.companies.keys():
                company, requests_count = Company.pull_data_and_init(company_number, requests_count)
                new_companies.append(company)
            else:
                company = self.companies[company_number]

            appointment = Appointment(parent_node_name=officer.node_name(), child_node_name=company.node_name(), **item)
            self.add_appointment(appointment)

        return new_companies, requests_count
