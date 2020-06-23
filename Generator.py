#!/usr/bin/env python3

import argparse
import csv
from itertools import islice
from lxml import etree

from generator.domain.PluralType import PluralType
from generator.domain.StringElement import StringElement
from generator.domain.PluralElement import PluralElement


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def parser():
        parser = argparse.ArgumentParser(
            description='Convert csv to Android localization files')

        parser.add_argument('-i', '--input', action="store", dest="input_file",
                            type=argparse.FileType('r', encoding='UTF-8'), help='CSV input file', required=True)
        parser.add_argument('-o', '--output', action="store", dest="output_file",
                            type=argparse.FileType('w+', encoding='UTF-8'), help='CSV input file', required=True)
        parser.add_argument('-k', '--key-column', action="store", dest="key_column",
                            type=int, help='Column for keys', default=0)
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
            if type(item) is PluralElement:
                AndroidPrinter.add_plural(resources, item)
            else:
                AndroidPrinter.add_string(resources, item)

        return resources

    @staticmethod
    def add_string(elem: etree.Element, item: StringElement):
        string = etree.SubElement(elem, "string")
        string.set('name', item.key)
        string.text = item.value

    @staticmethod
    def add_plural(elem: etree.Element, plural: PluralElement):
        plural_element = elem.find('.//plurals[@name="' + plural.key + '"]')
        if plural_element is None:
            plural_element = etree.SubElement(elem, "plurals")
            plural_element.set('name', plural.key)

        item_element = etree.SubElement(plural_element, 'item')
        item_element.set('quantity', plural.plural.value)
        item_element.text = plural.value


def main():
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
            if not value:
                print("WARNING: Key '" + key + "' has no value")
                # continue

            if plural is None:
                elements.append(StringElement(key, value))
            else:
                elements.append(PluralElement(key, value, PluralType(plural)))

    tree = AndroidPrinter.elements_to_etree(elements)

    tree[:] = sorted(tree, key=lambda elem: elem.get('name'))

    xml_str = etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8', standalone=True)

    with args.output_file as output_file:
        output_file.write(xml_str.decode("utf-8"))


if __name__ == '__main__':
    main()
