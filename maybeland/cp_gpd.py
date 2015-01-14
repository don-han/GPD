#! /usr/bin/env python
import argparse
import sqlite3 as lite
import os, subprocess

class GPD:
    def collect(con):
        task = input("What is the goal? ")
        con.execute("""
        INSERT INTO Collection(details) VALUES(?)
        """, (task,))

    def process(con):
        cur = con.execute("SELECT * FROM Collection ORDER BY id DESC")
        for pid, task, bucket in cur.fetchall():
            print('[*] PROCESSING: "{0}"'.format(task))
            if input('Is "{0}" actionable? (y,n)'.format(task)) in ('n'):
                choice = input("Is it trash, reference, or incubate?")
                # TODO: Make into integer only between 1 - 3 
                # (rf. Update multiple rows with different values and a single SQL query)
                con.execute("""
                UPDATE Collection
                SET bucket = ?
                WHERE id = ?
                """, (choice, pid,))
            else:
                if input("Is {0} the only next action?".format(task)) == 'y':
                    if input("Can you finish it within 2 minutes? If so, do it now and enter 'y'. If not, press 'n'") =='n':
                        # make Collection into next action
                        con.execute("""
                            INSERT INTO NextAction(details) VALUES(?)
                        """, (task,))

                    # delete Collection
                    con.execute("""
                        DELETE FROM Collection
                        WHERE id = ?
                    """, (pid,))
                else:
                    tempFile = ".temp"
                    with open(tempFile, 'w') as f:
                        ## TODO: find an alternative in case $EDITOR is not defined
                        # Substitue with Tkinter? Knowpapa text-editor
                        # cat > /dev/null (subprocess.Popen(['cat'], f)
                        subprocess.call(["vim", tempFile])
                        with open(tempFile, 'r') as f:
                            na_id = 1
                            project = input("What is the name of the project?")
                            for line in f:
                                con.execute("""
                                    INSERT INTO NextAction(id, details, project) VALUES(?,?,?)
                                """, (na_id, line, project))
                                na_id += 1
                        os.remove(tempFile)
                        con.execute("""
                        DELETE FROM Collection
                        WHERE id = ?
                        """, (pid,))
    def show(con):
        bucketDict = {"1": "Collection", "2": "NextAction", "3": "Project"}
        bucket = bucketDict[input("Which bucket do you wish to see? (1. {0}, 2. {1} 3. {2})".format(bucketDict["1"],bucketDict["2"],bucketDict["3"]))]

        cur = con.cursor()
        cur.execute("SELECT * FROM {0}".format(bucket))
        #if listToShow == "1":
        #    cur.execute("""
        #        SELECT * FROM Collection
        #    """)
        #elif listToShow == "2":
        #    cur.execute("""
        #        SELECT * FROM NextAction
        #    """)
        #elif listToShow == "3":
        #    cur.execute("""
        #        SELECT * FROM Project
        #    """)
        # TODO: Find a way to effectively show the data of schema
        for col in cur.description:
            print(col[0])
        for row in cur.fetchall():
            print(row)

    def do(con):
        # TODO: if you finish one next action, then reduce the id by one of entire project
        cur = con.cursor()
        cur.execute("SELECT * FROM NextAction")
        for line in cur.fetchall():
            print(line)
            #print("{0} {1} {2}".format(line))

        #todo = input("Which ones do you wish to do in next 25 minutes?")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Getting Pomodoros Done")
    subparsers = parser.add_subparsers(title="Steps")
    
    add_subparser = subparsers.add_parser('add',help="add").set_defaults(func=collect)
    collect_subparser = subparsers.add_parser('collect',help="collect").set_defaults(func=collect)
    process_subparsers = subparsers.add_parser('process',help="process").set_defaults(func=process)
    show_subparsers = subparsers.add_parser('show',help="show").set_defaults(func=show)
    do_subparser = subparsers.add_parser('do',help="do").set_defaults(func=do)
    """
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
    """
    args = parser.parse_args()
    
    # TODO: Get rid of bucket
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
            #print("DB is new? {0}".format(db_is_new))
    with lite.connect(db_filename) as con:
        if db_is_new:
            print("[*] Creating schema")
            con.executescript(schema_task)
            con.executescript(schema_next)
            #con.executescript(schema_proj)
        args.func(con)
