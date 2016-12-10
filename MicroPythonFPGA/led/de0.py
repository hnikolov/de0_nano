from de0.de0mem_py import *
import led.hps_0 as hps_0

# TODO: HPS peripherals, e.g., led, button, GSensor, DMA transfers?
# TODO: GPIOs

class LEDs(object):
    def __init__(self, pa_de0):
        if 'LED_PIO' not in dir(hps_0):
            raise RuntimeError('Cannot find "LED_PIO" in hps_0')
        self.pa = pa_de0 + hps_0.LED_PIO.BASE

    def get(self):
        return read_uint32_from_pa(self.pa)

    def set(self, value):
        return write_uint32_to_pa(self.pa, value)

    def _getLed(self, idx):
        return bool( read_uint32_from_pa(self.pa) & (1 << idx) )

    def on(self, idx):
        mask = read_uint32_from_pa(self.pa) | (1 << idx)
        write_uint32_to_pa(self.pa, mask)

    def off(self, idx):
        mask = read_uint32_from_pa(self.pa) & (~(1 << idx))
        write_uint32_to_pa(self.pa, mask)

    def toggle(self, idx):
        if self._getLed(idx): self.off(idx)
        else:                 self.on(idx)


class Buttons(object):
    def __init__(self, pa_de0):
        if 'BUTTON_PIO' not in dir(hps_0):
            raise RuntimeError('Cannot find "BUTTON_PIO" in hps_0')
        self.pa = pa_de0 + hps_0.BUTTON_PIO.BASE

    def get(self):
        return read_uint32_from_pa(self.pa)

    def _getButton(self, idx):
        return bool( read_uint32_from_pa(self.pa) & (1 << idx) )


class DipSwitches(object):
    def __init__(self, pa_de0):
        if 'DIPSW_PIO' not in dir(hps_0):
            raise RuntimeError('Cannot find "DIPSW_PIO" in hps_0')
        self.pa = pa_de0 + hps_0.DIPSW_PIO.BASE

    def get(self):
        return read_uint32_from_pa(self.pa)

    def _getDipSwitch(self, idx):
        return bool( read_uint32_from_pa(self.pa) & (1 << idx ) )


class MyRegFile32b(object):
    def __init__(self, pa_de0):
        if 'ONCHIP_MEMORY2_0' not in dir(hps_0):
            raise RuntimeError('Cannot find "ONCHIP_MEMORY2_0" in hps_0')
        self.pa = pa_de0 + hps_0.ONCHIP_MEMORY2_0.BASE

    def write(self, offset, value):
        write_uint32_to_pa(self.pa + (offset * 4), value)

    def read(self, offset):
        return read_uint32_from_pa(self.pa + (offset * 4))


class de0(object):
    """ Convenience class to access FPGA resources from HPS
        Examples:
            -- LEDs 0 to 7 ------------
            de0.l0 = 0          -> Switch-Off LED 0 (or de0.l0 = False)
            de0.l0 = 1          -> Switch-On  LED 0 (or de0.l0 = True)
            x = de0.l7          -> Read the status of LED 7 and assign to x
            de0.leds = 0x5a     -> Assign all LEDs at once (OFF_ON_OFF_ON_ON_OFF_ON_OFF)
            L = de0.leds        -> Read the status of all LEDs, assign to L
            de0._leds.toggle(3) -> Toggle LED 3
            -- Buttons 0, 1 -----------
            y = de0.b0          -> Read the status of Button 0, assign to y
            b = de0.butons      -> Read the status of both buttons and assign to b
            -- Dip Switches 0 to 3 --
            z = de0.ds2         -> Read the status of dip switch 2 and assign to z
            s = de0.dipsw       -> Read the status of all dip switches, assign to s
            -- On-chip memory (BRAM) --
            de0.rf.write(1, 23) -> Write value 23 to address 1 of the onchip (static) memory
    """
    def __init__(self):
        self.pa_de0_lws  = 0xFF200000
        self.pa_de0_axi  = 0xC0000000

        self._leds    = LEDs(self.pa_de0_lws)
        self._buttons = Buttons(self.pa_de0_lws)
        self._dipsw   = DipSwitches(self.pa_de0_lws)
        self.rf       = MyRegFile32b(self.pa_de0_axi)  # 16K x 32b
        self.my_rf    = MyRegFile32b(self.pa_de0_axi + 0x40000) # 8 x 32b
        self.my_lw_rf = MyRegFile32b(self.pa_de0_lws + 0x50000) # 8 x 32b


    @property
    def leds(self):
        """LEDs 0 to 7"""
        return self._leds.get()

    @leds.setter
    def leds(self, value):
        self._leds.set( value )

    @property
    def l0(self):
        """LED 0"""
        return self._leds._getLed(0)

    @l0.setter
    def l0(self, value):
        if value == 0: self._leds.off(0)
        else:          self._leds.on(0)

    @property
    def l1(self):
        """LED 1"""
        return self._leds._getLed(1)

    @l1.setter
    def l1(self, value):
        if value == 0: self._leds.off(1)
        else:          self._leds.on(1)

    @property
    def l2(self):
        """LED 2"""
        return self._leds._getLed(2)

    @l2.setter
    def l2(self, value):
        if value == 0: self._leds.off(2)
        else:          self._leds.on(2)

    @property
    def l3(self):
        """LED 3"""
        return self._leds._getLed(3)

    @l3.setter
    def l3(self, value):
        if value == 0: self._leds.off(3)
        else:          self._leds.on(3)

    @property
    def l4(self):
        """LED 4"""
        return self._leds._getLed(4)

    @l4.setter
    def l4(self, value):
        if value == 0: self._leds.off(4)
        else:          self._leds.on(4)

    @property
    def l5(self):
        """LED 5"""
        return self._leds._getLed(5)

    @l5.setter
    def l5(self, value):
        if value == 0: self._leds.off(5)
        else:          self._leds.on(5)

    @property
    def l6(self):
        """LED 6"""
        return self._leds._getLed(6)

    @l6.setter
    def l6(self, value):
        if value == 0: self._leds.off(6)
        else:          self._leds.on(6)

    @property
    def l7(self):
        """LED 7"""
        return self._leds._getLed(7)

    @l7.setter
    def l7(self, value):
        if value == 0: self._leds.off(7)
        else:          self._leds.on(7)


# ------------------------------------------------------
    @property
    def buttons(self):
        """Buttons 0 and 1"""
        return self._buttons.get()

    @property
    def b0(self):
        """Button 0"""
        return self._buttons._getButton(0)

    @property
    def b1(self):
        """Button 1"""
        return self._buttons._getButton(1)

# -------------------------------------------------------
    @property
    def dipsw(self):
        """Dip Switches 0 to 3"""
        return self._dipsw.get()

    @property
    def ds0(self):
        """Dip Switch 0"""
        return self._dipsw._getDipSwitch(0)

    @property
    def ds1(self):
        """Dip Switch 1"""
        return self._dipsw._getDipSwitch(1)

    @property
    def ds2(self):
        """Dip Switch 2"""
        return self._dipsw._getDipSwitch(2)

    @property
    def ds3(self):
        """Dip Switch 3"""
        return self._dipsw._getDipSwitch(3)