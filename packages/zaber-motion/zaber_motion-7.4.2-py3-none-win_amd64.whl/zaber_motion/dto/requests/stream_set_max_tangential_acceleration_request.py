# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass
from typing import Any, Dict
import decimal
import zaber_bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class StreamSetMaxTangentialAccelerationRequest:

    interface_id: int = 0

    device: int = 0

    stream_id: int = 0

    pvt: bool = False

    max_tangential_acceleration: float = 0

    unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'StreamSetMaxTangentialAccelerationRequest':
        return StreamSetMaxTangentialAccelerationRequest(
            interface_id=0,
            device=0,
            stream_id=0,
            pvt=False,
            max_tangential_acceleration=0,
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamSetMaxTangentialAccelerationRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamSetMaxTangentialAccelerationRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': int(self.interface_id),
            'device': int(self.device),
            'streamId': int(self.stream_id),
            'pvt': bool(self.pvt),
            'maxTangentialAcceleration': float(self.max_tangential_acceleration),
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamSetMaxTangentialAccelerationRequest':
        return StreamSetMaxTangentialAccelerationRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            stream_id=data.get('streamId'),  # type: ignore
            pvt=data.get('pvt'),  # type: ignore
            max_tangential_acceleration=data.get('maxTangentialAcceleration'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.interface_id is None:
            raise ValueError(f'Property "InterfaceId" of "StreamSetMaxTangentialAccelerationRequest" is None.')

        if not isinstance(self.interface_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "InterfaceId" of "StreamSetMaxTangentialAccelerationRequest" is not a number.')

        if int(self.interface_id) != self.interface_id:
            raise ValueError(f'Property "InterfaceId" of "StreamSetMaxTangentialAccelerationRequest" is not integer value.')

        if self.device is None:
            raise ValueError(f'Property "Device" of "StreamSetMaxTangentialAccelerationRequest" is None.')

        if not isinstance(self.device, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Device" of "StreamSetMaxTangentialAccelerationRequest" is not a number.')

        if int(self.device) != self.device:
            raise ValueError(f'Property "Device" of "StreamSetMaxTangentialAccelerationRequest" is not integer value.')

        if self.stream_id is None:
            raise ValueError(f'Property "StreamId" of "StreamSetMaxTangentialAccelerationRequest" is None.')

        if not isinstance(self.stream_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "StreamId" of "StreamSetMaxTangentialAccelerationRequest" is not a number.')

        if int(self.stream_id) != self.stream_id:
            raise ValueError(f'Property "StreamId" of "StreamSetMaxTangentialAccelerationRequest" is not integer value.')

        if self.max_tangential_acceleration is None:
            raise ValueError(f'Property "MaxTangentialAcceleration" of "StreamSetMaxTangentialAccelerationRequest" is None.')

        if not isinstance(self.max_tangential_acceleration, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "MaxTangentialAcceleration" of "StreamSetMaxTangentialAccelerationRequest" is not a number.')

        if self.unit is None:
            raise ValueError(f'Property "Unit" of "StreamSetMaxTangentialAccelerationRequest" is None.')

        if not isinstance(self.unit, (Units, str)):
            raise ValueError(f'Property "Unit" of "StreamSetMaxTangentialAccelerationRequest" is not Units.')
