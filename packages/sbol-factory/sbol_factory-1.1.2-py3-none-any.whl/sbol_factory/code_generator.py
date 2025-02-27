from .query import Query
from .shacl_validator import ShaclValidator
from .loader import OntologyLoader

import sbol3 as sbol
from sbol3 import PYSBOL3_MISSING, SBOL_TOP_LEVEL, SBOL_IDENTIFIED

# pySBOL extension classes are aliased because they are not present in SBOL-OWL
from sbol3 import CustomTopLevel as TopLevel
from sbol3 import CustomIdentified as Identified

import rdflib
import os
import sys
import importlib
import logging


SBOL = 'http://sbols.org/v3#'
OM = 'http://www.ontology-of-units-of-measure.org/resource/om-2/'
PROVO = 'http://www.w3.org/ns/prov#'


logging.basicConfig()
LOGGER = logging.getLogger(__name__)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(message)s'))
LOGGER.addHandler(ch)
ch2 = logging.StreamHandler()
ch2.setLevel(logging.ERROR)
ch2.setFormatter(logging.Formatter('[%(levelname)s] %(filename)s %(lineno)d: %(message)s'))
LOGGER.addHandler(ch2)


class Document(sbol.Document):

    def __init__(self):
        super(Document, self).__init__()
        self._validator = ShaclValidator()        

    def validate(self):
        conforms, results_graph, results_txt = self._validator.validate(self.graph())
        return ValidationReport(conforms, results_txt)


class ValidationReport():

    def __init__(self, is_valid, results_txt):
        self.is_valid = is_valid
        self.results = results_txt
        self.message = ''
        if not is_valid:
            i_message = results_txt.find('Message: ') + 9
            self.message = results_txt[i_message:]

    def __repr__(self):
        return self.message


