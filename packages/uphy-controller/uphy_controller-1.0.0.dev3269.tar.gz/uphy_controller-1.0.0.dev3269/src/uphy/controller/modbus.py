import logging
from threading import Event
from time import sleep

import pymodbus.client
from pymodbus.client import ModbusBaseClient, ModbusTcpClient
import pymodbus.exceptions
from upgen.model.uphy import DataType, Signal
import struct

from . import Target, gui

datatype_to_modbus_type = {
    DataType.INT8: ModbusBaseClient.DATATYPE.INT16,
    DataType.INT16: ModbusBaseClient.DATATYPE.INT16,
    DataType.INT32: ModbusBaseClient.DATATYPE.INT32,
    DataType.UINT8: ModbusBaseClient.DATATYPE.UINT16,
    DataType.UINT16: ModbusBaseClient.DATATYPE.UINT16,
    DataType.UINT32: ModbusBaseClient.DATATYPE.UINT32,
    DataType.REAL32: ModbusBaseClient.DATATYPE.FLOAT32,
}


def get_type(datatype: DataType) -> tuple[ModbusBaseClient.DATATYPE, int]:
    data_type = datatype_to_modbus_type[datatype]
    data_type_bits = data_type.value[1] * 16
    return data_type, data_type_bits


def signal_to_regs_and_type(signal: Signal):
    data_type, data_bits = get_type(signal.datatype)
    data_regs = bits_to_regs(data_bits) * (signal.array_length or 1)
    return data_regs, data_type


def bits_to_regs(bits: int) -> None:
    return (bits + 15) // 16


def target_runner(stop: Event, target: Target, device_gui: gui.DeviceGUI):
    device_gui.update_status("CONNECTING")
    client = ModbusTcpClient(target.host, port=target.port)

    while not stop.is_set():
        try:
            client.connect()

            base = 0
            for slot in device_gui.slots.values():
                for input in slot.inputs.values():
                    count, data_type = signal_to_regs_and_type(input.signal)
                    index = base
                    base += count
                    try:
                        response = client.read_holding_registers(index, count=count)
                        if response.isError():
                            raise pymodbus.ModbusException("Error")
                    except pymodbus.exceptions.ConnectionException:
                        raise
                    except pymodbus.ModbusException as exception:
                        logging.error("Error on read %d - %r", index, exception)
                        input.update(None)
                        continue

                    values = [
                        client.convert_from_registers(
                            response.registers[ix : ix + data_type.value[1]], data_type
                        )
                        for ix in range(0, count, data_type.value[1])
                    ]
                    input.update(values)

                for output in slot.outputs.values():
                    count, data_type = signal_to_regs_and_type(output.signal)
                    index = base
                    base += count

                    if output.value is None:
                        continue

                    try:
                        payload = []
                        for value in output.value:
                            payload.extend(client.convert_to_registers(value, data_type))
                    except struct.error:
                        logging.error("Bad payload")
                        continue

                    try:
                        response = client.write_registers(index, payload)
                        if response.isError():
                            raise pymodbus.ModbusException("Error")
                    except pymodbus.exceptions.ConnectionException:
                        raise
                    except pymodbus.ModbusException as exception:
                        logging.error("Error on read %d - %r", index, exception)

                for param in slot.params.values():
                    count = bits_to_regs(param.signal.bitlen)
                    index = base
                    base += count
        except pymodbus.ModbusException as exception:
            device_gui.update_status("ERROR")
            logging.error("%r", exception)
            sleep(2)
        else:
            device_gui.update_status("CONNECTED")
            sleep(0.5)
