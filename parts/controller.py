# -*- coding: utf-8 -*-
"""
ELECOM製JT-U3912T ワイヤレスゲームパッド用コントローラクラス

`donkey createjs` でベースクラスを作成し、追記した。
"""
from donkeycar.parts.controller import Joystick, JoystickController, PS3JoystickController, PS4JoystickController

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
            # 右ボタン群：上
            '1': self.on_recording,
            '2': self.off_recording,

            # 右ボタン群：下
            '3': self.set_user_init,
            '4': self.set_local_init,

            # トリガ
            '5': self.normal_stop,
            '6': self.emergency_stop,

            # トリガ小
            '7': self.decrease_max_throttle,
            '8': self.increase_max_throttle,

            # アナログスティック押込   
            '9': self.normal_stop,
            '10': self.erase_last_N_records,

            # START相当
            '12': self.toggle_mode,
            # SELECT 相当
            '11': self.toggle_manual_recording,
        }

        self.button_up_trigger_map = {

        }

        self.axis_trigger_map = {
            'analog_left_vertical': self.set_throttle,
            'analog_right_horizontal': self.set_steering_analog,
            'dpad_horizontal': self.move_left_or_right,
            'dpad_vertical': self.move_front_or_rear,
        }

    def set_user_init(self):
        self.mode = 'user'
        print('force mode:', self.mode)
    
    def set_local_init(self):
        self.mode = 'local'
        print('force mode:', self.mode)
    
    def on_recording(self):
        if self.auto_record_on_throttle:
            print('auto record on throttle is enabled.')
        self.recording = True
        print('recording:', self.recording)

    def off_recording(self):
        if self.auto_record_on_throttle:
            print('auto record on throttle is enabled.')
        self.recording = False
        print('recording:', self.recording)

    def normal_stop(self):
        self.set_throttle(0)
        self.set_steering(0)

    def move_left_or_right(self, axis_val):
        
        if axis_val > 0:
            self.set_throttle(-1)
            self.set_steering(-1)
        elif axis_val < 0:
            self.set_throttle(-1)
            self.set_steering(1)
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

    def set_steering_analog(self, axis_val):
        return self.set_steering(axis_val * (-1))

