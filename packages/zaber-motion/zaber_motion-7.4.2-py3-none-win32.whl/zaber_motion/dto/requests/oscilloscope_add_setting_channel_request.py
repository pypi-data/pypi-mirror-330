# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass
from typing import Any, Dict
import decimal
import zaber_bson


@dataclass
class OscilloscopeAddSettingChannelRequest:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    setting: str = ""

    @staticmethod
    def zero_values() -> 'OscilloscopeAddSettingChannelRequest':
        return OscilloscopeAddSettingChannelRequest(
            interface_id=0,
            device=0,
            axis=0,
            setting="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'OscilloscopeAddSettingChannelRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return OscilloscopeAddSettingChannelRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': int(self.interface_id),
            'device': int(self.device),
            'axis': int(self.axis),
            'setting': str(self.setting or ''),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'OscilloscopeAddSettingChannelRequest':
        return OscilloscopeAddSettingChannelRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            setting=data.get('setting'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.interface_id is None:
            raise ValueError(f'Property "InterfaceId" of "OscilloscopeAddSettingChannelRequest" is None.')

        if not isinstance(self.interface_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "InterfaceId" of "OscilloscopeAddSettingChannelRequest" is not a number.')

        if int(self.interface_id) != self.interface_id:
            raise ValueError(f'Property "InterfaceId" of "OscilloscopeAddSettingChannelRequest" is not integer value.')

        if self.device is None:
            raise ValueError(f'Property "Device" of "OscilloscopeAddSettingChannelRequest" is None.')

        if not isinstance(self.device, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Device" of "OscilloscopeAddSettingChannelRequest" is not a number.')

        if int(self.device) != self.device:
            raise ValueError(f'Property "Device" of "OscilloscopeAddSettingChannelRequest" is not integer value.')

        if self.axis is None:
            raise ValueError(f'Property "Axis" of "OscilloscopeAddSettingChannelRequest" is None.')

        if not isinstance(self.axis, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Axis" of "OscilloscopeAddSettingChannelRequest" is not a number.')

        if int(self.axis) != self.axis:
            raise ValueError(f'Property "Axis" of "OscilloscopeAddSettingChannelRequest" is not integer value.')

        if self.setting is not None:
            if not isinstance(self.setting, str):
                raise ValueError(f'Property "Setting" of "OscilloscopeAddSettingChannelRequest" is not a string.')
