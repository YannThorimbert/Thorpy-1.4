"""Graphical element of an application."""

from __future__ import division

from copy import copy

from pygame import Rect, SRCALPHA

from thorpy.painting.fusionner import _Fusionner
from thorpy.miscgui.title import Title
from thorpy.elements.ghost import Ghost
from thorpy.miscgui.state import State
from thorpy.miscgui._screened import _Screened
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui import constants, functions, parameters, style, painterstyle


class Element(_Screened, Ghost):
    """Fundamental graphical element of a program"""

    def __init__(self, text="", elements=None, normal_params=None):
        _Screened.__init__(self)
        Ghost.__init__(self, elements, normal_params)
        self._finished = False
        self.normal_params.polite_set("txt", text)
        self.visible = self.normal_params.params.get("visible", True)
##        self.click_quit = None
##        self._bar = None
##        self._bartarget = None #element of which self is the bar
##        self._lift = None
##        self._jail = None

    def finish(self):
        fusionner_attr = self.normal_params.get_fusionner()
        state_normal = State(fusionner_attr)
        self._states[constants.STATE_NORMAL] = state_normal
        self.current_state = self._states[constants.STATE_NORMAL]
        self._finished = True
##        self._finish_elements()

    def get_fus_rects(self, state=None):
        """Returns a list containing the fus rect of all self's elements."""
        rects = [self.get_fus_rect(state)]
        original_state = state
        if state is None:
            state = self.current_state_key
        state = original_state
        for e in self._blit_before:
            rects.extend(e.get_fus_rects(state))
        for e in self._blit_after:
            rects.extend(e.get_fus_rects(state))
        return rects

    def get_title(self):
        try:
            return self.current_state.fusionner.title
        except AttributeError:
            return str(self)

    def set_title(self, title, state=None):
        if state is None:
            for state in self._states:
                self.set_title(title, state)
        else:
            self._states[state].fusionner.title = title
            self._states[state].fusionner.refresh()

    def change_title(self, state=None, **kwargs):
        if state is None:
            for state in self._states:
                self.change_title(state, **kwargs)
        else:
            for arg in kwargs:
                setattr(self._states[state].fusionner.title, arg, kwargs[arg])
            self._states[state].fusionner.refresh()

    def set_writer(self, writer, state=None):
        title = self.get_title()
        title._writer = writer
        self.set_title(title, state)

    def get_text(self):
        title = self.get_title()
        if isinstance(title, str):
            return title
        else:
            text = title._text
            if text:
                return text
            else:
                return "no name : " + str(self) + constants.SYNTAX_BEG

    def build_state(self, key, painter=None, title=None, fusionner_class=None):
        """Add state"""
