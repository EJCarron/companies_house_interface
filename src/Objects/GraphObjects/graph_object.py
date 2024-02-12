from collections.abc import MutableMapping


class Graph_Object:
    bad_name_chars = ['-', '(', ')', '.', '@', '&', '\'', '’', '/', ',', ' ']

    @classmethod
    def clean_name(cls, dirty_name):

        for bad in cls.bad_name_chars:
            dirty_name = dirty_name.replace(bad, '')

        if dirty_name[0].isnumeric():
            dirty_name = '_' + dirty_name

        return dirty_name

    def render_parameters_string(self):

        parameters_string = ''

        self_dict = self.to_flat_dict()

        first = True
        for attr, value in self_dict.items():
            if first:
                first = False
            else:
                parameters_string += ','
            parameters_string += self.handle_param(attr, value)

        return parameters_string

    def to_flat_dict(self):
        return flatten_dict(self.__dict__)

    def handle_param(self, attr, value):
        value_type = type(value)

        clean_attr = self.clean_name(attr)

        if value_type == str:
            if self.is_date_time(value):
                return '{attr}: date(\'{date}\')'.format(attr=clean_attr, date=value)
            else:
                value = value.replace('\'', '')
                return '{attr}: \'{value}\''.format(attr=clean_attr, value=value)
        elif value_type == bool:
            if value:
                return '{attr}: true'.format(attr=clean_attr, value=value)
            else:
                return '{attr}: false'.format(attr=clean_attr, value=value)
        elif value_type == int:
            return '{attr}: {value}'.format(attr=clean_attr, value=value)
        elif value_type == dict:
            print('bad dict somehow')
        else:
            return '{attr}: null'.format(attr=clean_attr, value=value)

    def is_date_time(self, param):

        splits = param.split('-')

        if len(splits) != 3:
            return False

        if splits[0].isnumeric() and len(splits[0]) == 4:
            if splits[1].isnumeric() and 0 < int(splits[1]) < 13:
                if splits[2].isnumeric() and 0 < int(splits[1]) < 32:
                    return True

        return False


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '_') -> MutableMapping:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
