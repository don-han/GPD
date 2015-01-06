import urwid

palette = [ ('titlebar', 'black', 'white'),
            ]

def keyhandler(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    # Collect
    if key in ('a', 'A'):

        pass
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
        self.original_widget=urwid.Text(u'The task "{0}" is added to the Collection Bucket'.format(footer.edit_text))

if __name__ == "__main__":
    body_txt = urwid.Text(u"Enter 'a' to add a task", align='center')
    body = urwid.Filler(body_txt)
    footer= urwid.Edit(u"What task would you like to add?")
    header_txt = urwid.Text(u"list goes here")
    header = urwid.AttrMap(header_txt, 'titlebar')
    #footer = urwid.Edit(u"What task would you like to add? ")
    fr = urwid.Frame(header=header, body=body,footer=footer, focus_part='footer')
    loop = urwid.MainLoop(fr, palette, unhandled_input=keyhandler)
    loop.run()
