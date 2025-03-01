from typing import Optional, TypedDict

from lxml import etree
from pydantic.v1 import BaseModel

from spei import types
from spei.utils import to_snake_case, to_upper_camel_case  # noqa: WPS347


class DataDict(TypedDict, total=False):
    categoria: types.CategoriaOrdenPago
    id: Optional[str]
    fecha_oper: Optional[int]
    err_codigo: Optional[types.CodigoError]
    err_descripcion: Optional[str]


class Respuesta(BaseModel):
    err_codigo: types.CodigoError
    categoria: types.CategoriaOrdenPago
    id: Optional[str]
    fecha_oper: Optional[int]
    err_descripcion: Optional[str]

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True

    def build_xml(self):
        respuesta = etree.Element('respuesta')

        for element, value in self.dict(exclude={'categoria'}).items():  # noqa: WPS110
            if element in self.__fields__:
                upper_camel_case_element = to_upper_camel_case(element)
                subelement = etree.SubElement(respuesta, upper_camel_case_element)
                subelement.text = str(value)

        return respuesta

    @classmethod
    def parse_xml(cls, respuesta_element, categoria: types.CategoriaOrdenPago):
        respuesta_data: DataDict = {
            'categoria': categoria,
        }

        for sub_element in respuesta_element.getchildren():
            tag = to_snake_case(sub_element.tag)
            respuesta_data[tag] = sub_element.text  # type: ignore

        return cls(**respuesta_data)
