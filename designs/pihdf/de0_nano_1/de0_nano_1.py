from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

import sys
import os
module_path = os.path.dirname(__file__)


import site
site.addsitedir(module_path + '/src/modules')

from src.de0_nano_1_beh import *
from src.de0_nano_1_rtl import *

class de0_nano_1(Convertible):
    '''|
    | The design class
    |________'''
    def __init__(self, IMPL={}):

        self.structural = True
        self.models = IMPL

        if isinstance(IMPL, dict):
            self.IMPL = IMPL["top"] if "top" in IMPL else IMPL
        else:
            self.IMPL = IMPL

        # call base class constructor
        Convertible.__init__(self)

        self.resets = lambda : [
            Reset(name="rst", active=1, val=1, async=True)
        ]

        self.clocks = lambda : [
            Clock(name="clk")
        ]

        self.interfaces = lambda fdump : [
            HSD(direction=self.IN, name="mode_1", data=1, filedump=fdump),
            HSD(direction=self.IN, name="mode_2", data=2, push=True, filedump=fdump),
            HSD(direction=self.OUT, name="LEDs", data=5, filedump=fdump),
            HSD(direction=self.OUT, name="LED_rdy_en", data=1, filedump=fdump),
            HSD(direction=self.OUT, name="LED_rdy_buff", data=1, filedump=fdump),
            HSD(direction=self.OUT, name="LED_rdy_out", data=1, filedump=fdump)
        ]

        self.parameters = []

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': de0_nano_1_beh,
            'rtl': de0_nano_1_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            mode_1_ready,mode_1_valid,mode_1_data,
            mode_2_ready,mode_2_valid,mode_2_data,
            LEDs_ready,LEDs_valid,LEDs_data,
            LED_rdy_en_ready,LED_rdy_en_valid,LED_rdy_en_data,
            LED_rdy_buff_ready,LED_rdy_buff_valid,LED_rdy_buff_data,
            LED_rdy_out_ready,LED_rdy_out_valid,LED_rdy_out_data):
        '''|
        | Provides flat interface to the top-level implementation. This
        | function is given to MyHDL.toVerilog() and MyHDL.toVHDL()
        |________'''
        x = locals()
        del x['self']
        return self.flat2struct(**x)


if __name__ == "__main__":

    import myhdl
    import pihdf

    pihdf.info("Using MyHDL version %s" % myhdl.__version__)
    pihdf.info("Using MyFramework version %s" % pihdf.__version__)

    dn = de0_nano_1(IMPL=1)
    dn.convert(hdl="verilog")
    dn.convert(hdl="vhdl")
    dn.clean()
