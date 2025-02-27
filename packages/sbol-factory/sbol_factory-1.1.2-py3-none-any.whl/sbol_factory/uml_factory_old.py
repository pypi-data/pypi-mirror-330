import abc
import os
from math import inf
from collections import OrderedDict

import graphviz
import sbol3 as sbol
import pylatex
import PyPDF2
if PyPDF2.__version__.split('.')[0] < '3':
   from PyPDF2 import PdfFileReader
else:
   # PdfFileReader is deprecated and was removed in PyPDF2 3.0.0. Use PdfReader instead.
   from PyPDF2 import PdfReader as PdfFileReader

from .query import Query


GLOBALS = set()

class UMLFactory(abc.ABC):
    """
    Class for generating UML diagrams from an ontology file
    """
    namespace_to_prefix = {}

    def __init__(self, ontology_path, ontology_namespace, output_path=None):
        self.namespace = ontology_namespace
        self.query = Query(ontology_path)
        self.tex = pylatex.Document()
        for prefix, ns in self.query.graph.namespaces():
            UMLFactory.namespace_to_prefix[str(ns)] = prefix
        self.prefix = UMLFactory.namespace_to_prefix[self.namespace]
        self.output_path = output_path

    def generate(self, output_path=None):
        if output_path:
            self.output_path=output_path
        if not self.output_path:
            raise ValueError('No output path specified')
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        dot = graphviz.Digraph()
        for class_uri in self.query.query_classes():
            # Don't try to document classes in the graph
            # that don't belong to this ontology specifically
            if self.namespace not in class_uri:
                continue
            print('Generating ' + class_uri)

            try:
                superclass_uri = self.query.query_superclass(class_uri)
            except:
                continue


            # Skip subclasses in the same ontology, since these
            # will be clustered into the same diagram as the super
            if self.namespace in self.query.query_superclass(class_uri):
                continue

            GLOBALS.add(class_uri)

            class_name = sbol.utils.parse_class_name(class_uri)
            # dot.graph_attr['splines'] = 'ortho'

            self.render_class_pattern(class_uri, dot)
            self.finish(dot) 

    def _generate(self, class_uri, drawing_method_callback, level, fig_ref,  *args):
        try:
            superclass_uri = self.query.query_superclass(class_uri)
        except:
            superclass_uri = None
        drawing_method_callback(class_uri, superclass_uri, level, fig_ref, *args)
        if class_uri in GLOBALS or class_uri in completed or 'sbol' in class_uri:
            return
        print(f'  Generating ' + class_uri)


        child_class_uris = [self.query.query_property_datatype(p, class_uri)[0] for p in self.query.query_compositional_properties(class_uri)]
        for uri in child_class_uris:
            self._generate(uri, drawing_method_callback, level, fig_ref, *args)

        subclass_uris = self.query.query_subclasses(class_uri)
        for uri in subclass_uris:
            level += 1
            self._generate(uri, drawing_method_callback, level, fig_ref, *args)

    @abc.abstractmethod
    def render_class_pattern(self, class_uri, dot):
        pass

    @abc.abstractmethod
    def finish(self, dot):
        pass
 
