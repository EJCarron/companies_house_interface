from src.Objects.GraphObjects.graph_object import Graph_Object


class Relationship(Graph_Object):

    def __init__(self, parent_node_name, child_node_name, **params):
        self.relationship_type = type(self).__name__
        self.parent_node_name = parent_node_name
        self.child_node_name = child_node_name
        self.__dict__.update(params)

    def render_create_clause(self):
        parameters_string = self.render_parameters_string()

        clause = '''
        CREATE ({parent})-[: {relationship} {{{parameters}}}]->({child})
        '''.format(parent=self.clean_name(self.parent_node_name), child=self.clean_name(self.child_node_name),
                   relationship=self.relationship_type,
                   parameters=parameters_string)
        return clause
