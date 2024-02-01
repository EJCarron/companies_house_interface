from src.Objects.GraphObjects.graph_object import Graph_Object


class Relationship(Graph_Object):

    def __init__(self, parent_node_name, child_node_name, **params):
        self.parent_node_name = parent_node_name
        self.child_node_name = child_node_name
        self.__dict__.update(params)

    def render_create_clause(self):
        parameters_string = self.render_parameters_string()

        clause = '''
        CREATE ({parent})-[: {relationship} {{{parameters}}}]->({child})
        '''.format(parent=self.parent_node_name, child=self.child_node_name, relationship=type(self).__name__,
                   parameters=parameters_string)
        return clause