class CodeGenerator():

    graph = rdflib.Graph()
    graph.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rdf/sbolowl3.rdf'), format ='xml')
    graph.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rdf/prov-o.owl'), format ='xml')
    graph.namespace_manager.bind('sbol', Query.SBOL)
    graph.namespace_manager.bind('owl', Query.OWL)
    graph.namespace_manager.bind('rdfs', Query.RDFS)
    graph.namespace_manager.bind('rdf', Query.RDF)
    graph.namespace_manager.bind('xsd', Query.XSD)
    graph.namespace_manager.bind('om', Query.OM)
    graph.namespace_manager.bind('prov', Query.PROVO)

    # Prefixes are used to automatically generate module names
    namespace_to_prefix = {}

    def __new__(cls, module_name, ontology_path, ontology_namespace, verbose=False):
        if verbose is False:
            logging.disable(logging.INFO)
        CodeGenerator.graph.parse(ontology_path, format=rdflib.util.guess_format(ontology_path))
        for prefix, ns in CodeGenerator.graph.namespaces():
            CodeGenerator.namespace_to_prefix[str(ns)] = prefix
            # TODO: handle namespace with conflicting prefixes

        # Use ontology prefix as module name
        CodeGenerator.module_name = CodeGenerator.namespace_to_prefix[ontology_namespace]
        if not os.path.isdir(module_name):
            os.mkdir(module_name)

        ontology_namespace = ontology_namespace
        CodeGenerator.query = Query(ontology_path)
        symbol_table = []
        for class_uri in CodeGenerator.query.query_classes():
            symbol_table = CodeGenerator.generate(class_uri, symbol_table, ontology_namespace)
        IMPORTS = '\n'.join([f'import {cls} from .{cls.lower()}' for cls in symbol_table])
        with open(os.path.join(module_name, '__init__.py'), 'w', encoding='utf-8') as f_init:
            f_init.write(IMPORTS) 
        return object.__new__(cls)



    @staticmethod
    def generate(class_uri, symbol_table, ontology_namespace):
        log = ''
        if ontology_namespace not in class_uri: 
            return symbol_table

        # Recurse into superclass
        superclass_uri = CodeGenerator.query.query_superclass(class_uri)
        symbol_table = CodeGenerator.generate(superclass_uri, symbol_table, ontology_namespace)

        CLASS_URI = class_uri
        CLASS_NAME = sbol.utils.parse_class_name(class_uri)

        if CodeGenerator.get_constructor(class_uri, symbol_table):  # Abort if the class has already been generated
            return symbol_table
        print('Generating ' + class_uri)

        #Logging
        LOGGER.info(f'\n{CLASS_NAME}\n')
        LOGGER.info('-' * (len(CLASS_NAME) - 2) + '\n')
        CodeGenerator.define_class(CLASS_URI, symbol_table)
        CodeGenerator.log(CLASS_URI)
        symbol_table.append(CLASS_NAME)
        return symbol_table

    @staticmethod
    def get_constructor(class_uri, symbol_table):

        if class_uri == SBOL_IDENTIFIED:
            return sbol.CustomIdentified
        if class_uri == SBOL_TOP_LEVEL:
            return sbol.CustomTopLevel

        # First look in the module we are generating
        class_name = sbol.utils.parse_class_name(class_uri)
        if class_name in symbol_table:
            return symbol_table[class_name]

        # Look in submodule
        namespace = None
        if '#' in class_uri:
            namespace = class_uri[:class_uri.rindex('#')+1]
        elif '/' in class_uri:
            namespace = class_uri[:class_uri.rindex('/')+1]
        else:
            raise ValueError(f'Cannot parse namespace from {class_uri}. URI must use either / or # as a delimiter.')

        # Look in the sbol module 
        if namespace == SBOL or namespace == PROVO or namespace == OM:
            return sbol.__dict__[class_name]

        # Look in other ontologies
        module_name = CodeGenerator.namespace_to_prefix[namespace]
        if module_name in sys.modules and class_name in sys.modules[module_name].__dict__:
            return sys.modules[module_name].__dict__[class_name]

        return None



    @staticmethod
    def clear():
        Query.graph = None
        modules = []
        ontology_modules = []
        for name, module in sys.modules.items():
            modules.append((name, module))
        for name, module in modules:
            if '__loader__' in module.__dict__ and type(module.__loader__) is OntologyLoader:
                ontology_modules.append(name)
        for name in ontology_modules:
            del sys.modules[name]

    @staticmethod
    def delete(symbol):
        del globals()[symbol]

    @staticmethod
    def define_class(class_uri, symbol_table):
        CLASS_URI = class_uri
        CLASS_NAME = sbol.utils.parse_class_name(class_uri)
        superclass_uri = CodeGenerator.query.query_superclass(class_uri)
        SUPERCLASS_NAME = sbol.utils.parse_class_name(class_uri)


        EXTENSION_TYPE = ''
        if 'http://sbols.org/v3#' in superclass_uri and not superclass_uri == SBOL_TOP_LEVEL and not superclass_uri == SBOL_IDENTIFIED:
            if SBOLFactory.query.is_top_level(CLASS_URI):
                EXTENSION_TYPE = 'self._rdf_types.append(sbol.SBOL_TOP_LEVEL)\n'
            else:
                EXTENSION_TYPE = 'self._rdf_types.append(sbol.SBOL_IDENTIFIED)\n'




        def compile_properties(class_uri, property_uris, property_type):
           PROPERTY_TEMPLATE = 'self.{property_name} = sbol.{property_type}(self, {property_uri}, {lower_bound}, {upper_bound})'
           if not property_uris:
               return '\b' * 5  # remove indentation and extra newline
           lines = []
           for property_uri in property_uris:
               property_name = CodeGenerator.query.query_label(property_uri).replace(' ', '_')
               lower_bound, upper_bound = CodeGenerator.query.query_cardinality(property_uri, class_uri)
               lines.append(PROPERTY_TEMPLATE.format(
                                property_name=property_name,
                                property_type=property_type,
                                property_uri=property_uri,
                                lower_bound=lower_bound,
                                upper_bound=upper_bound
                           ))
           return '\n'.join(lines)

        COMPOSITIONAL_PROPERTIES = compile_properties(
            CLASS_URI,
            CodeGenerator.query.query_compositional_properties(CLASS_URI),
            'OwnedObject'
        )
        ASSOCIATIVE_PROPERTIES = compile_properties(
            CLASS_URI,
            CodeGenerator.query.query_associative_properties(CLASS_URI),
            'ReferencedObject'
        )
        TEXT_PROPERTIES = compile_properties(
            CLASS_URI,
            CodeGenerator.query.query_text_properties(CLASS_URI),
            'TextProperty'
        )
        INT_PROPERTIES = compile_properties(
            CLASS_URI,
            CodeGenerator.query.query_int_properties(CLASS_URI),
            'IntProperty'
        )
        BOOL_PROPERTIES = compile_properties(
            CLASS_URI,
            CodeGenerator.query.query_bool_properties(CLASS_URI),
            'BooleanProperty'
        )
        DATETIME_PROPERTIES = compile_properties(
            CLASS_URI,
            CodeGenerator.query.query_datetime_properties(CLASS_URI),
            'DateTimeProperty'
        )
        URI_PROPERTIES = compile_properties(
            CLASS_URI,
            CodeGenerator.query.query_uri_properties(CLASS_URI),
            'URIProperty'
        )

        arg_names = [arg.replace(' ', '_') for arg in CodeGenerator.query.query_required_properties(CLASS_URI)]
        BUILDER_KWARGS = '\n'.join([f'kwargs[{arg}]: PYSBOL3_MISSING' for arg in arg_names])

        class_definition = '''
import sbol3 as sbol
from {MODULE_NAME} import {SUPERCLASS_NAME}


class {CLASS_NAME}({SUPERCLASS_NAME}):

    def __init__(self, identity, *args, type_uri='{CLASS_URI}', **kwargs):
        super().__init__(identity, *args, type_uri=type_uri, **kwargs)
        {EXTENSION_TYPE}
        {COMPOSITIONAL_PROPERTIES}
        {ASSOCIATIVE_PROPERTIES}
        {TEXT_PROPERTIES}
        {INT_PROPERTIES}
        {BOOL_PROPERTIES}
        {DATETIME_PROPERTIES}
        {URI_PROPERTIES}

        for kw, val in kwargs.items():
            if kw == 'type_uri':
                continue
            if kw in self.__dict__:
                try:
                    self.__dict__[kw].set(val)
                except:
                    # TODO: should this throw an exception?
                    pass

    def accept(self, visitor):
        visitor_method = f'visit_{VISITOR}'
        getattr(visitor, visitor_method)(self)


    def builder(identity, type_uri):
        kwargs['type_uri'] = type_uri
        {BUILDER_KWARGS}
        return {CLASS_NAME}(identity, **kwargs)

    sbol.Document.register_builder('{CLASS_URI}', builder)'''
        with open(os.path.join(CodeGenerator.module_name, CLASS_NAME.lower() + '.py'), 'w', encoding='utf-8') as f_class:
            f_class.write(
                class_definition.format(
                    CLASS_URI=CLASS_URI,
                    CLASS_NAME=CLASS_NAME,
                    SUPERCLASS_NAME=SUPERCLASS_NAME,
                    MODULE_NAME=SUPERCLASS_NAME.lower(),
                    EXTENSION_TYPE=EXTENSION_TYPE,
                    COMPOSITIONAL_PROPERTIES=COMPOSITIONAL_PROPERTIES,
                    ASSOCIATIVE_PROPERTIES=ASSOCIATIVE_PROPERTIES,
                    TEXT_PROPERTIES=TEXT_PROPERTIES,
                    INT_PROPERTIES=INT_PROPERTIES,
                    BOOL_PROPERTIES=BOOL_PROPERTIES,
                    DATETIME_PROPERTIES=DATETIME_PROPERTIES,
                    URI_PROPERTIES=URI_PROPERTIES,
                    VISITOR=CLASS_NAME.lower(),
                    BUILDER_KWARGS=BUILDER_KWARGS
                )
            )
        return symbol_table


    @staticmethod
    def log(class_uri):
        # Print out properties -- this is for logging only
        CLASS_URI = class_uri
        property_uris = CodeGenerator.query.query_object_properties(CLASS_URI)
        for property_uri in property_uris:
            property_name = CodeGenerator.query.query_label(property_uri).replace(' ', '_')
            datatype = CodeGenerator.query.query_property_datatype(property_uri, CLASS_URI)
            if len(datatype):
                datatype = sbol.utils.parse_class_name(datatype[0])
            else:
                datatype = None
            lower_bound, upper_bound = CodeGenerator.query.query_cardinality(property_uri, CLASS_URI)
            LOGGER.info(f'\t{property_name}\t{datatype}\t{lower_bound}\t{upper_bound}\n')
        property_uris = CodeGenerator.query.query_datatype_properties(CLASS_URI)
        for property_uri in property_uris:
            property_name = CodeGenerator.query.query_label(property_uri).replace(' ', '_')
            datatype = CodeGenerator.query.query_property_datatype(property_uri, CLASS_URI)
            if len(datatype):
                datatype = sbol.utils.parse_class_name(datatype[0])
            else:
                datatype = None
            lower_bound, upper_bound = CodeGenerator.query.query_cardinality(property_uri, CLASS_URI)            
            LOGGER.info(f'\t{property_name}\t{datatype}\t{lower_bound}\t{upper_bound}\n')

