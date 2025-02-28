import math
from dataclasses import dataclass

import dearpygui.dearpygui as dpg
from upgen.model.uphy import DataType
from upgen.model.runtime import Root as RootModel, Device, Slot, Signal, Parameter

datatype_to_min_max = {
    DataType.INT8: (-(2**7), 2**7 - 1),
    DataType.INT16: (-(2**15), 2**15 - 1),
    DataType.INT32: (-(2**31), 2**31 - 1),
    DataType.UINT8: (0, 2**8 - 1),
    DataType.UINT16: (0, 2**16 - 1),
    DataType.UINT32: (0, 2**31 - 1), # Incorrect max but larger values do not work with dpg
    DataType.REAL32: (-math.inf, math.inf),
}


@dataclass
class InputGUI:
    signal: Signal
    value_id: list[str | int]

    def __init__(self, signal: Signal):
        self.signal = signal
        dpg.add_text(signal.name)
        with dpg.group():
            self.value_id = [
                dpg.add_text("N/A") for _ in range(signal.array_length or 1)
            ]

    def update(self, value: list[int | float] | None):
        if value is None:
            for ix in range(self.signal.array_length or 1):
                dpg.set_value(self.value_id[ix], "N/A")
        else:
            for ix in range(self.signal.array_length or 1):
                dpg.set_value(self.value_id[ix], value[ix])


@dataclass
class OutputGUI:
    signal: Signal
    value_id: list[str | int]
    value: list[int] | None = None

    def __init__(self, signal: Signal):
        self.signal = signal
        self.value = [0] * (signal.array_length or 1)
        dpg.add_text(signal.name)
        min, max = datatype_to_min_max[signal.datatype]
        widget = dpg.add_input_float if signal.datatype == DataType.REAL32 else dpg.add_input_int
        with dpg.group():
            self.value_id = [
                widget(
                    width=100,
                    callback=lambda sender, app_data, user_data: self.callback(
                        ix, app_data
                    ),
                    min_value=min,
                    max_value=max,
                    min_clamped=True,
                    max_clamped=True,
                )
                for ix in range(signal.array_length or 1)
            ]

    def callback(self, ix: int, value: int):
        self.value[ix] = value


class ParamGUI:
    def __init__(self, signal: Parameter):
        self.signal = signal


@dataclass
class SlotGUI:
    inputs: dict[str, InputGUI]
    outputs: dict[str, OutputGUI]
    params: dict[str, ParamGUI]


@dataclass
class DeviceGUI:
    widget: int | str
    slots: dict[str, SlotGUI]
    status_id: str | int

    def update_status(self, status: str):
        dpg.set_value(self.status_id, status)

    def close(self):
        dpg.delete_item(self.widget)


def add_device(model: RootModel, device: Device, suffix: str) -> DeviceGUI:
    width = 300
    windows = [
        window
        for window in dpg.get_windows()
        if dpg.get_item_user_data(window) == "device"
    ]
    for ix, window in enumerate(windows):
        dpg.set_item_pos(window, [ix * width, 0])
    ix = len(windows)

    with dpg.window(
        width=width,
        pos=[ix * width, 0],
        autosize=True,
        label=f"{device.name} - {suffix}",
        user_data="device"
    ) as window:
        with dpg.group(horizontal=True):
            dpg.add_text("Status")
            status_id = dpg.add_text()

        slot_guis = {}
        for slot in device.slots:
            with dpg.child_window(auto_resize_y=True):
                slot_gui = _add_slot(model, slot)
                slot_guis[slot.name] = slot_gui

    return DeviceGUI(window, slot_guis, status_id)


def _add_slot(model: RootModel, slot: Slot):
    dpg.add_text(f"{slot.name}")

    dpg.add_separator()

    with dpg.group(indent=10), dpg.table(label=slot.name, header_row=False):
        dpg.add_table_column()
        dpg.add_table_column()

        inputs: dict[str, InputGUI] = {}
        for signal in slot.inputs:
            with dpg.table_row():
                inputs[signal.name] = InputGUI(signal)

        outputs: dict[str, OutputGUI] = {}
        for signal in slot.outputs:
            with dpg.table_row():
                outputs[signal.name] = OutputGUI(signal)

        params: dict[str, ParamGUI] = {}
        for signal in slot.parameters:
            with dpg.table_row():
                params[signal.name] = ParamGUI(signal)

    return SlotGUI(inputs=inputs, outputs=outputs, params=params)


def setup():
    dpg.create_context()
    def on_key_q(s, a, u):
        if dpg.is_key_down(dpg.mvKey_LControl):
            dpg.stop_dearpygui()

    def on_key_esc(s, a, u):
        dpg.stop_dearpygui()

    with dpg.handler_registry():
        dpg.add_key_press_handler(key=dpg.mvKey_Q, callback=on_key_q)
        dpg.add_key_press_handler(key=dpg.mvKey_Escape, callback=on_key_esc)

    dpg.create_viewport(title="U-Phy Controller", width=800)
    dpg.setup_dearpygui()


def run():
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