##        if not key in self._states:
        if fusionner_class is None:
            FusionnerClass = _Fusionner
        if title is None:
            title = Title("")
        if painter == -1:
            fusionner = FusionnerClass(title)
        else:
            fusionner = FusionnerClass(painter, title)
        state = State(fusionner)
        self._states[key] = state

    def set_font_color(self, color, state=None, center_title=True):
        """set font color for a given state"""
        if state is None:
            for state in self._states:
                self.set_font_color(color, state, center_title)
        else:
            self._states[state].fusionner.title._writer.set_color(color)
            self._states[state].fusionner.title.refresh_imgs()
            self._states[state].fusionner.refresh(center_title)

    def set_font_effects(self, biu, state=None, center=True, preserve=False):
        """biu = tuple : (bold, italic, underline)"""
        if state is None:
            for state in self._states:
                self.set_font_effects(biu, state, center, preserve)
        else:
            (bold, italic, underline) = biu
            self._states[state].fusionner.title._writer.set_effects(
                bold,
                italic,
                underline)
            self._states[state].fusionner.title.refresh_imgs()
            self._states[state].fusionner.refresh(center, preserve)
            self.scale_rects_to_fus()

    def set_font_size(self, size, state=None, center_title=True):
        """set font color"""
        if state is None:
            for state in self._states:
                self.set_font_size(size, state, center_title)
        else:
            self._states[state].fusionner.title._writer.set_size(size)
            self._states[state].fusionner.title.refresh_imgs()
            self._states[state].fusionner.refresh(center_title)
            self.scale_rects_to_fus()

    def replace_img_color(self, source, target, state=None, center=True,
                          preserve=False):
        """Replace colors from <source> to <target> for <state>.
        <preserve> = True means ???"""
        if state is None:
            for state in self._states:
                self.replace_img_color(source, target, state, center, preserve)
        else:
            self._states[state].fusionner.painter.change_color(source, target)
            self._states[state].fusionner.refresh(center, preserve)

    def set_text(self, text=None, state=None, center_title=True, size=None,
                cut=-1):
        """
        cut : - if cut is a string, this string will be used when needed to cut
            the word.
              - else if cut==-1 the line will be cut (default)
        """
        if state is None:
            for state in self._states:
                self.set_text(text, state, center_title, size, cut)
        else:
            if text is None:
                text = self._states[state].fusionner.title._text
            if cut:
                go_cut = True
                if isinstance(cut, str):
                    self._states[state].fusionner.title._cut_word = cut
                elif cut == -1:
                    go_cut = -1
            else:
                go_cut = False
            self._states[state].fusionner.title.set_text(text, size, go_cut)
            self._states[state].fusionner.refresh(center_title,
                                                  refresh_title=False)
            self._states[state].ghost_rect = self.get_fus_rect()
            self.redraw()

    def get_style(self):
        return self.normal_params.params.get("style")

    def set_style(self, new_style):
        self.normal_params.params["style"] = new_style

    def get_lines(self, state=None):
        if state is None:
            return {state: self._states[state].fusionner.title._lines for state\
                    in self.states}
        else:
            return self._states[state].fusionner.title._lines

    def redraw(self, state=None, painter=None, title=None, refresh_title=False):
        if state is None:
            for state in self._states:
                self.redraw(state, painter, title, refresh_title)
        else:
            if painter:
                try:
                    self._states[state].fusionner.painter = painter
                except AttributeError:
                    functions.debug_msg(
                        "Impossible to change Element's painter: " +
                        str(self) +
                        " in state: " +
                        str(state))
            if title:
                try:
                    self._states[state].fusionner.title = title
                    refresh_title = True
                except AttributeError:
                    functions.debug_msg(
                        "Impossible to change Element's title: " +
                        str(self) +
                        " in state: " +
                        str(state))
            self._states[state].fusionner.refresh(refresh_title=refresh_title)
            self._states[state].refresh_ghost_rect()

    def set_size(self, size, state=None, center_title=True, adapt_text=True,
                 cut=None, margins=style.MARGINS, refresh_title=False):
        """<margins> is used for text cutting only."""
        if state is None:
            for state in self._states:
                self.set_size(size, state, center_title, adapt_text, cut,
                              margins)
        else:
            try:
                if size[0] is None:
                    sizex = self._states[state].fusionner.painter.size[0]
                else:
                    sizex = size[0]
                if size[1] is None:
                    sizey = self._states[state].fusionner.painter.size[1]
                else:
                    sizey = size[1]
                size = (sizex, sizey)
                self._states[state].fusionner.painter.set_size(size)
                if adapt_text:
                    txt_size = (size[0] - 2 * margins[0],
                                size[1] - 2 * margins[1])
                    self.set_text(self._states[state].fusionner.title._text,
                                  state, center_title, txt_size, cut)
                    refresh_title = False
                self.redraw(state, refresh_title=refresh_title)
            except AttributeError:
                functions.debug_msg(
                    "Impossible to change Element's size: " +
                    str(self) +
                    "\n State: " +
                    str(state))
                if self._lift:
                    self.refresh_lift()

    #todo : move lift consequently
    def fit_children(self, w=1., h=1., state=constants.STATE_NORMAL,
                     only_children=False):
        """Scale to englobe children"""
        Ghost.englobe_childrens(self) #set the ghost rect
        fr = self.get_family_rect(state, only_children=only_children)
        width = fr.width
        height = fr.height
        if not w:
            width = self.get_fus_size()[0]
        elif w == "auto":
            width += 2
        else:
            width *= w
        if not h:
            height = self.get_fus_size()[1]
        elif h == "auto":
            height += 2
        else:
            height *= h
        self.set_size((width, height))
        if self._lift:
            self.refresh_lift()

    def click_quit_reaction(self, pygame_event):
        """Makes the element disappear if click is not colliding it."""
        self.click_quit = True
        (x, y) = pygame_event.pos
        if not self.collide((x, y), constants.STATE_NORMAL):
            functions.quit_menu_func()

    def set_main_color(self, color, state=None):
        if state is None:
            for state in self._states:
                self.set_main_color(color, state)
        else:
            try:
                self._states[state].fusionner.painter.set_color(color)
                self.redraw(state)
            except AttributeError:
                functions.debug_msg(
                    "Impossible to change Element's main color: ", self,
                    "\n State: " + str(state))

    def set_painter(self, painter, state=None, autopress=True):
        """Use before finish. If not, use set_active_painter instead."""
        self.normal_params.params["painter"] = painter
        if self._finished:
            self.change_painter(painter, state, autopress)
            functions.debug_msg("Attention, this element is not finished : " +
                                str(self) + ". Use set_active_painter instead")

    def change_painter(self, painter, state=None, autopress=True):
        if state is None:
            for state in self._states:
                self.change_painter(painter, state, autopress)
        else:
            painter = copy(painter)  # copy painter
            if autopress:  # _press if need to
                painter.pressed = True
            self._states[state].fusionner.painter = painter
            self._states[state].fusionner.refresh()

    def scale_to_title(self, margins=None, state=None):
        """scale to content"""
        if state is None:
            for state in self._states:
                Element.scale_to_title(self, margins, state)
        else:
            self._states[state].fusionner.scale_to_title(margins, True, False)
            self._states[state].refresh_ghost_rect()

    def scale_rects_to_fus(self, ghost=True, storer=True, state=None):
        if state is None:
            for state in self._states:
                self.scale_rects_to_fus(ghost, storer, state)
        else:
            self._states[state].refresh_ghost_rect()

    def get_image(self, state=constants.STATE_NORMAL):
        return self._states[state].fusionner.img

    def set_image(self, img, state=constants.STATE_NORMAL):
        self._states[state].fusionner.img = img

    def _change_animation_frame(self, event, imgs, interval, state):
        self._tot_ticks += event.tick
        if self._tot_ticks >= interval:
            state = self.current_state_key if state is None else state
            self._current_frame += 1
            self._current_frame %= len(imgs)
            self.unblit()
            self.set_image(imgs[self._current_frame], state)
            self.blit()
            self.update()
            self._tot_ticks = 0

    def set_animated(self, pps, imgs, state=None):
        """
        <pps>: Number of periods per seconds. It means that regardless of the number
               of frames, the whole set of frame is refreshed <pps> times per
               second (of course, a high pps is limited by machine performances).
        <imgs>: List of frames (pygame surfaces).
        <state>: Element state for which the animation accounts.
                 None means element's current state.
        NOTE : self's fus_rect and state properties doesn't adapt to the images,
        so use images of the same size in order to prevent bugs.
        Next version will provide auto-inflatable animations.
        """
        n = len(imgs)
        #factor 1000 because the thick will be in millisec
        #factor 2 because Clock.get_time() returns time between two last iters.
        interval = 1000. / (pps*n)
        self._tot_ticks = 0
        self._current_frame = 0
        reac = Reaction(constants.THORPY_EVENT,
                        self._change_animation_frame,
                        {"name":constants.EVENT_TIME},
                        {"imgs":imgs, "interval":interval, "state":state},
                        "thorpy animation")
        self.add_reaction(reac)



