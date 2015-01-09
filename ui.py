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
            ('bigtext', 'white', 'black')]
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

