import urwid
import sqlite3 as lite
import os

class GPD:
    # Set up color scheme
    palette = [ ('titlebar', 'black', 'white'),
                ('bigtext', 'white', 'black'),
                ('reversed', 'standout', '')]

    def __init__(self):
        ### SET UP SQLITE3 ###
        schema_task = """
        CREATE TABLE Collection (
            id      integer primary key autoincrement,
            details text,
            bucket  text
        )
        """

        schema_next="""
        CREATE TABLE NextAction(
            id integer,
            step_id integer,
            details text,
            project text references Project(name)
        )
        """ 

        schema_proj="""
        CREATE TABLE Project(
            name text
        )
        """
        db_filename = "test.db"
        db_is_new = not os.path.exists(db_filename) 
        with lite.connect(db_filename) as self.con:
            if db_is_new:
                print("[*] Creating schema")
                self.con.executescript(schema_task)
                self.con.executescript(schema_next)
                self.con.executescript(schema_proj)
            self.build()
    def build(self):

        ### SET UP UI ###
        # Create initial screen
        self.header_txt = urwid.Text(u"list stat goes here")
        #header = urwid.AttrWrap(header_txt, 'titlebar')
        cur = self.con.cursor()
        cur.execute("SELECT * FROM NextAction")
        tasks = cur.fetchall()
        # TODO: Make this condition dynamic (applies each time something new is added)
        if tasks:
            body_txt = urwid.Text(u"{0}".format(tasks))
        else:
            body_txt = urwid.Text(u"""
            Welcome to GPD!
            Enter 'a' to add a new task, 'q' to quit, 'h' for more help""", align='center')
        self.body = urwid.Filler(body_txt)

        # place holder for footer
        self.footer = urwid.Text(u"")
        self.layout = urwid.Frame(header=self.header_txt, body=self.body, footer=self.footer)

    
    def main(self):
        self.loop = urwid.MainLoop(self.layout, self.palette, unhandled_input=self.keyhandler)
        self.loop.run()

    def keyhandler(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        # Collect
        if key in ('a', 'A'):
            self.layout.footer = AddPrompt(self.loop, self.con)
            self.layout.focus_position = 'footer'
        # Process
        if key in ('p', 'P'):
            # for task in tasks:
            self.layout.body = CascadingBoxes(self.loop, self.con)
            self.layout.focus_position = 'body'

        # do
        if key in ('d', 'D'):
            bt = urwid.BigText('1 : 0 0', urwid.font.HalfBlock7x7Font())
            bt = urwid.Padding(bt, 'center', width='clip')
            #bt = urwid.AttrWrap(bt, 'bigtext')
            bt = urwid.Filler(bt)
            self.layout.body = bt
            self.layout.focus_position = 'body'

class AddPrompt(urwid.Edit):
    def __init__(self, loop, con):
        self.loop = loop
        self.con = con
        urwid.Edit.__init__(self, 'What task would you like to add? ')

    def keypress(self, size, key):
        if key == 'enter':
            task = self.get_edit_text()
            self.loop.widget.footer = urwid.Text(u'The task "{0}" is added!'.format(task))
            self.con.execute("""
            INSERT INTO Collection(details) VALUES(?)
            """, (task,))
            self.con.commit()
        else:
            return urwid.Edit.keypress(self, size, key)

class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 5

    def __init__(self, loop, con):
        self.loop = loop
        self.con = con
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

    # TODO: Make a special function for each of the item, and attach it to the menu_button
    def item_chosen(self, button):
        response = urwid.Text([u'You chose ', button.label, u'\n'])
        done = self.menu_button(u'Ok',)
        self.open_box(urwid.Filler(urwid.Pile([response, done])))



if __name__ == "__main__":
    gpd = GPD()
    gpd.main()

