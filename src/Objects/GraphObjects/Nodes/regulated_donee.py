from .node import Node


class RegulatedDonee(Node):

    def __init__(self, name, **kwargs):
        super(RegulatedDonee, self).__init__()
        self.name = name
        self.__dict__.update(kwargs)

    def render_unique_label(self):
        return self.name.replace(' ', '_')

    @property
    def node_id(self):
        return self.name + '_regulated_donee'
