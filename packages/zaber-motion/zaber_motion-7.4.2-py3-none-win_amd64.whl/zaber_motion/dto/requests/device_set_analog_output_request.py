# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass
from typing import Any, Dict
import decimal
import zaber_bson


@dataclass
class DeviceSetAnalogOutputRequest:

    interface_id: int = 0

    device: int = 0

    channel_number: int = 0

    value: float = 0

    @staticmethod
    def zero_values() -> 'DeviceSetAnalogOutputRequest':
        return DeviceSetAnalogOutputRequest(
            interface_id=0,
            device=0,
            channel_number=0,
            value=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceSetAnalogOutputRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceSetAnalogOutputRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': int(self.interface_id),
            'device': int(self.device),
            'channelNumber': int(self.channel_number),
            'value': float(self.value),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceSetAnalogOutputRequest':
        return DeviceSetAnalogOutputRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            channel_number=data.get('channelNumber'),  # type: ignore
            value=data.get('value'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.interface_id is None:
            raise ValueError(f'Property "InterfaceId" of "DeviceSetAnalogOutputRequest" is None.')

        if not isinstance(self.interface_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "InterfaceId" of "DeviceSetAnalogOutputRequest" is not a number.')

        if int(self.interface_id) != self.interface_id:
            raise ValueError(f'Property "InterfaceId" of "DeviceSetAnalogOutputRequest" is not integer value.')

        if self.device is None:
            raise ValueError(f'Property "Device" of "DeviceSetAnalogOutputRequest" is None.')

        if not isinstance(self.device, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Device" of "DeviceSetAnalogOutputRequest" is not a number.')

        if int(self.device) != self.device:
            raise ValueError(f'Property "Device" of "DeviceSetAnalogOutputRequest" is not integer value.')

        if self.channel_number is None:
            raise ValueError(f'Property "ChannelNumber" of "DeviceSetAnalogOutputRequest" is None.')

        if not isinstance(self.channel_number, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "ChannelNumber" of "DeviceSetAnalogOutputRequest" is not a number.')

        if int(self.channel_number) != self.channel_number:
            raise ValueError(f'Property "ChannelNumber" of "DeviceSetAnalogOutputRequest" is not integer value.')

        if self.value is None:
            raise ValueError(f'Property "Value" of "DeviceSetAnalogOutputRequest" is None.')

        if not isinstance(self.value, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Value" of "DeviceSetAnalogOutputRequest" is not a number.')
