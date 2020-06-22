from dataclasses import dataclass

from generator.domain.PluralType import PluralType
from generator.domain.StringElement import StringElement


@dataclass()
class PluralElement(StringElement):
    plural: PluralType
