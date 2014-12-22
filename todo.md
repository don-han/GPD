TODO: look at old project and see if anything is missing
### Planning and Todo: Getting Pomodoros Done (Terminal ver.)  

- Conscious mind is a focusing tool, not a storage place

- Write down the outcome you want to acheive and then determine the "next physical action" required to move situation forward

- the "next physical action" must be organized in a system one reviews regularly! (put it where one sees it the most) !This should be the primary interface

## Workflow: collect, process, organize , review, do (do is where pomodoro comes in)

# 1. Collect
1. every loop has to be in the collection system, and out of your brain (things to do)
2. fewer collection buckets, the better
3. empty them regularly

# 2. Process - Getting "In" to Empty
the most important part of the step

task = Task()   # the thing you are trying to achieve/goal/desired outcome
if not task.isActionable:
    choose (
        trash(task),                    # delete 
        reference(task),                # reference folder
        incubate(task))                 # someday/maybe folder
        maybe/someday + calendar/tickler (time specific)
    )

task.determineNextAction() # NA is defined as next physical, visible activity that needs to be done to move the task to completion of goal
if task.isProject:
    project(task)   # need to be reviewed

if task.nextAction.duration < 2 minutes :
    task.nextAction.do()
else task.nextAction.duration >= 2 minutes:
    choose(
        task.nextAction.delegate("name"),    # Waiting for list
        task.nextAction.defer()
        # task.nextAction.actionRequired()      # next action list
        # task.nextAction.tickle()             # Calendar
    )

# 3. Organize - Setting up the right bucket
1. trash
2. Incubation tools (someday/ maybe)
3. Reference material
4. "Projects" List: add a subdivision such as personal/professional
5. Project support materials
6. Calendar: actions & informations that needs to be done on a certain time/day # sync with Google?
7. "Next Action" List # organized by context: "calls", "errands", "at home" (place)
8. "Waiting For" list # specific repeating reminders for each task

# 4. Review
Review once a week (may be an alarm?)

# 5. Do
Pomodoro

### The Process
## Business Requirements - What the program should do (setting the lower bound) (User's side)
- create a task that will be stored in Collection Box for future "Processing"
- interactive process stage that lets you "process" each task according to PTD rules
- view any list 
- make an alarm system that will remind you to review the system at a specific interval (default: once a week)
- Make Pomodoro counter so that you can finish off Next Actions

# Version II
- Implement more side of pomodoro (counting each work)

# range of requirement - What sort of requirement? (setting the upper bound)

## Technical Specification - How would you implement the requirements (Creator's side)
# command lines
gpd --help (-h) : shows help
gpd --collect (-c) : add a task into a collection basket
gpd --process (-p) : process task from the most recent to the oldest chronologically
gpd --show (-h) {trash, incubation, reference, projects, support, next, waiting, calendar} : shows argument's list (default: next)
gpd --review (-r) : goes through each list ? # TODO: Find out what to do in review section
gpd --do (-d) : runs pomodoro timer with specified next action

# Classes
- tasks 
- lists 
- pomodoro timer

## Design of Solution - Pseudocode of implementation
# TODO: Implement with the guideline of technical specifications and the goal of the requirement
