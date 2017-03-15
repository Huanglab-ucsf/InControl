import os
from ctypes import c_long, c_buffer, c_float, windll, pointer
print os.getcwd()


class API():
    def __init__(self, HWtype = 31, SerialNum = 83854883, verbose = False):
        self.HWtype = HWtype
        self.connected = False
        dllname = os.path.join(os.path.dirname(__file__), 'APT.dll')
        if not os.path.exists(dllname):
            print("ERROR: DLL not found")

        else:
            self.aptdll = windll.LoadLibrary(dllname)
            self.aptdll.EnableEventDlg(True)
            self.aptdll.AptInit()



def main():
    API_test = API()

if __name__ == "__main__":
    main()

