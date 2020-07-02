#!/usr/bin/env python3

import argparse
import csv
import logging
from itertools import islice
from lxml import etree
import re

import xml.dom.minidom

from generator.domain.PluralType import PluralType
from generator.domain.StringElement import StringElement
from generator.domain.PluralElement import PluralElement


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def parser():
        parser = argparse.ArgumentParser(
            description='Convert csv to Android strings.xml')

        required = parser.add_argument_group('required arguments')
        required.add_argument('-i', '--input', action="store", dest="input_file",
                            type=argparse.FileType('r', encoding='UTF-8'), help='CSV input file', required=True)

        parser.add_argument('-o', '--output', action="store", dest="output_file",
                            type=argparse.FileType('w+', encoding='UTF-8'), help='CSV input file')
        parser.add_argument('-k', '--key-column', action="store", dest="key_column",
                            type=int, help='Column for keys', required=True)
        parser.add_argument('-v', '--value-column', action="store", dest="value_column",
                            type=int, help='Column for values', required=True)
        parser.add_argument('-p', '--plural-column', action="store", dest="plural_column",
                            type=int, help='Column for plural values', required=True)
        parser.add_argument('-r', '--start-row', action="store", dest="start_row",
                            type=int, help='Row where data starts', default=0)

        return parser


class AndroidPrinter:
    def __init__(self):
        pass

    @staticmethod
    def elements_to_etree(elements):
        resources = etree.Element('resources')
        for item in elements:
            if not item.value:
               continue
            elif type(item) is PluralElement:
                AndroidPrinter.add_plural(resources, item)
            else:
                AndroidPrinter.add_string(resources, item)

        return resources

    @staticmethod
    def add_string(elem: etree.Element, item: StringElement):
        string = etree.SubElement(elem, "string")
        string.set('name', item.key)
        string.text = AndroidPrinter.escape(item.value)

    @staticmethod
    def add_plural(elem: etree.Element, plural: PluralElement):
        if not plural.value:
            return

        plural_element = elem.find('.//plurals[@name="' + plural.key + '"]')

        # If plural wrapper doesn't exist, create it.
        if plural_element is None:
            plural_element = etree.SubElement(elem, "plurals")
            plural_element.set('name', plural.key)

        item_element = etree.SubElement(plural_element, 'item')
        item_element.set('quantity', plural.plural.value)
        item_element.text = AndroidPrinter.escape(plural.value)

    @staticmethod
    def escape(text):
        return text.replace("\"", "\\\"").replace("'", "\\'")


def main():
    logging.basicConfig(format='%(message)s')
    log = logging.getLogger(__name__)

    parser = Parser().parser()
    args = parser.parse_args()
    elements = []
    with args.input_file as input_file:
        csv_data = csv.reader(input_file)
        for row in islice(csv_data, args.start_row, None):
            key = row[args.key_column]
            value = row[args.value_column]
            plural = row[args.plural_column] or None
            if not key:
                continue

            if plural is None:
                elements.append(StringElement(key, value))
            else:
                log.warning("Key '" + key + "' has no value")
                elements.append(PluralElement(key, value, PluralType(plural)))

    tree = AndroidPrinter.elements_to_etree(elements)

    # Sort elements
    tree[:] = sorted(tree, key=lambda elem: elem.get('name'))

    xml_str = etree.tostring(tree, encoding='UTF-8')

    # Work around for pretty printing
    decoded_str = xml_str.decode("utf-8")
    dom = xml.dom.minidom.parseString(decoded_str)
    pretty_xml_as_string = dom.toprettyxml(indent="    ", encoding='UTF-8')
    decoded_str = pretty_xml_as_string.decode("utf-8")

    if args.output_file is not None:
        with args.output_file as output_file:
            output_file.write(decoded_str)
    else:
        print(decoded_str)


if __name__ == '__main__':
    main()
