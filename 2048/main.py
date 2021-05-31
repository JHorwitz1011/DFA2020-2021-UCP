import vars.config as cfg
from gui.Wrapper import Wrapper

if __name__ == "__main__":
    cfg.wrapper = Wrapper()
    cfg.wrapper.launch()