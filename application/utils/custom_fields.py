from flask_restx import fields
"""
Module which contains custom field classes that are used for the creation of namespace models
"""

class NullableString(fields.String):
    """
    Class which inherits from fields.String and modifies the base class code
    to allow for null types as well as strings.
    """
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'

