import json
from src.Objects.GraphObjects.graph_object import Graph_Object


class Node(Graph_Object):

    def __init__(self):
        self.node_type = type(self).__name__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def render_create_clause(self):

        parameters_string = self.render_parameters_string()

        clause_string = '''
        ({name}:{label} {{{parameters}}})
        '''.format(name=self.node_name(), label=self.node_type, parameters=parameters_string)

        return clause_string

    def node_name(self):

        node_name = self.render_unique_label()

        node_name = self.clean_name(node_name)

        return node_name

    @property
    def node_id(self):
        return 'need to implement node_id property'

    def render_unique_label(self):
        return 'need to implement render unique label'
