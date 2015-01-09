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
        top = CascadingBoxes(menu_top)
        layout.body = top
        layout.focus_position = 'body'
        ## lst = get_list
        #tasks = []
        #for task in tasks:
            
        # make widget about processing (menu)
        # loop.widget = 
        pass

    # do
    if key in ('d', 'D'):
        """
        bt = urwid.BigText("")
        bt = urwid.AttrMap(bt, 'bigtext')
        
        loop.widget = bt
        # make big text widget
        # loop.widget=
        """
        pass



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


# Set up color scheme
palette = [ ('titlebar', 'black', 'white'),
            ('bigtext', 'white', 'black'),
            ('reversed', 'standout', '')]


# Create menu for Process Step
menu_top = menu(u'Processing...', [
    sub_menu(u'Not Actionable', [
        menu_button(u'Trash', item_chosen),
        menu_button(u'Incubate', item_chosen),
        menu_button(u'Reference', item_chosen),
    ]),
    sub_menu(u'Actionable', [
        sub_menu(u'Next Action', [
            menu_button(u'Less than 2 minutes', item_chosen),
            sub_menu(u'Longer than 2 minutes', [
                menu_button(u'Delegate it: Waiting for', item_chosen),
                menu_button(u'Defer it: NextActions ', item_chosen),
                menu_button(u'Defer it: Calendar', item_chosen),
                ]),
            ]),
    menu_button(u'Project', item_chosen),
    ]),
])

# Creating Cascading Menu
def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def sub_menu(caption, choices):
    contents = menu(caption, choices)
    def open_menu(button):
        return self.open_box(contents)
    return menu_button([caption, u'...'], open_menu)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button):
    response = urwid.Text([u'You chose ', button.label, u'\n'])
    done = menu_button(u'Ok', exit_program)
    self.open_box(urwid.Filler(urwid.Pile([response, done])))

class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 5

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u'/'))
        self.box_level = 0
        self.open_box(box)

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


if __name__ == "__main__":
    GUI()

