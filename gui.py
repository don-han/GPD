import urwid
# Set up color scheme
palette = [ ('titlebar', 'black', 'white') ]
def keyhandler(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    # Collect
    if key in ('a', 'A'):
        edit = urwid.Edit(u"What task would you like to add? ")
        edit = urwid.Filler(edit)
        q = QuestionBox(edit)
        layout.footer = q
        layout.focus_position = 'footer'
    # Process
    if key in ('p', 'P'):
        # make widget about processing (menu)
        # loop.widget = 
        pass

    # do
    if key in ('d', 'D'):
        bt = urwid.BigText("")
        bt = urwid.AttrWrap(bt, 'bigtext')
        
        loop.widget = bt
        # make big text widget
        # loop.widget=
        pass



class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        #layout.footer = urwid.Text(u'The Task "{0}" is added to the Collection Bucket'.format(footer.edit_text))
        #self.original_widget=urwid.Text(u'The task "{0}" is added to the Collection Bucket'.format(footer.edit_text))

if __name__ == "__main__":

    # Create the beginning screen
    header_txt = urwid.Text(u"list stat goes here")
    header = urwid.AttrMap(header_txt, 'titlebar')

    body_txt = urwid.Text(u"""
    Welcome to GPD!
    Enter 'a' to add a new task, 'q' to quit, 'h' for more help""", align='center')
    body = urwid.Filler(body_txt)

    # place holder for footer
    footer = urwid.Text(u"")

    layout = urwid.Frame(header=header, body=body, footer=footer)

    loop = urwid.MainLoop(layout,palette, unhandled_input=keyhandler)
    loop.run()

