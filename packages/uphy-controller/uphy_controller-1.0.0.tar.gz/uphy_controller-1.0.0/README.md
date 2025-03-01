# U-Phy Controller

This contain a python based U-Phy device controller that act as a fieldbus master/controller.

Supported fieldbuses:

- modbus

## Install

```sh
uv pip install uphy-controller
```

## Workflow

```sh
# Start up controller against an existing device
uphy-controller modbus --model [PATH_TO_MODEL] --target [UUID]:[HOST]:[PORT]
```


```sh
# Start up controller against discovered devices that expose their model via
# mdns.
uphy-controller mdns
```
