#! /usr/bin/env python
import json
import argparse

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
    
    subparsers.add_parser('add',help="add")
    subparsers.add_parser('collect',help="collect")
    subparsers.add_parser('process',help="process")
    subparsers.add_parser('show',help="show").add_argument("lst")
    subparsers.add_parser('review',help="review")
    subparsers.add_parser('do',help="do")

    args = parser.parse_args()

    
#def collect(goal):
#    # TODO: Best way to store data?
#    try:
#        data = json.loads(open(collectionPath, 'r').read())
#    except FileNotFoundError as fe:
#        json.dump({'goal': goal},open(collectionPath, "w"))
#    finally:
#        f.close()
#
#
#    task = Task(goal)
#    collect.add(goal)
#
#
#def process():
#    for task in collectionBasket:
#        isActionable = input("Is " + task.name +" actionable? (y/n)") == 'y':True?False
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
#
#                
#            
#
#
#            
#
#
#
#
#def organize():
#
#def do():
#    
#    
#class Task:
#    def __init__(self, goal):
#        self.goal = goal
#        
#    isActionable = False
#    isProject = False
#        
#class List:
#    def move(self, task, to_list):
#class Pomodroo:
#    def __init__(self, time)
#
#
if __name__ == "__main__":
    main()
