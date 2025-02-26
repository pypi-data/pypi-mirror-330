# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass
from typing import Any, Dict
import decimal
import zaber_bson


@dataclass
class CustomInterfaceWriteRequest:

    transport_id: int = 0

    message: str = ""

    @staticmethod
    def zero_values() -> 'CustomInterfaceWriteRequest':
        return CustomInterfaceWriteRequest(
            transport_id=0,
            message="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'CustomInterfaceWriteRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return CustomInterfaceWriteRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'transportId': int(self.transport_id),
            'message': str(self.message or ''),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CustomInterfaceWriteRequest':
        return CustomInterfaceWriteRequest(
            transport_id=data.get('transportId'),  # type: ignore
            message=data.get('message'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.transport_id is None:
            raise ValueError(f'Property "TransportId" of "CustomInterfaceWriteRequest" is None.')

        if not isinstance(self.transport_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "TransportId" of "CustomInterfaceWriteRequest" is not a number.')

        if int(self.transport_id) != self.transport_id:
            raise ValueError(f'Property "TransportId" of "CustomInterfaceWriteRequest" is not integer value.')

        if self.message is not None:
            if not isinstance(self.message, str):
                raise ValueError(f'Property "Message" of "CustomInterfaceWriteRequest" is not a string.')
