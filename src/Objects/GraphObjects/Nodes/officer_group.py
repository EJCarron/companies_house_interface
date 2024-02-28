from .node import Node


class OfficerGroup(Node):

    def __init__(self, officer_ids, name, **kwargs):
        super(OfficerGroup, self).__init__()
        self.officer_ids = officer_ids
        self.name = name
        self.__dict__.update(kwargs)

    @property
    def node_id(self):
        return ''.join(self.officer_ids)

    def render_unique_label(self):
        return self.name.replace(' ', '_') + 'Group'
