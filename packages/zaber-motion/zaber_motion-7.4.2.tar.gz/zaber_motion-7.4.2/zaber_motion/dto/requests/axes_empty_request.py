# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import Any, Dict, List
import decimal
from collections.abc import Iterable
import zaber_bson


@dataclass
class AxesEmptyRequest:

    interfaces: List[int] = field(default_factory=list)

    devices: List[int] = field(default_factory=list)

    axes: List[int] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'AxesEmptyRequest':
        return AxesEmptyRequest(
            interfaces=[],
            devices=[],
            axes=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'AxesEmptyRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return AxesEmptyRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaces': [int(item) for item in self.interfaces] if self.interfaces is not None else [],
            'devices': [int(item) for item in self.devices] if self.devices is not None else [],
            'axes': [int(item) for item in self.axes] if self.axes is not None else [],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AxesEmptyRequest':
        return AxesEmptyRequest(
            interfaces=data.get('interfaces'),  # type: ignore
            devices=data.get('devices'),  # type: ignore
            axes=data.get('axes'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.interfaces is not None:
            if not isinstance(self.interfaces, Iterable):
                raise ValueError('Property "Interfaces" of "AxesEmptyRequest" is not iterable.')

            for i, interfaces_item in enumerate(self.interfaces):
                if interfaces_item is None:
                    raise ValueError(f'Item {i} in property "Interfaces" of "AxesEmptyRequest" is None.')

                if not isinstance(interfaces_item, (int, float, decimal.Decimal)):
                    raise ValueError(f'Item {i} in property "Interfaces" of "AxesEmptyRequest" is not a number.')

                if int(interfaces_item) != interfaces_item:
                    raise ValueError(f'Item {i} in property "Interfaces" of "AxesEmptyRequest" is not integer value.')

        if self.devices is not None:
            if not isinstance(self.devices, Iterable):
                raise ValueError('Property "Devices" of "AxesEmptyRequest" is not iterable.')

            for i, devices_item in enumerate(self.devices):
                if devices_item is None:
                    raise ValueError(f'Item {i} in property "Devices" of "AxesEmptyRequest" is None.')

                if not isinstance(devices_item, (int, float, decimal.Decimal)):
                    raise ValueError(f'Item {i} in property "Devices" of "AxesEmptyRequest" is not a number.')

                if int(devices_item) != devices_item:
                    raise ValueError(f'Item {i} in property "Devices" of "AxesEmptyRequest" is not integer value.')

        if self.axes is not None:
            if not isinstance(self.axes, Iterable):
                raise ValueError('Property "Axes" of "AxesEmptyRequest" is not iterable.')

            for i, axes_item in enumerate(self.axes):
                if axes_item is None:
                    raise ValueError(f'Item {i} in property "Axes" of "AxesEmptyRequest" is None.')

                if not isinstance(axes_item, (int, float, decimal.Decimal)):
                    raise ValueError(f'Item {i} in property "Axes" of "AxesEmptyRequest" is not a number.')

                if int(axes_item) != axes_item:
                    raise ValueError(f'Item {i} in property "Axes" of "AxesEmptyRequest" is not integer value.')
