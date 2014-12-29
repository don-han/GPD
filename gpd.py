#! /usr/bin/env python
import argparse
import sqlite3 as lite
import os, subprocess

### List Path ###

def main():
    parser = argparse.ArgumentParser(description="Getting Pomodoros Done")
    subparsers = parser.add_subparsers(title="Steps")
    
    add_subparser = subparsers.add_parser('add',help="add").set_defaults(func=collect)
    collect_subparser = subparsers.add_parser('collect',help="collect").set_defaults(func=collect)
    process_subparsers = subparsers.add_parser('process',help="process").set_defaults(func=process)
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
    do_subparser = subparsers.add_parser('do',help="do").set_defaults(func=do)
    """
    args = parser.parse_args()

    db_filename = "test.db"
    schema_task = """
    CREATE TABLE Task (
        id      integer primary key autoincrement,
        details text,
        bucket  text
    )
    """
    schema_next="""
    CREATE TABLE Next(
        id integer,
        details text,
        project text
    )
    """ 
    db_is_new = not os.path.exists(db_filename) 
    with lite.connect(db_filename) as con:
        if db_is_new:
            print("Creating schema")
            con.executescript(schema_task)
            con.executescript(schema_next)
        args.func(con)
    
def collect(con):
    task = input("What is the goal? ")
    con.execute("""
    INSERT INTO Task(details, bucket) VALUES(?, 'collection')
    """, (task,))

def process(con):
    cur = con.execute("SELECT * FROM Task WHERE bucket = 'collection' ORDER BY id DESC")
    for pid, task, bucket in cur.fetchall():
        print('### PROCESSING: "{0}" ###'.format(task))
        if input('Is "{0}" actionable? (y,n)'.format(task)) == 'n':
            choice = input("Is it trash, reference, or incubate?")
            # TODO: Make into integer only between 1 - 3 
            # (rf. Update multiple rows with different values and a single SQL query)
            con.execute("""
            UPDATE Task
            SET bucket = ?
            WHERE bucket = 'collection' AND id = ?
            """, (choice, pid,))
        else:
            if input("Is {0} the only next action?".format(task)) == 'y':
                if input("Can you finish it within 2 minutes? If so, do it now and enter 'y'. If not, press 'n'" =='n':
                    # make Task into next action
                    con.execute("""
                        INSERT INTO Next(details) VALUES(?)
                    """, (task,))

                # delete Task
                con.execute("""
                    DELETE FROM Task
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
                        for line in f:
                            con.execute("""
                                INSERT INTO NEXT(id, details, project) VALUES(?,?,?)
                            """, (na_id, line, task,))
                            na_id += 1
                        os.remove(tempFile)
                        con.execute("""
                        DELETE FROM Task
                        WHERE id = ?
                        """, (pid,))

if __name__ == "__main__":
    main()
