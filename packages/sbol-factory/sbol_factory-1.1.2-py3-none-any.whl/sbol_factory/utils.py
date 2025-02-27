import sbol3 as sbol


def format_qname(class_uri, ns_to_prefix_map):
    class_name = sbol.utils.parse_class_name(class_uri)
    qname = class_name
    prefix = format_prefix(class_uri, ns_to_prefix_map)
    if prefix:
        qname = prefix + ':' + class_name
    return qname


def format_prefix(class_uri, ns_to_prefix_map):
    for ns, prefix in ns_to_prefix_map.items():
        if ns in class_uri:
            return prefix
    return ''

