import os
from math import inf
from collections import OrderedDict

import sbol3 as sbol
import graphviz

import sbol_factory.utils as utils


def draw_abstraction_hierarchy(dot, class_qname, subclass_qnames, header_level):

    label = f'{class_qname}|'
    label = '{' + label + '}'  # graphviz syntax for record-style label
    draw_uml_record(dot, class_qname, label)
    
    for subclass_qname in subclass_qnames:
        draw_inheritance(dot, class_qname, subclass_qname)
        label = self.label_properties(uri)
        draw_uml_record(dot, subclass_qname, label)
        fig_ref = class_qname
        draw_class_definition(uri, class_uri, header_level, fig_ref, dot)

 
def draw_class_definition(class_uri, superclass_uri, header_level, fig_ref, dot_graph=None):

    CLASS_URI = class_uri
    CLASS_NAME = sbol.utils.parse_class_name(class_uri)
    SUPERCLASS_NAME = sbol.utils.parse_class_name(superclass_uri)

    log = ''
    prefix = ''
    qname = utils.format_qname(class_uri)
    label = f'{qname}|'

    #draw_inheritance(dot, superclass_uri, class_uri)

    # Object properties can be either compositional or associative
    property_uris = self.query.query_object_properties(CLASS_URI)
    compositional_properties = self.query.query_compositional_properties(CLASS_URI)
    associative_properties = [uri for uri in property_uris if uri not in
                                compositional_properties]

    # Initialize associative properties
    for property_uri in associative_properties:
        if len(associative_properties) != len(set(associative_properties)):
            print(f'{property_uri} is found more than once')
        property_name = self.query.query_label(property_uri).replace(' ', '_')
        property_name = utils.format_qname(property_uri)
        lower_bound, upper_bound = self.query.query_cardinality(property_uri, class_uri)
        if upper_bound == inf:
            upper_bound = '*'
        object_class_uri = self.query.query_property_datatype(property_uri, CLASS_URI)[0]
        arrow_label = f'{property_name} [{lower_bound}..{upper_bound}]'
        draw_association(dot, class_uri, object_class_uri, arrow_label)
        # self.__dict__[property_name] = sbol.ReferencedObject(self, property_uri, 0, upper_bound)

    # Initialize compositional properties
    for property_uri in compositional_properties:
        if len(compositional_properties) != len(set(compositional_properties)):
            print(f'{property_uri} is found more than once')
        property_name = self.query.query_label(property_uri).replace(' ', '_')
        property_name = utils.format_qname(property_uri)
        lower_bound, upper_bound = self.query.query_cardinality(property_uri, class_uri)
        if upper_bound == inf:
            upper_bound = '*'
        object_class_uri = self.query.query_property_datatype(property_uri, CLASS_URI)[0]
        arrow_label = f'{property_name} [{lower_bound}..{upper_bound}]'
        draw_composition(dot, class_uri, object_class_uri, arrow_label)

    # Initialize datatype properties
    property_uris = self.query.query_datatype_properties(CLASS_URI)
    for property_uri in property_uris:
        property_name = self.query.query_label(property_uri).replace(' ', '_')
        property_name = utils.format_qname(property_uri)

        # Get the datatype of this property
        datatypes = self.query.query_property_datatype(property_uri, CLASS_URI)
        if len(datatypes) == 0:
            continue
        if len(datatypes) > 1:  # This might indicate an error in the ontology
            raise
        # Get the cardinality of this datatype property
        lower_bound, upper_bound = self.query.query_cardinality(property_uri, class_uri)
        if upper_bound == inf:
            upper_bound = '*'

        datatype = sbol.utils.parse_class_name(datatypes[0])
        if datatype == 'anyURI':
            datatype = 'URI'
        label += f'{property_name} [{lower_bound}..{upper_bound}]: {datatype}\\l'
    label = '{' + label + '}'  # graphviz syntax for record-style label
    draw_uml_record(dot, class_uri, label)
    # if not dot_graph:
    #     source = graphviz.Source(dot.source.replace('\\\\', '\\'))
    #     source.render(f'./uml/{CLASS_NAME}')
    return [dot_graph]

def draw_uml_record(dot_graph, class_qname, label):
    node_format = {
        'label' : None,
        'fontname' : 'Bitstream Vera Sans',
        'fontsize' : '8',
        'shape': 'record'
        }
    node_format['label'] = label
    dot_graph.node(sanitize(class_qname), **node_format)


def draw_association(dot_graph, parent_qname, child_qname, label):
    association_relationship = {
            'xlabel' : None,
            'arrowtail' : 'odiamond',
            'arrowhead' : 'vee',
            'fontname' : 'Bitstream Vera Sans',
            'fontsize' : '8',
            'dir' : 'both'
        }
    association_relationship['xlabel'] = label
    dot_graph.edge(sanitize(parent_qname), sanitize(child_qname), **association_relationship)
    label = '{' + child_qname + '|}'
    draw_uml_record(dot_graph, sanitize(child_qname), label)


