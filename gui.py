import urwid

def keyhandler(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    # Add
    if key in ('a', 'A'):
        txt = urwid.Text(u"Hello world")
        body = urwid.Filler(txt)
        fr = urwid.Frame(body)
        urwid.MainLoop(fr).run()

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)

if __name__ == "__main__":
    txt = urwid.Text(u"Enter 'a' to add a task", align='center')
    body = urwid.Filler(txt)
    fr = urwid.Frame(body)
    loop = urwid.MainLoop(fr,unhandled_input=keyhandler)
    loop.run()
