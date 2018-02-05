from bolt_tui.dummy_pane import dummy_pane
from math import floor

class tui(object):
    panes = []

    def __init__(self, width, height):
        pane_width = floor((width - 2)/2)
        self.pane_width = pane_width
        self.height = height

        self.panes.append(dummy_pane(focused=True))
        self.panes.append(dummy_pane(focused=False))

        self.selected = 0

    def cmd_up(self):
        self.panes[self.selected].cmd_up()

    def cmd_down(self):
        self.panes[self.selected].cmd_down()

    def cmd_tab(self):
        self.panes[self.selected].set_focus(False)
        self.selected = (self.selected + 1) % 2
        self.panes[self.selected].set_focus(True)

    def get_panes(self):
        left_pane = self.panes[0].get_pane()
        right_pane = self.panes[1].get_pane()
        width = self.pane_width

        buf = []

        for i in range(0, self.height):
            if i < len(left_pane):
                left = left_pane[i]
            else:
                left = ''

            if i < len(right_pane):
                right = right_pane[i]
            else:
                right = ''

            str = left.ljust(width) + ' | ' + right.ljust(width)

            buf.append(str)

        return buf
