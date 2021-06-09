import vars.config as cfg
import vars.constants as c
from gui.Wrapper import Wrapper
from tracking.Tracking import auto_range

if __name__ == "__main__":
    
    cfg.wrapper = Wrapper()
    cfg.wrapper.launch()