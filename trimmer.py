import gremlin
from vjoy.vjoy import AxisName

current_offset_x = 0
current_offset_y = 0

commanded_offset_x = 0
commanded_offset_y = 0

trim_was_pushed = False
trim_was_released = False

last_x = 0
last_y = 0

mode = gremlin.user_plugin.ModeVariable(
        "Mode",
        "The mode to use for this mapping"
)

axis_x = gremlin.user_plugin.PhysicalInputVariable(
        "Physical X Axis",
        "X axis of the physical device.",
        [gremlin.common.InputType.JoystickAxis]
)
axis_x_dec = axis_x.create_decorator(mode.value)

axis_y = gremlin.user_plugin.PhysicalInputVariable(
        "Physical Y Axis",
        "Y axis of the physical device.",
        [gremlin.common.InputType.JoystickAxis]
)
axis_y_dec = axis_y.create_decorator(mode.value)

trim_btn = gremlin.user_plugin.PhysicalInputVariable(
        "Physical Trim set button",
        "Set trim button of the physical device.",
        [gremlin.common.InputType.JoystickButton]
)
trim_btn_dec = trim_btn.create_decorator(mode.value)


untrim_btn = gremlin.user_plugin.PhysicalInputVariable(
        "Physical UnTrim button",
        "Reset trim button of the physical device.",
        [gremlin.common.InputType.JoystickButton]
)
untrim_btn_dec = untrim_btn.create_decorator(mode.value)

vjoy_x = gremlin.user_plugin.VirtualInputVariable(
        "Vjoy X Axis",
        "X axis of the target VJoy device.",
        [gremlin.common.InputType.JoystickAxis]
)

vjoy_y = gremlin.user_plugin.VirtualInputVariable(
        "Vjoy Y Axis",
        "Y axis of the target VJoy device.",
        [gremlin.common.InputType.JoystickAxis]
)

@axis_x_dec.axis(axis_x.input_id)
def pitch(event, vjoy):
    global current_offset_x, last_x
    if not trim_was_pushed:
        vjoy[vjoy_x.vjoy_id].axis(vjoy_x.input_id).value = event.value + current_offset_x
        last_x = vjoy[vjoy_x.vjoy_id].axis(vjoy_x.input_id).value
    else:
        vjoy[vjoy_x.vjoy_id].axis(vjoy_x.input_id).value = last_x

@axis_y_dec.axis(axis_y.input_id)
def roll(event, vjoy):
    global current_offset_y, last_y
    if not trim_was_pushed:
        vjoy[vjoy_y.vjoy_id].axis(vjoy_y.input_id).value  = event.value + current_offset_y
        last_y = vjoy[vjoy_y.vjoy_id].axis(vjoy_y.input_id).value
    else:
        vjoy[vjoy_y.vjoy_id].axis(vjoy_y.input_id).value = last_y

@trim_btn_dec.button(trim_btn.input_id)
def trim(event, joy):
    global current_offset_x, current_offset_y, commanded_offset_x, commanded_offset_y, trim_was_pushed, trim_was_released
    global axis_x, axis_y
    v_x = joy[axis_x.device_guid].axis(axis_x.input_id)
    v_y = joy[axis_y.device_guid].axis(axis_y.input_id)
    if event.is_pressed:
        if not trim_was_pushed:
            trim_was_pushed = True
            commanded_offset_x += v_x.value
            commanded_offset_y += v_y.value
            
    else:
        if not trim_was_released:
            trim_was_released = True
            trim_was_pushed = False
            current_offset_x = commanded_offset_x
            current_offset_y = commanded_offset_y
        else:
            trim_was_released = False

@untrim_btn_dec.button(untrim_btn.input_id)
def untrim(event, joy):
    global current_offset_x, current_offset_y, commanded_offset_x, commanded_offset_y, trim_was_pushed, trim_was_released
    if event.is_pressed:
        current_offset_x = 0
        current_offset_y = 0
        commanded_offset_x = 0
        commanded_offset_y = 0
