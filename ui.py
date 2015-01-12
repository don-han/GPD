import urwid

def keyhandler(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    # Collect
    if key in ('a', 'A'):
        layout.footer = AddPrompt()
        layout.focus_position = 'footer'
    # Process
    if key in ('p', 'P'):
        # for task in tasks:
        layout.body = CascadingBoxes()
        layout.focus_position = 'body'

    # do
    if key in ('d', 'D'):
        bt = urwid.BigText('1 : 0 0', urwid.font.HalfBlock7x7Font())
        bt = urwid.Padding(bt, 'center', width='clip')
        #bt = urwid.AttrWrap(bt, 'bigtext')
        bt = urwid.Filler(bt)
        layout.body = bt
        layout.focus_position = 'body'



class AddPrompt(urwid.Edit):
    def __init__(self):
        urwid.Edit.__init__(self, 'What task would you like to add? ')

    def get_prompt(self):
        return self.get_edit_text()

    def keypress(self, size, key):
        if key == 'enter':
            layout.footer = urwid.Text(u'The task "{0}" is added!'.format(self.get_edit_text()))
        else:
            return urwid.Edit.keypress(self, size, key)



class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 5

    def __init__(self):
        # Create menu for Process Step
        menu_top = self.menu(u'Processing...', [
            self.sub_menu(u'Not Actionable', [
                self.menu_button(u'Trash', self.item_chosen),
                self.menu_button(u'Incubate', self.item_chosen),
                self.menu_button(u'Reference', self.item_chosen),
            ]),
            self.sub_menu(u'Actionable', [
                self.sub_menu(u'Next Action', [
                    self.menu_button(u'Less than 2 minutes', self.item_chosen),
                    self.sub_menu(u'Longer than 2 minutes', [
                        self.menu_button(u'Delegate it: Waiting for', self.item_chosen),
                        self.menu_button(u'Defer it: NextActions ', self.item_chosen),
                        self.menu_button(u'Defer it: Calendar', self.item_chosen),
                        ]),
                    ]),
            self.menu_button(u'Project', self.item_chosen),
            ]),
        ])
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u'/'))
        self.box_level = 0
        self.open_box(menu_top)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

    # Creating Cascading Menu
    def menu_button(self, caption, callback):
        button = urwid.Button(caption)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, None, focus_map='reversed')

    def sub_menu(self, caption, choices):
        contents = self.menu(caption, choices)
        def open_menu(button):
            return self.open_box(contents)
        return self.menu_button([caption, u'...'], open_menu)

    def menu(self, title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        body.extend(choices)
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(self, button):
        response = urwid.Text([u'You chose ', button.label, u'\n'])
        done = self.menu_button(u'Ok', keyhandler)
        self.open_box(urwid.Filler(urwid.Pile([response, done])))



if __name__ == "__main__":
    # Set up color scheme
    palette = [ ('titlebar', 'black', 'white'),
                ('bigtext', 'white', 'black'),
                ('reversed', 'standout', '')]

    # Create the beginning screen
    header_txt = urwid.Text(u"list stat goes here")
    #header = urwid.AttrMap(header_txt, 'titlebar')

    body_txt = urwid.Text(u"""
    Welcome to GPD!
    Enter 'a' to add a new task, 'q' to quit, 'h' for more help""", align='center')
    body = urwid.Filler(body_txt)

    # place holder for footer
    footer = urwid.Text(u"")

    layout = urwid.Frame(header=header_txt, body=body, footer=footer)

    loop = urwid.MainLoop(layout,palette, unhandled_input=keyhandler)
    loop.run()
