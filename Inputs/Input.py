class input():
    #Not quite sure what is fully needed here
    #         HEIRARCHY
    #             input  --------------------------------\
    #           /     \-----\                             \
    #      joystick         trackpad                        button
    #       (velocity)        (position)---\                (on/off)   ---------\
    #    /     /       \       /     \      \                /   |  \            \
    #  blobs   aruco    |     |      blobs  aruco         aruco  |    color       keyboard
    #             keyboard    mouse                           GPIO pin
    #            /     \
    #          asdf   arrows
    #

    """
    initializes an input
    """
    def __init__(self):
        pass
    
    """
    calibrates the input if necessary
    """
    def calibrate(self):
        pass

    """
    Boolean to ensure that sensor is working properly
    """
    def is_working(self):
        return True

    """
    prints the input type to the console. to be overridden
    """
    def __str__(self):
        return "generic input"


        