class TwoWheelsPS3JoystickController(PS3JoystickController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_trigger_maps(self):
        '''
        init set of mapping from buttons to function calls
        '''

        self.button_down_trigger_map = {
            # 右ボタン群：上
            'square': self.on_recording,
            'triangle': self.off_recording,

            # 右ボタン群：下
            'cross': self.set_user_init,
            'circle': self.set_local_init,

            # トリガ
            'L2': self.normal_stop,
            'R2': self.emergency_stop,

            # トリガ小
            'L1': self.decrease_max_throttle,
            'R1': self.increase_max_throttle,

            # アナログスティック押込   
            'L3': self.normal_stop,
            'R3': self.erase_last_N_records,

            # START相当
            'start': self.toggle_mode,
            # SELECT 相当
            'select': self.toggle_manual_recording,

            # dpad
            'dpad_up': self.move_forward,
            'dpad_down': self.move_backward,
            'dpad_left': self.move_left,
            'dpad_right': self.move_right,

        }

        self.button_up_trigger_map = {
            # dpad up
            'dpad_up': self.normal_stop,
            'dpad_down': self.normal_stop,
            'dpad_left': self.normal_stop,
            'dpad_right': self.normal_stop,
        }

        self.axis_trigger_map = {
            'right_stick_horz' : self.set_steering,
            'left_stick_vert' : self.set_throttle,

            #'dpad_horizontal': self.move_left_or_right,
            #'dpad_vertical': self.move_front_or_rear,
        }

    def set_user_init(self):
        self.mode = 'user'
        print('force mode:', self.mode)
    
    def set_local_init(self):
        self.mode = 'local'
        print('force mode:', self.mode)
    
    def on_recording(self):
        if self.auto_record_on_throttle:
            print('auto record on throttle is enabled.')
        self.recording = True
        print('recording:', self.recording)

    def off_recording(self):
        if self.auto_record_on_throttle:
            print('auto record on throttle is enabled.')
        self.recording = False
        print('recording:', self.recording)

    def move_forward(self):
        self.set_throttle(1)
    
    def move_backward(self):
        self.set_throttle(-1)
    
    def move_left(self):
            self.set_throttle(-1)
            self.set_steering(1)

    def move_right(self):
            self.set_throttle(-1)
            self.set_steering(-1)

    def normal_stop(self):
        self.set_throttle(0)
        self.set_steering(0)

    def set_steering(self, axis_val):
        self.angle = self.steering_scale * axis_val * (-1.0)
        #print("angle", self.angle)

class TwoWheelsPS4JoystickController(PS4JoystickController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_trigger_maps(self):
        '''
        init set of mapping from buttons to function calls
        '''
        self.button_down_trigger_map = {
            # 右ボタン群：上
            'square': self.on_recording,
            'triangle': self.off_recording,

            # 右ボタン群：下
            'cross': self.set_user_init,
            'circle': self.set_local_init,

            # トリガ
            'L2': self.normal_stop,
            'R2': self.emergency_stop,

            # トリガ小
            'L1': self.decrease_max_throttle,
            'R1': self.increase_max_throttle,

            # アナログスティック押込   
            'L3': self.normal_stop,
            'R3': self.erase_last_N_records,

            # START相当
            'share': self.toggle_mode,
            # SELECT 相当
            'options': self.toggle_manual_recording,

        }

        self.button_up_trigger_map = {

        }

        self.axis_trigger_map = {
            'right_stick_horz' : self.set_steering,
            'right_stick_vert' : self.set_throttle,
            'left_stick_horz' : self.set_steering,
            'left_stick_vert' : self.set_throttle,

            'dpad_leftright': self.move_leftright,
            'dpad_updown': self.move_fwdbwd,
        }

    def set_user_init(self):
        self.mode = 'user'
        print('force mode:', self.mode)
    
    def set_local_init(self):
        self.mode = 'local'
        print('force mode:', self.mode)
    
    def on_recording(self):
        if self.auto_record_on_throttle:
            print('auto record on throttle is enabled.')
        self.recording = True
        print('recording:', self.recording)

    def off_recording(self):
        if self.auto_record_on_throttle:
            print('auto record on throttle is enabled.')
        self.recording = False
        print('recording:', self.recording)

    def move_fwdbwd(self, axis_val):
        self.set_steering(0)
        self.set_throttle(axis_val)
    
    def move_leftright(self, axis_val):
        if axis_val > 0:
            self.set_throttle(-1)
            self.set_steering(axis_val)
        elif axis_val < 0:
            self.set_throttle(-1)
            self.set_steering(axis_val)
        else:
            self.set_throttle(0)
            self.set_steering(0)

    def set_steering(self, axis_val):
        self.angle = self.steering_scale * axis_val * (-1.0)
        #print("angle", self.angle)

    def normal_stop(self):
        self.set_throttle(0)
        self.set_steering(0)


def get_js_controller(cfg):

    try:
        from donkeycar.parts.controller import get_js_controller as get_controller
        return get_controller(cfg)
    except:
        if cfg.CONTROLLER_TYPE == "JCU3912T":
            cont_class = ELECOM_JCU3912TController
            ctr = cont_class(throttle_dir=cfg.JOYSTICK_THROTTLE_DIR,
                                throttle_scale=cfg.JOYSTICK_MAX_THROTTLE,
                                steering_scale=cfg.JOYSTICK_STEERING_SCALE,
                                auto_record_on_throttle=cfg.AUTO_RECORD_ON_THROTTLE)
            ctr.set_deadzone(cfg.JOYSTICK_DEADZONE)
            return ctr
        elif cfg.CONTROLLER_TYPE == "JS3TwoWheels":
            cont_class = TwoWheelsPS3JoystickController
            ctr = cont_class(throttle_dir=cfg.JOYSTICK_THROTTLE_DIR,
                                throttle_scale=cfg.JOYSTICK_MAX_THROTTLE,
                                steering_scale=cfg.JOYSTICK_STEERING_SCALE,
                                auto_record_on_throttle=cfg.AUTO_RECORD_ON_THROTTLE)
            ctr.set_deadzone(cfg.JOYSTICK_DEADZONE)
            return ctr
        elif cfg.CONTROLLER_TYPE == "JS4TwoWheels":
            cont_class = TwoWheelsPS4JoystickController
            ctr = cont_class(throttle_dir=cfg.JOYSTICK_THROTTLE_DIR,
                                throttle_scale=cfg.JOYSTICK_MAX_THROTTLE,
                                steering_scale=cfg.JOYSTICK_STEERING_SCALE,
                                auto_record_on_throttle=cfg.AUTO_RECORD_ON_THROTTLE)
            ctr.set_deadzone(cfg.JOYSTICK_DEADZONE)
            return ctr
        else:
            raise
    
    
    