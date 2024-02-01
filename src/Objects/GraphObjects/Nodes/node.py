import json
from src.Objects.GraphObjects.graph_object import Graph_Object


class Node(Graph_Object):
    bad_name_chars = ['-', '(', ')', '.', '@', '&', '\'', '’', '/', ',']

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def render_create_clause(self):

        parameters_string = self.render_parameters_string()

        clause_string = '''
        ({name}:{label} {{{parameters}}})
        '''.format(name=self.node_name(), label=type(self).__name__, parameters=parameters_string)

        return clause_string

    def node_name(self):

        node_name = self.render_unique_label()

        node_name = self.clean_name(node_name)

        return node_name

    def render_unique_label(self):
        return ''

    @classmethod
    def clean_name(cls, name):
        for bad in cls.bad_name_chars:
            name = name.replace(bad, '')

        if name[0].isnumeric():
            name = '_' + name

        return name