def draw_composition(dot_graph, parent_qname, child_qname, label):
    composition_relationship = {
            'xlabel' : None,
            'arrowtail' : 'diamond',
            'arrowhead' : 'vee',
            'fontname' : 'Bitstream Vera Sans',
            'fontsize' : '8',
            'dir' : 'both'
        }
    composition_relationship['xlabel'] = label
    dot_graph.edge(sanitize(parent_qname), sanitize(child_qname), **composition_relationship)
    label = '{' + child_qname + '|}'
    draw_uml_record(dot_graph, child_qname, label)


def draw_inheritance(dot_graph, superclass_qname, subclass_qname):
    inheritance_relationship = {
            'label' : None,
            'arrowtail' : 'empty',
            'fontname' : 'Bitstream Vera Sans',
            'fontsize' : '8',
            'dir' : 'back'
        }
    dot_graph.edge(sanitize(superclass_qname), sanitize(subclass_qname), **inheritance_relationship)
    label = '{' + superclass_qname + '|}'
    draw_uml_record(dot_graph, superclass_qname, label)


def label_properties(self, class_uri):
    class_name = sbol.utils.parse_class_name(class_uri)
    qname = utils.format_qname(class_uri)
    label = f'{qname}|'

    # Object properties can be either compositional or associative
    property_uris = self.query.query_object_properties(class_uri)
    compositional_properties = self.query.query_compositional_properties(class_uri)
    associative_properties = self.query.query_associative_properties(class_uri)
    if len(associative_properties) != len(set(associative_properties)):
        raise ValueException(f'{property_uri} is found more than once')
    if len(compositional_properties) != len(set(compositional_properties)):
        raise ValueException(f'{property_uri} is found more than once')

    # Label associative properties
    for property_uri in associative_properties:
        property_name = self.query.query_label(property_uri).replace(' ', '_')
        property_name = utils.format_qname(property_uri)
        lower_bound, upper_bound = self.query.query_cardinality(property_uri, class_uri)
        if upper_bound == inf:
            upper_bound = '*'
        object_class_uri = self.query.query_property_datatype(property_uri, class_uri)
        arrow_label = f'{property_name} [{lower_bound}..{upper_bound}]'

    # Label compositional properties
    for property_uri in compositional_properties:
        property_name = self.query.query_label(property_uri).replace(' ', '_')
        property_name = utils.format_qname(property_uri)
        cardinality = self.query.query_cardinality(property_uri, class_uri)
        lower_bound, upper_bound = self.query.query_cardinality(property_uri, class_uri)
        if upper_bound == inf:
            upper_bound = '*'
        object_class_uri = self.query.query_property_datatype(property_uri, class_uri)
        arrow_label = f'{property_name} [{lower_bound}..{upper_bound}]'

    # Label datatype properties
    property_uris = self.query.query_datatype_properties(class_uri)
    for property_uri in property_uris:
        property_name = self.query.query_label(property_uri).replace(' ', '_')
        property_name = utils.format_qname(property_uri)

        # Get the datatype of this property
        datatypes = self.query.query_property_datatype(property_uri, class_uri)
        if len(datatypes) == 0:
            continue
        if len(datatypes) > 1:  # This might indicate an error in the ontology
            raise
        # Get the cardinality of this datatype property
        lower_bound, upper_bound = self.query.query_cardinality(property_uri, class_uri)
        if upper_bound == inf:
            upper_bound = '*'
        datatype = sbol.utils.parse_class_name(datatypes[0])
        if datatype == 'anyURI':
            datatype = 'URI'
        label += f'{property_name} [{lower_bound}..{upper_bound}]: {datatype}\\l'
    label = '{' + label + '}'  # graphviz syntax for record-style label
    return label




def format_description(self, class_uri):
    tex_description = self.query.query_comment(class_uri)
    class_list = self.query.query_classes()
    for uri in class_list:
        prefix = format_prefix(uri)
        if prefix == '':
            continue
        class_name = sbol.utils.parse_class_name(uri)
        qname = utils.format_qname(uri)
        tex_description = tex_description.replace(f' {qname} ', f' \\{prefix}{{{class_name}}} ')
        tex_description = tex_description.replace(f' {qname}.', f' \\{prefix}{{{class_name}}}.')
        tex_description = tex_description.replace(f' {qname},', f' \\{prefix}{{{class_name}}},')

        tex_description = tex_description.replace(f' {class_name} ', f' \\{prefix}{{{class_name}}} ')
        tex_description = tex_description.replace(f' {class_name}.', f' \\{prefix}{{{class_name}}}.')
        tex_description = tex_description.replace(f' {class_name},', f' \\{prefix}{{{class_name}}},')

    return tex_description
            

def remove_duplicates(dot_source):
    d = OrderedDict()
    entries = dot_source.split('\n')
    for e in entries:
        d[e] = None
    dot_source = '\n'.join(list(d.keys()))
    return dot_source


def sanitize(qname):
    return qname.replace(':', '_')
