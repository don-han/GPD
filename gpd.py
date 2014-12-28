#! /usr/bin/env python
import argparse
import sqlite3 as lite
import os, subprocess

### List Path ###
collectionPath = ".collection"


"""
nextActionPath = ".nextAction"
projectPath = ".project"
projectSupportPath = ".projectSupport"
referencePath = ".reference"
calendarPath = ".calendar"
incubationPath = ".incubation"
waitingPath = ".waiting"
trashPath = ".trash"
"""


def main():
    parser = argparse.ArgumentParser(description="Getting Pomodoros Done")
    subparsers = parser.add_subparsers(title="Steps")
    
    add_subparser = subparsers.add_parser('add',help="add").set_defaults(func=collect)
    collect_subparser = subparsers.add_parser('collect',help="collect").set_defaults(func=collect)
    process_subparsers = subparsers.add_parser('process',help="process").set_defaults(func=process)

    show_subparser = subparsers.add_parser('show',help="show")
    show_subparser2 = show_subparser.add_subparsers(dest="show_command")
    show_subparser2.add_parser("incubation").set_defaults(func=show)
    show_subparser2.add_parser("reference").set_defaults(func=show)
    show_subparser2.add_parser("projects").set_defaults(func=show)
    show_subparser2.add_parser("support").set_defaults(func=show)
    show_subparser2.add_parser("next").set_defaults(func=show)
    show_subparser2.add_parser("waiting").set_defaults(func=show)
    show_subparser2.add_parser("calendar").set_defaults(func=show)

    review_subparser = subparsers.add_parser('review',help="review").set_defaults(func=review)
    do_subparser = subparsers.add_parser('do',help="do").set_defaults(func=do)

    args = parser.parse_args()

    db_filename = "test.db"
    schema = """
    CREATE TABLE Goal (
        id      integer primary key autoincrement not null,
        details text,
        list    text
    )
    """
    db_is_new = not os.path.exists(db_filename)
    with lite.connect(db_filename) as con:
        if db_is_new:
            print("Creating schema")
            con.executescript(schema)
        args.func(con)
    
def collect(con):
    goal = input("What is the goal? ")
    con.execute("""
    INSERT INTO Goal(details, list) VALUES(?, 'collection')
    """, (goal,))

def process(con):
    cur = con.execute('SELECT * FROM Goal ORDER BY id DESC')
    for id, todo, list in cur.fetchall():
        if input('Is "{0}" actionable? (y,n)'.format(todo)) == 'n':
            choice = input("Is it trash, reference, or incubate?")
            print(todo)
            con.execute("""
            UPDATE Goal
            SET list = ?
            WHERE list = 'collection' AND id = ?
            """, (choice, id))
        else:
            ### TESTED UNTIL HERE
            nextAction = input("What is the next action?")
            if input("Do you have more next action?") == 'n':
                con.execute("""
                UPDATE Goal
                SET list = 'next action'
                WHERE list = 'collection' AND id = ?
                """, (id,))
            #else: 
                # The Project


            # Substitue with Tkinter? Knowpapa text-editor
            # subprocess.call(["xdg-open", filename])
            


def show(lst):
    print("The list is " + lst)


#    # TODO: Best way to store data?
#    try:
#        data = json.loads(open(collectionPath, 'r').read())
#    except FileNotFoundError as fe:
#        json.dump({'goal': goal},open(collectionPath, "w"))
#    finally:
#        f.close()
#
#
#    goal = Goal(goal)
#    collect.add(goal)
#
#
#    for goal in collectionBasket:
#        isActionable = input("Is " + goal.name +" actionable? (y/n)") == 'y':True?False
#        if !isActionable:
#            choose (trash, refernce, incubate)
#        nextActionList = NextActionList()
#        # Do you write all the next actions at process stage or do you just pass it onto project list
#        while True: 
#            print ("Write all necessary next actions and when you are finished, write "." to finish")
#            nextActionList.add(input("What is the immediate next action?"))
#        if input("Can the next action be completed in two minutes? y/n") == 'y':
#            #initiate pomodoro
#        else:
def organize():
    pass
#
def review():
    pass
def do():
    pass
#    
#    
#class Goal:
#    def __init__(self, goal):
#        self.goal = goal
#        
#    isActionable = False
#    isProject = False
#        
#class List:
#    def move(self, goal, to_list):
#class Pomodroo:
#    def __init__(self, time)
#
#
if __name__ == "__main__":
    main()
