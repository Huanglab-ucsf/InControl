'''
APT motor controller for Thorlabs, to be integrated into the package InControl
Core functions adapted from https://github.com/mcleung/PyAPT/blob/master/PyAPT.py

Dan Xie
dan.xie@ucsf.edu
'''


import os
from ctypes import c_long, c_buffer, c_float, windll, pointer


class API():
    def __init__(self, HWtype = 31, SerialNum = 83854883, verbose = False):
        self.HWtype = HWtype
        self.connected = False
        dllname = "C:\Program Files\Thorlabs\APT\APT Server\APT.dll"
        if not os.path.exists(dllname):
            print("ERROR: DLL not found")

        else:
            print("DLL found!")
            self.verbose = verbose
            self.dstep = 0.001 # one micron stepsize
            self.bl_range = 0.020 # backlash correction range 
            self.aptdll = windll.LoadLibrary(dllname)
            self.aptdll.APTCleanUp()
            self.aptdll.EnableEventDlg(True)
            self.aptdll.APTInit()
            self.HWtype = c_long(HWtype)
            self.SerialNum = SerialNum
            self.init_hardware() # initialization


    def init_hardware(self):
        '''
        Initialises the motor.
        '''
        if self.verbose:
            print 'initializeHardwareDevice serial', self.SerialNum

        result = self.aptdll.InitHWDevice(self.SerialNum)
        if result == 0:
            self.connected = True
            if self.verbose:
                print 'initialization SUCESS'
            return True
        else:
            raise Exception('Connection Failed. Check Serial Number!')
            return False



    def go_home(self):
        '''
        Go home
        '''
        if self.verbose:
            print('Going home...')
        if not self.connected:
            raise Exception('Please connect first!')

        self.aptdll.MOT_MoveHome(self.SerialNum)
        return True




    def get_stageInfo(self):
        '''
        Get the stage information
        '''
        min_pos = c_float()
        max_pos = c_float()
        units = c_long()
        pitch = c_float()
        self.aptdll.MOT_GetStageAxisInfo(self.SerialNum, pointer(min_pos), pointer(max_pos), pointer(units), pointer(pitch))
        stageInfo = [min_pos.value, max_pos.value, units.value, pitch.value]
        return stageInfo


    def set_stageInfo(self, min_pos, max_pos):
        '''
        Set the stage information
        '''
        min_pos = c_float(min_pos)
        max_pos = c_fload(max_pos)
        units = c_long(1)
        pitch = c_float(self.config.get_pitch())
        self.aptdll.MOT_SetStageAxisInfo(self.SerialNum, min_pos, max_pos, units, pitch)
        return True


    def set_stepsize(self, dstep, test_ax = False):
        '''
        Set the moving stepsize
        '''
        self.dstep = dstep
        if test_ax:
            self.aptdll.MOT_SetJogStepSize(self.SerialNum, c_float(dstep))
        if self.verbose:
            print("step size reset to:", self.dstep)

    def get_pos(self):
        '''
        get current position.
        '''
        if self.verbose:
            print("get_pos probing...")
        if not self.connected:
            raise Exception('Device not connected! ')

        position = c_float()
        self.aptdll.MOT_GetPosition(self.SerialNum, pointer(position))
        if self.verbose:
            print("Current position:", position.value)
        return position.value

    def move_by(self, rpos):
        '''
        Move by rpos from current position.
        '''
        if self.verbose:
            print("Move by:", rpos, c_float(rpos))
        if not self.connected:
            raise Exception('Please connect first!')

        cr_pos = c_float(rpos)
        self.aptdll.MOT_MoveRelativeEx(self.SerialNum, cr_pos, True)
        if self.verbose:
            print("Moved successfully by", rpos)
        return True


    def move_to(self, apos):
        '''
        move the motor to the position pos.
        '''
        if self.verbose:
            print("Move to", apos, c_float(apos))
        if not self.connected:
            raise Exception('Please connect first!')

        ca_pos = c_float(apos)
        self.aptdll.MOT_MoveAbsoluteEx(self.SerialNum, ca_pos, True)
        if self.verbose:
            print("Moved successfully to", apos)
        return True


    def jog_up(self):
        '''
        just jog the stage up, assume the stage is connected.
        '''
        self.move_by(self.dstep)

    def jog_down(self):
        '''
        jog the stage dowm, assume the stage is connected.
        '''
        self.move_by(-self.dstep)
        return True

    def bl_correction(self, dest_pos):
        '''
        back lash correction, smarter than stepwise motion
        '''
        current_pos = self.get_pos()
        if dest_pos > current_pos:
            self.move_by(dest_pos-current_pos+self.bl_range)
            self.move_by(-self.bl_range)
        else:
            self.move_by(dest_pos-current_pos-self.bl_range)
            self.move_by(self.bl_range)
        if self.verbose:
            print("Backlash corrected!")



    def identify(self):
        '''
        I don't quite understand the purpose of this function, but I copied it here anyway.
        '''
        self.aptdll.MOT_Identify(self.SerialNum)
        return True

    def clean_up(self):
        self.aptdll.APTCleanUp()
        if self.verbose:
            print('APT cleaned up')
            self.connected = False


def main():
    API_test = API(verbose = True)
    if API_test.connected:
        # API_test.jog_up()
        API_test.move_by(0.50)
        print(API_test.get_stageInfo())
        API_test.clean_up()
    else:
        print("Initialization fails.")


if __name__ == "__main__":
    main()
