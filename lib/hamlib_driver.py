import Hamlib
from Hamlib import Rig
from schemas import RigMode, VFO

class HamlibRig:
    """
    High-level translation wrapper for Hamlib Rig API.
    Designed to provide a clean, Pythonic interface while
    exposing all common rig control capabilities Hamlib supports.
    """

    HAMLIB_MODE_MAP = {
        Hamlib.RIG_MODE_LSB: RigMode.LSB,
        Hamlib.RIG_MODE_USB: RigMode.USB,
        Hamlib.RIG_MODE_CW: RigMode.CW,
        Hamlib.RIG_MODE_CWR: RigMode.CWR,
        Hamlib.RIG_MODE_FM: RigMode.FM,
        Hamlib.RIG_MODE_AM: RigMode.AM,
        # Hamlib.RIG_MODE_DIG: RigMode.DIG,
        # Hamlib.RIG_MODE_PKT: RigMode.PKT,
        # Hamlib.RIG_MODE_RTTY: RigMode.RTTY,
        # Hamlib.RIG_MODE_RTTYR: RigMode.RTTYR,
        # Hamlib.RIG_MODE_SAM: RigMode.SAM,
        # Hamlib.RIG_MODE_DRM: RigMode.DRM,
    }

    HAMLIB_VFO_MAP = {
        Hamlib.RIG_VFO_CURR: VFO.curr,
        Hamlib.RIG_VFO_A:    VFO.vfoa,
        Hamlib.RIG_VFO_B:    VFO.vfob,
        Hamlib.RIG_VFO_MAIN: VFO.vfo_main,
        Hamlib.RIG_VFO_SUB:  VFO.vfo_sub,
    }

    def __init__(self, rig_model, rig_port=None, baud=None):
        Hamlib.rig_set_debug(Hamlib.RIG_DEBUG_NONE)

        self.rig = Hamlib.Rig(rig_model)

        # Configure serial parameters if given
        if rig_port:
            self.rig.set_conf("rig_pathname", rig_port)
        if baud:
            self.rig.set_conf("serial_speed", str(baud))

        self.rig.open()

    # ------------------------------------------------------------
    # Frequency + VFO
    # ------------------------------------------------------------

    def get_frequency(self, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.get_freq(vfo)

    def set_frequency(self, freq, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.set_freq(vfo, freq)

    def get_vfo(self):
        current_vfo = self.rig.get_vfo()
        return self.HAMLIB_VFO_MAP.get(current_vfo)


    def set_vfo(self, vfo):
        for key, val in self.HAMLIB_VFO_MAP.items():
            if val == vfo:
                new_vfo = key
                break
        return self.rig.set_vfo(new_vfo)

    # ------------------------------------------------------------
    # Mode + Filter width
    # ------------------------------------------------------------

    def get_mode(self, vfo=Hamlib.RIG_VFO_CURR):
        mode, width = self.rig.get_mode(vfo)
        return {
            "mode": self.HAMLIB_MODE_MAP.get(mode),
            "width": width
        }

    
    def set_mode(self, mode):
        for key, val in self.HAMLIB_MODE_MAP.items():
            if val == mode:
                new_mode = key
                break
        return self.rig.set_mode(new_mode)

    # ------------------------------------------------------------
    # Generic Level controls (RF power, squelch, IF shift, etc.)
    # ------------------------------------------------------------

    def get_level(self, level_flag, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.get_level(vfo, level_flag)

    def set_level(self, level_flag, value, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.set_level(vfo, level_flag, value)

    # ------------------------------------------------------------
    # Split operations
    # ------------------------------------------------------------

    def get_split(self, vfo=Hamlib.RIG_VFO_CURR):
        tx_mode, tx_width = self.rig.get_split_mode(vfo)
        tx_freq = self.rig.get_split_freq(vfo)
        tx_vfo = self.rig.get_split_vfo(vfo)

        return {
            "tx_freq": tx_freq,
            "mode": tx_mode,
            "width": tx_width,
            "tx_vfo": tx_vfo,
        }

    def set_split(self, tx_freq=None, tx_vfo=None, mode=None, width=None, vfo=Hamlib.RIG_VFO_CURR):
        """
        Set any subset of split parameters.
        Will call only the appropriate Hamlib functions.
        """
        if tx_freq is not None:
            self.rig.set_split_freq(vfo, tx_freq)

        if tx_vfo is not None:
            self.rig.set_split_vfo(vfo, tx_vfo)

        if mode is not None:
            # width must be provided when setting mode
            if width is None:
                raise ValueError("set_split requires width when setting mode.")
            self.rig.set_split_mode(vfo, mode, width)

    # ------------------------------------------------------------
    # RIT / XIT
    # ------------------------------------------------------------

    def get_rit(self, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.get_rit(vfo)

    def set_rit(self, offset, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.set_rit(vfo, offset)

    def get_xit(self, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.get_xit(vfo)

    def set_xit(self, offset, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.set_xit(vfo, offset)

    # ------------------------------------------------------------
    # Repeater: shift + offset
    # ------------------------------------------------------------

    def get_rptr(self, vfo=Hamlib.RIG_VFO_CURR):
        shift = self.rig.get_rptr_shift(vfo)
        offset = self.rig.get_rptr_offset(vfo)
        return {"shift": shift, "offset": offset}

    def set_rptr(self, offset=None, shift=None, vfo=Hamlib.RIG_VFO_CURR):
        if offset is not None:
            self.rig.set_rptr_offset(vfo, offset)
        if shift is not None:
            self.rig.set_rptr_shift(vfo, shift)

    # ------------------------------------------------------------
    # PTT
    # ------------------------------------------------------------

    def get_ptt(self, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.get_ptt(vfo)

    def set_ptt(self, ptt_state, vfo=Hamlib.RIG_VFO_CURR):
        return self.rig.set_ptt(vfo, ptt_state)

    # ------------------------------------------------------------
    # Power state
    # ------------------------------------------------------------

    def get_power_status(self):
        return self.rig.get_powerstat()

    def set_power_status(self, status):
        return self.rig.set_powerstat(status)

    # ------------------------------------------------------------
    # Configuration parameters
    # ------------------------------------------------------------

    def set_conf(self, name, value):
        """Set a rig backend configuration parameter."""
        return self.rig.set_conf(name, value)

    def get_conf_params(self):
        """
        Enumerate configuration parameters supported by this rig backend.
        Not all Hamlib builds expose confparam enumeration, so this may vary.
        """
        params = []
        try:
            cp = self.rig.confparams
            for p in cp:
                params.append(p["name"])
        except Exception:
            pass
        return params

    # ------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------

    def close(self):
        self.rig.close()
