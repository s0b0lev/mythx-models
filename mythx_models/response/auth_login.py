import json
from typing import Dict

from mythx_models.response.base import BaseResponse
from mythx_models.util import resolve_schema


class AuthLoginResponse(BaseResponse):
    """The API response domain model for a login action."""

    with open(resolve_schema(__file__, "auth.json")) as sf:
        schema = json.load(sf)

    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_dict(cls, d: Dict):
        """Create the response domain model from a dict.

        This also validates the dict's schema and raises a :code:`ValidationError`
        if any required keys are missing or the data is malformed.

        :param d: The dict to deserialize from
        :return: The domain model with the data from :code:`d` filled in
        """
        cls.validate(d)
        return cls(
            access_token=d["jwtTokens"]["access"],
            refresh_token=d["jwtTokens"]["refresh"],
        )

    def to_dict(self):
        """Serialize the reponse model to a Python dict.

        :return: A dict holding the request model data
        """
        d = {"jwtTokens": {"access": self.access_token, "refresh": self.refresh_token}}
        self.validate(d)
        return d
