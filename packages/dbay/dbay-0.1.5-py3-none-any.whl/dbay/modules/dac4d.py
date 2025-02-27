from dbay.http import Http
from dbay.addons.vsource import VsourceChange
from dbay.state import IModule, Core
from typing import Literal
from dbay.addons.vsource import IVsourceAddon
from typing import Union


class dac4D_spec(IModule):
    module_type: Literal["dac4D"] = "dac4D"
    core: Core
    vsource: IVsourceAddon


class dac4D:
    def __init__(self, data, http: Http):
        self.http = http
        self.data = dac4D_spec(**data)
        # print("Initializing dac4D with data:", data)
        # print("data: ", self.data)

    def __del__(self):
        print("Cleaning up dac4D instance.")

        # reverting to previous config
        for idx in range(4):
            change = VsourceChange(
                module_index=self.data.core.slot,
                index=idx,
                bias_voltage=self.data.vsource.channels[idx].bias_voltage,
                activated=self.data.vsource.channels[idx].activated,
                heading_text=self.data.vsource.channels[idx].heading_text,
                measuring=False,
            )

            self.http.put("dac4D/vsource/", data=change.model_dump())

    def voltage_set(
        self, index: int, voltage: float, activated: Union[bool, None] = None
    ):
        if activated is None:
            activated = self.data.vsource.channels[index].activated
        change = VsourceChange(
            module_index=self.data.core.slot,
            index=index,
            bias_voltage=voltage,
            activated=activated,
            heading_text=self.data.vsource.channels[index].heading_text,
            measuring=True,
        )

        self.http.put("dac4D/vsource/", data=change.model_dump())

    def __str__(self):
        """Return a pretty string representation of the dac4D module."""
        slot = self.data.core.slot
        active_channels = sum(1 for ch in self.data.vsource.channels if ch.activated)
        return f"dac4D (Slot {slot}): {active_channels}/4 channels active"

    # Add other methods corresponding to the endpoints defined in dac4D.py as needed.
