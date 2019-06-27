# -*- coding: utf-8 -*-
"""
ELECOM製JT-U3912T ワイヤレスゲームパッド用コントローラクラス

`donkey createjs` でベースクラスを作成し、追記した。
"""
from donkeycar.parts.controller import Joystick, JoystickController


class ELECOM_JCU3912T(Joystick):
    """
    JC-T3912Tにおける/dev/input/js0 でのボタン/パッド/ジョイスティック
    各々のコードをマップ化したクラス。
    """
    #An interface to a physical joystick available at /dev/input/js0
    def __init__(self, *args, **kwargs):
        super(ELECOM_JCU3912T, self).__init__(*args, **kwargs)

            
        self.button_names = {
            0x130 : '1',
            0x131 : '2',
            0x132 : '3',
            0x133 : '4',
            0x134 : '5',
            0x135 : '6',
            0x136 : '7',
            0x137 : '8',
            0x138 : '9',
            0x139 : '10',
            0x13a : '11',
            0x13b : '12',
        }


        self.axis_names = {
            0x0 : 'analog_left_horizontal',
            0x1 : 'analog_left_vertical',
            0x2 : 'analog_right_vertical',
            0x5 : 'analog_right_horizontal',
            0x10 : 'dpad_horizontal',
            0x11 : 'dpad_vertical',
        }



class ELECOM_JCU3912TController(JoystickController):
    #A Controller object that maps inputs to actions
    def __init__(self, *args, **kwargs):
        super(ELECOM_JCU3912TController, self).__init__(*args, **kwargs)


    def init_js(self):
        #attempt to init joystick
        try:
            self.js = ELECOM_JCU3912T(self.dev_fn)
            self.js.init()
        except FileNotFoundError:
            print(self.dev_fn, "not found.")
            self.js = None
        return self.js is not None


    def init_trigger_maps(self):
        #init set of mapping from buttons to function calls
            
        self.button_down_trigger_map = {
            '12': self.toggle_mode,
            '11': self.toggle_manual_recording,

            '7': self.emergency_stop,
            '8': self.emergency_stop,

            '1': self.on_recording,
            '2': self.off_recording,

            '3': self.set_user_init,
            '4': self.set_local_init,

            '5': self.normal_stop,
            '6': self.normal_stop,
            '9': self.normal_stop,
            '10': self.normal_stop,
        }

        self.button_up_trigger_map = {

        }

        self.axis_trigger_map = {
            'analog_left_vertical': self.set_throttle,
            'analog_right_horizontal': self.set_steering,
            'dpad_horizontal': self.move_left_or_right,
            'dpad_vertical': self.move_front_or_rear,
        }

    def set_user_init(self):
        pass
    
    def set_local_init(self):
        pass
    
    def on_recording(self):
        pass

    def off_recording(self):
        pass

    def normal_stop(self):
        self.set_throttle(0)
        self.set_steering(0)

    def move_left_or_right(self, axis_val):
        
        if axis_val > 0:
            self.set_throttle(1)
            self.set_steering(1)
        elif axis_val < 0:
            self.set_throttle(1)
            self.set_steering(-1)
        else:
            self.set_throttle(0)
            self.set_steering(0)

    
    def move_front_or_rear(self, axis_val):
        self.set_steering(0)
        if axis_val > 0:
            self.set_throttle(1)
        elif axis_val < 0:
            self.set_throttle(-1)
        else:
            self.set_throttle(0)


def get_js_controller(cfg):

    try:
        return donkeycar.parts.controller.get_js_controller(cfg)
    except:
        if cfg.CONTROLLER_TYPE == "JCU3912T":
            cont_class = ELECOM_JCU3912TController
            ctr = cont_class(throttle_dir=cfg.JOYSTICK_THROTTLE_DIR,
                                throttle_scale=cfg.JOYSTICK_MAX_THROTTLE,
                                steering_scale=cfg.JOYSTICK_STEERING_SCALE,
                                auto_record_on_throttle=cfg.AUTO_RECORD_ON_THROTTLE)
            ctr.set_deadzone(cfg.JOYSTICK_DEADZONE)
            return ctr
        else:
            raise
    
    
    