# ******************* BLIT FUNCTIONS ********************


    def blit(self):
        """Recursive blit"""
        self._clip_screen()
        for e in self._blit_before:
            e.blit()
        if self.visible:
            self.solo_blit()
        for e in self._blit_after:
            e.blit()
        self._unclip_screen()


    def _blit_update_bar(self):
        if self._bar:
            self._bar.blit()
            self._bar.update()

    def _update_bar(self):
        if self._bar:
            self._bar.update()

    def _blit_debug2(self, pos=None, temps=2, bckgr=constants.YELLOW):
        """fill bckgr, blit(), flip screen and sleep"""
        import pygame
        import time
        if pos:
            self.set_topleft(pos)
        if bckgr:
            self.surface.fill(bckgr)
        self.blit()
        pygame.display.flip()
        time.sleep(temps)



    def solo_blit(self):
        """
        Most basic blit : blit the self.fusionner's image on self.surface, at
        position topleft of self.fusionner.
        """
        self.surface.blit(self.current_state.fusionner.img,
                          self.current_state.fusionner.rect.topleft)

    def solo_partial_blit(self, rect):
        """
        Blit the part of this element (and not its childrens) which is within
        <rect>.
        """
        if self.visible:
            self._clip_screen(rect)
            self.solo_blit()
            self._unclip_screen()

    def solo_unblit(self, rect=None):#not used in the library!
        """Partial blit of self's oldest ancester on self's fus rect area."""
        r = self.get_fus_rect()
        if rect is not None:
            r = r.clip(rect)
        self.unblit(rect=r)

    def unblit(self, rect=None): #v1
        """Unblit self and all its descendants."""
        dr = [e.get_fus_rect() for e in self.get_descendants()]
        zone = self.get_fus_rect().unionall(dr)
        if rect is not None:
            zone.clip(rect)
        a = self.get_oldest_ancester()
        a.partial_blit(exception=self, rect=zone)

    def update(self):
        """Recursive update"""
        if self.visible:
            self.solo_update() #see Ghost
        for e in self._elements:
            e.update()

    def total_unblit(self):
        """Equivalent to self.surface.partial_blit(self.get_fus_rect())"""
        ancester = self.get_oldest_ancester()
        if ancester:
            ancester.unblit()
            ancester.blit()

    def total_update(self):
        ancester = self.get_oldest_ancester()
        ancester.update()

