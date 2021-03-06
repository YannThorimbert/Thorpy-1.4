from __future__ import division

from thorpy.elements.element import Element
from thorpy.miscgui.constants import STATE_NORMAL


class OneLineText(Element):

    def __init__(self, text="", elements=None, normal_params=None):
        Element.__init__(self, text, elements, normal_params)

    def finish(self):
        self.set_style("text")
        Element.finish(self)


class MultilineText(Element):

    def __init__(self, text="", size=None, elements=None, normal_params=None):
        Element.__init__(self, text, elements, normal_params)
        self._size = size
        self.visible = False

    def finish(self):
        Element.finish(self)
        if not self._size:
            self._size = self.get_fus_rect()
        self.set_size(self._size)
        for line in self.get_lines(STATE_NORMAL):
            e = OneLineText(line)
            e.finish()
            e.set_writer(self.current_state.fusionner.title._writer)
            self.add_elements([e])
        self.format_txt()

    def build_elements(self):
        for e in self._elements:
            e.father = None
        self._elements = []
        self._blit_before = []
        self._blit_after = []
        self.set_size(self._size)
        for line in self.get_lines(STATE_NORMAL):
            e = OneLineText(line)
            e.finish()
            e.set_writer(self.current_state.fusionner.title._writer)
            self.add_elements([e])
        self.format_txt()

    def format_txt(self):
        title = self._states[STATE_NORMAL].fusionner.title
        (x, y) = title._pos
        r = title.get_rect()
        for i in self._elements:
            (w, h) = i.get_fus_size()
            if title._align is "left":
                x = title._pos[0]
            elif title._align is "center":
                x = (r.width - w) // 2
            elif title._align is "right":
                x = r.width - w
            i.set_topleft((x, y))
            y += title._space + h

    def set_font_color(self, color, state=None, center_title=True):
        """set font color for a given state"""
        Element.set_font_color(self, color, state, center_title)
        self.build_elements()

    # remettre bonne couleur, etc
    def set_font_size(self, size, state=None, center_title=True):
        """set font color for a given state"""
        Element.set_font_size(self, size, state, center_title)
        self.build_elements()

    def set_font_effects(self, biu, state=None, center=True, preserve=False):
        """biu = tuple : (bold, italic, underline)"""
        Element.set_font_effects(self, biu, state, center, preserve)
        self.build_elements()
