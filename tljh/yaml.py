"""consolidated yaml API

ensures the same yaml settings for reading/writing
throughout tljh
"""
from ruamel.yaml.composer import Composer
from ruamel.yaml import YAML


class _NoEmptyFlowComposer(Composer):
    """yaml composer that avoids setting flow_style on empty
    containers.

    workaround ruamel.yaml issue #255
    """

    def compose_mapping_node(self, anchor):
        node = super().compose_mapping_node(anchor)
        if not node.value:
            node.flow_style = False
        return node

    def compose_sequence_node(self, anchor):
        node = super().compose_sequence_node(anchor)
        if not node.value:
            node.flow_style = False
        return node


# create the global yaml object:
yaml = YAML(typ="rt")
yaml.Composer = _NoEmptyFlowComposer