# ************** END BLIT FUNCTIONS **************

    def get_fus_rect(self, state=None):
        """get rect"""
        if not state:
            state = self.current_state_key
        return self._states[state].fusionner.rect.copy()

    def get_fus_topleft(self, state=None):
        """get topleft"""
        if not state:
            state = self.current_state_key
        return self._states[state].fusionner.rect.topleft

    def get_fus_size(self, state=None):
        """get size"""
        if not state:
            state = self.current_state_key
        return self._states[state].fusionner.rect.size

    def get_fus_center(self, state=None):
        """get center"""
        if not state:
            state = self.current_state_key
        return self._states[state].fusionner.rect.center

    def get_clip(self):
        """Try to return the clip rect of the painter of this element. If not
        possible, simply returns the rect corresponding to the image.
        """
        try:
            pos = self.get_fus_topleft(self.current_state_key)
            return self.current_state.fusionner.painter.clip.move(pos)
        except AttributeError:
            return self.get_fus_rect()

    def _clip_screen(self, rect=None):
        """
        Clip the screen to <rect>. If not rect, rect is set to self's fus rect.
        If this element has a _jail, <rect> will be the overlapping between
        <rect> and self.jail.
        """
        self._add_old_clip()
        if rect is None:
            rect = self.get_fus_rect()
        if self._jail:
            if self._overframe:
                rect = self.get_jail_rect()
            else:
                rect = self.get_jail_rect().clip(rect)
        self.surface.set_clip(rect)
        return rect

    def get_jail_rect(self):
        """Returns the rect of self's jail. Returns None if self doesn't have
        jail.
        """
        if self._jail:
            r1 = self._jail.get_clip()
            r2 = self._jail.get_jail_rect()
            if r2:
                return r1.clip(r2)
            else:
                return r1
        return None

    def _debug_clip(self):
        functions.debug_msg(
            self.surface.get_clip().contains(
                self.get_fus_rect()))

    def scroll_children(self, exceptions=None, shift=parameters.CHILDREN_SHIFT):
        """Typically used when lift dragged. Uses blit and update.
        <shift> is the 2D shift in pixels.
        """
        self.unblit()
        if not exceptions:
            exceptions = []
        for e in self._elements:
            if not (e in exceptions) and not(e == self._bar):
                e.move(shift)
        self.blit()
        self.update()

    def set_jailed(self, jail):
        if not self._lock_jail:
            self._jail = jail

    def set_prison(self):
        """Modify the descendants of self in such a way that they cannot be
        displayed outside self.get_clip().
        Caution: this overrides the previous prisons of the concerned
        elements!
        """
        self.update = self.solo_update
        for e in self.get_descendants():
            if not e == self._bar:
                e.set_jailed(self)

    def has_transparent(self):
        """Returns False if this element is not transparent.
        Note that the children of this element may be transparent.
        """
        return self.current_state.fusionner.img.get_flags() & SRCALPHA

    def get_family_rect(self, state=None, only_children=False):
        if not state:
            state = self.current_state_key
        gfr = Ghost.get_family_rect(self, state)
        if only_children:
            return gfr
        elif self.visible:
            if self._finished:
                r = self.get_fus_rect(state)
            else:
                r = self.get_ghost_rect(state)
            return r.union(gfr)

    def is_family_bigger(self, state=None):
        if not state:
            state = self.current_state_key
        fr = Ghost.get_family_rect(self, state)
        r = self.get_fus_rect(state)
        sl = r.left
        st = r.top
        sw = r.width
        sh = r.height
        return (((fr.x < sl) or (fr.w > sw)), ((fr.y < st) or (fr.h > sh)))

    def add_lift(self, axis="vertical", typ="normal"):
        if typ == "normal":
            from thorpy.elements.lift import LiftY
            lift_typ = LiftY
        elif typ == "dv":
            from thorpy.elements.lift import LiftDirViewerY
            lift_typ = LiftDirViewerY
        if axis == "vertical":
            lift = lift_typ(self)  # lift is already finished
            self.add_elements([lift])
            self._lift = lift  # to access easily to the lift
        else:
            functions.debug_msg("Only vertical lift is available.")
