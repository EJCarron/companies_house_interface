import json
import sys

from .GraphObjects.Nodes.company import Company
from .GraphObjects.Nodes.officer import Officer
from .GraphObjects.Nodes.officer_group import OfficerGroup
from .GraphObjects.Relationships.appointment import Appointment
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
    def officer_groups(self):
        return self.get_nodes_of_type(node_factory.officer_group)

    @property
    def appointments(self):
        return self.get_relationship_of_type(relationship_factory.appointment)

    @property
    def donations(self):
        return self.get_relationship_of_type(relationship_factory.donation)

    def get_officer(self, officer_id):
        self.officers.get(officer_id, None)

    def get_company(self, company_number):
        self.companies.get(company_number, None)

    def add_officer(self, officer):
        self.add_node(officer, node_factory.officer)

    # Officers can only appear in one group at a time so when new groups are added its oids need to be cross-referenced
    # against exists groups
    def add_officer_group(self, officer_group):

        if not isinstance(officer_group, node_factory.officer_group):
            print('tried to add not officer group to officer groups')
            sys.exit()

        for oid in officer_group.officer_ids:
            for current_officer_group in self.officer_groups.values():
                for coid in current_officer_group.officer_ids:
                    if oid == coid:
                        print(oid + ' already exists in a current officer group, no overlaps allowed')
                        sys.exit()

        self.nodes[officer_group.node_id] = officer_group

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

    def add_donation(self, donation):
        self.add_relationship(donation, relationship_factory.donation)

    def add_relationship(self, relationship, relationship_type=None):
        if isinstance(relationship, Relationship if relationship_type is None else relationship_type):
            self.relationships.append(relationship)
        else:
            print('Internal Error, tried to add none relationship to network relationships list')

    def standard_node_cyphers(self):
        nodes = []

        for node in self.nodes.values():
            if not isinstance(node, node_factory.officer_group):
                clause = node.render_create_clause()
                nodes.append(clause)
        return nodes

    def standard_relationship_cyphers(self):
        cypher = ''
        for relationship in self.relationships:
            cypher += '\n {clause}'.format(clause=relationship.render_create_clause())
        return cypher

    def find_officer_group(self, officer_id):
        for officer_group in self.officer_groups.values():
            if officer_id in officer_group.officer_ids:
                return officer_group
        return None

    def grouped_relationship_cyphers(self):
        cypher = ''

        for relationship in self.relationships:
            if isinstance(relationship, relationship_factory.appointment):
                officer_group = self.find_officer_group(relationship.parent_id)
                if officer_group is None:
                    pass
                else:
                    relationship.parent_node_name = officer_group.node_name()

            if isinstance(relationship, relationship_factory.donation):
                officer_group = self.find_officer_group(relationship.parent_id)
                if officer_group is None:
                    pass
                else:
                    relationship.parent_node_name = officer_group.node_name()

            cypher += '\n {clause}'.format(clause=relationship.render_create_clause())

        return cypher

    def officer_is_grouped(self, officer):

        for officer_group in self.officer_groups.values():
            if officer.node_id in officer_group.officer_ids:
                return True
        return False

    def grouped_node_cyphers(self):
        node_cyphers = []

        for node in self.nodes.values():
            if isinstance(node, node_factory.officer) and self.officer_is_grouped(node):
                continue
            else:
                node_cyphers.append(node.render_create_clause())

        return node_cyphers

    def render_create_cypher(self, group_officers=False):

        if group_officers:
            node_cyphers = self.grouped_node_cyphers()
        else:
            node_cyphers = self.standard_node_cyphers()

        nodes_string = ''

        for i in range(len(node_cyphers)):
            if i > 0:
                nodes_string += ', '

            nodes_string += '{node}'.format(node=node_cyphers[i])

        cypher_string = '''
        CREATE {nodes}
        '''.format(nodes=nodes_string)

        if group_officers:
            relationship_cyphers = self.grouped_relationship_cyphers()
        else:
            relationship_cyphers = self.standard_relationship_cyphers()

        cypher_string += relationship_cyphers

        return cypher_string

    # todo update this
    def to_dataframes(self):
        df_dict = {'officers': pd.DataFrame([o.to_flat_dict() for o in self.officers.values()]).drop(
            columns=['items', 'links_self']),
            'companies': pd.DataFrame(c.to_flat_dict() for c in self.companies.values()),
            'appointments': pd.DataFrame([a.to_flat_dict() for a in self.appointments]),
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
        print("getting  core officers")
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

        network = cls(nodes=core_companies)

        requests_count = network.expand_network(appointments_limit=appointments_limit, requests_count=requests_count)

        requests_count = network.process_new_officers(core_officers, requests_count)

        return network, requests_count

    def process_new_officers(self, core_officers, requests_count):
        print("processing new officers")

        new_companies = []

        for officer in core_officers.values():

            if officer.node_id not in self.nodes.keys():

                self.add_officer(officer)

                officer_new_companies, requests_count = self.process_officer_appointments(officer=officer,
                                                                                          requests_count=requests_count)
                new_companies += officer_new_companies

        self.add_companies_to_network(new_companies)

        return requests_count

    def add_companies_to_network(self, new_companies):

        for company in new_companies:
            self.add_company(company)

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

            appointment = Appointment(parent_node_name=officer.node_name(), child_node_name=company.node_name(),
                                      parent_id=officer.node_id, child_id=company.node_id,
                                      **item)
            self.add_appointment(appointment)

        return new_companies, requests_count

    def add_officers(self, officers):
        for officer in officers:
            self.add_officer(officer)

    def group_officers(self, officer_ids, group_name):
        officer_group = OfficerGroup(officer_ids=officer_ids, name=group_name)

        self.add_officer_group(officer_group)
