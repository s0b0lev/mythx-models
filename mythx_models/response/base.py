"""This module contains the base response domain model."""

import abc
import json
import logging

import jsonschema

from mythx_models.exceptions import ResponseValidationError

LOGGER = logging.getLogger(__name__)


class BaseResponse(abc.ABC):
    """An abstract object describing responses from the MythX API."""

    schema = None

    @classmethod
    def validate(cls, candidate):
        """Validate the object's data format.

        This is done using a schema contained at the class level. If no schema is given, it is
        assumed that the request does not contain any meaningful data (e.g. an empty logout
        response) and no validation is done.

        If the schema validation fails, a :code:`RequestValidationError` is raised.

        If this method is called on a concrete object that does not contain a schema,
        :code:`validate` will return right away and log a warning as this behaviour might not have
        been intended by a developer.

        :param candidate: The candidate dict to check the schema against
        :return: None
        """
        if cls.schema is None:
            LOGGER.warning("Cannot validate {} without a schema".format(cls.__name__))
            return
        try:
            jsonschema.validate(candidate, cls.schema)
        except jsonschema.ValidationError as e:
            raise ResponseValidationError(e)

    @classmethod
    def from_json(cls, json_str: str):
        """Deserialize a given JSON string to the given domain model.

        Internally, this method uses the :code:`from_dict` method.

        :param json_str: The JSON string to deserialize
        :return: The concrete deserialized domain model instance
        """
        parsed = json.loads(json_str)
        return cls.from_dict(parsed)

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, d: dict):
        """An abstract method to construct the given domain model from a Python dict instance.

        :param d: The dict instance to deserialize
        """
        pass

    def to_json(self):
        """Serialize the current domain model instance to a JSON string.

        Internally, this method uses the :code:`to_dict` method.

        :return: The serialized domain model JSON string
        """
        return json.dumps(self.to_dict())

    @abc.abstractmethod
    def to_dict(self):
        """An abstract method to serialize the current domain model instance to a Python dict.

        :return: A Python dict instance holding the serialized domain model data
        """
        pass