##        self._lift.active_wheel = True
##        rect = self.get_fus_rect()
##        rect.right = self._lift.get_fus_rect().left
##        self.set_clip(tuple(rect))

    def refresh_lift(self):
        """Refresh current lift. Removes lift if not needed. Add lift if needed.
        """
        if self._lift:
            functions.remove_element(self._lift)
        if self.get_family_rect().height > self.get_fus_rect().height:
            self.add_lift()
        functions.refresh_current_menu()

    def stick_to(self, target, target_side, self_side, align=True):
        """Sides must be either 'top', 'bottom, 'left' or 'right'.
        This function moves self in order to make its <self_side> just next to
        target's <target_side>.

        Note that unless <align> = True, this does not move self along the
        orthogonal axis: e.g, stick_to(target_element, 'right', 'left') will
        move self such that self.left = target.right (using storers rects), but
        self.top might not be target.top. Then this is up to the user to move
        self on the vertical axis once self is sticked to target.
        """
        r = self.get_storer_rect()
        topleft = r.topleft
        size = r.size
        if target == "screen":
            W, H = functions.get_screen_size()
            t = Rect(0, 0, W, H)
        else:
            t = target.get_storer_rect()
        target_topleft = t.topleft
        target_size = t.size
        if target_side == "left":
            sx = topleft[0]
            tx = target_topleft[0]
            if self_side == "right":
                sx += size[0]
            self.move((tx - sx, 0))
        elif target_side == "right":
            sx = topleft[0]
            tx = target_topleft[0] + target_size[0]
            if self_side == "right":
                sx += size[0]
            self.move((tx - sx, 0))
        elif target_side == "left":
            sx = topleft[0]
            tx = target_topleft[0]
            if self_side == "right":
                sx += size[0]
            self.move((tx - sx, 0))
        elif target_side == "bottom":
            sy = topleft[1]
            ty = target_topleft[1] + target_size[1]
            if self_side == "bottom":
                sy += size[1]
            self.move((0, ty - sy))
        elif target_side == "top":
            sy = topleft[1]
            ty = target_topleft[1]
            if self_side == "bottom":
                sy += size[1]
            self.move((0, ty - sy))
        else:
            return
        if align:
            if target_side == "top" or target_side == "bottom":
                self.set_center((t.centerx, None))
            else:
                self.set_center((None, t.centery))

    def set_bar_of(self, target, mode="horizontal"):
        self._bartarget = target
        if mode == "horizontal":
            sizex = target.get_fus_size()[0]
            sizey = self.get_fus_size()[1]
        self.set_size((sizex, sizey))
        if mode == "horizontal":
            self.stick_to(target, "top", "bottom")
            (target_left, target_top) = target.get_fus_topleft()
            self.set_topleft((target_left, None))
        self._bartarget._bar = self
        self._bartarget.add_elements([self])

    def add_bar(self, text="", size=None, painter=None):
        writer = painterstyle.WRITER(font_name=style.BAR_FONTS,
                                     color=style.FONT_BAR_COLOR,
                                     size=style.FONT_BAR_SIZE,
                                     italic=style.BAR_ITALIC,
                                     bold=style.BAR_BOLD,
                                     underline=style.BAR_UNDERLINE,
                                     aa=style.FONT_BAR_AA,
                                     bckgr_color=style.FONT_BAR_BCKGR)

        params = {"writer": writer}
        bar = Element(text=text, normal_params=params)
        if not painter:
            painter = functions.obtain_valid_painter(painterstyle.BAR_PAINTER,
                                                     color=style.BAR_COLOR)
        bar.set_painter(painter)
        bar.finish()
        if size:
            bar.set_size(size)
        bar.set_bar_of(self)

    def set_help_of(self, hoverable, wait_time=1000, pos=None):
        """NB : help needs a timed menu to work."""
        try:
            self.visible = False
            hoverable.add_elements([self])
            hoverable._help_element = self
            hoverable._help_wait_time = wait_time
            hoverable._help_pos = pos
            hoverable._help_reaction = Reaction(constants.THORPY_EVENT,
                                                hoverable._reaction_help,
                                                {"name":constants.EVENT_TIME},
                                                name=constants.REAC_HELP)
        except AttributeError:
            raise Exception("Cannot set helper of an element who does not have\
                                _reaction_help method.")