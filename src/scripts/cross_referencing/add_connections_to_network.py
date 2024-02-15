from src.data.political_influence_lists.political_influence_lists_params import lists
import pandas as pd
from src.Objects.GraphObjects.Nodes import node_factory
from src.Objects.GraphObjects.Relationships import relationship_factory


def add_connections_to_network(network, connections_directory):
    for influence_list in lists:
        company_connections_df = pd.read_csv(connections_directory + influence_list['company_connections_path'])
        officer_connections_df = pd.read_csv(connections_directory + influence_list['officer_connections_path'])

        company_connections = company_connections_df.to_dict('records')
        officer_connections = officer_connections_df.to_dict('records')

        def add_to_network(connections, node_dict):
            for connection in connections:
                new_node_name = connection[influence_list['node_name_col']]
                new_node_params = {k: connection[k] for k in influence_list['node_params_cols']}

                child_node = node_factory.node_dict[influence_list['node_type']](name=new_node_name, **new_node_params)

                parent_node = node_dict.get(connection['connection_id'], None)

                if child_node is None:
                    print('Error connection Node ID not found in network')
                    continue

                new_relationship = relationship_factory.relationship_dict[influence_list['relationship_type']] \
                    (parent_node_name=parent_node.node_name(),
                     parent_node_id=parent_node.node_id,
                     child_node_name=child_node.node_name(),
                     child_node_id=child_node.node_id,
                     **connection
                     )

                network.add_node(child_node)
                network.add_relationship(new_relationship)

        add_to_network(company_connections, network.companies)
        add_to_network(officer_connections, network.officers)
