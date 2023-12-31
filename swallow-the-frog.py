'''
The following script incorporates several important productivity concepts:

Swallowing the Frog: This is a concept popularized by Brian Tracy in his book "Eat That Frog!" The "frog" is the most challenging task of your day—the one you are most likely to procrastinate on, but also the one that can have the greatest positive impact on your life.

Prioritizing: Prioritizing involves determining the order in which you will handle tasks based on their importance and urgency.

Working on the Most Important Thing: This is the concept of focusing your efforts on the tasks that make the most significant difference.

Experiential Avoidance: This is a concept from psychology that refers to a person's attempt to avoid thoughts, feelings, memories, physical sensations, and other internal experiences—even when doing so creates harm in the long-run.

Accepting Discomfort: This is about understanding that discomfort is a natural part of life and work, and that avoiding it can actually hinder progress and growth.

Not Getting Sidetracked by the Easy Task: This is about resisting the temptation to do easier, less important tasks instead of focusing on the more challenging, critical ones.

Development:
https://chat.openai.com/share/512550f7-cb92-4dff-a46b-a8ebb550d6da

2023-10-09:
https://chat.openai.com/share/e2de705a-03a3-4423-8c19-28cc3f261e23
'''

from PyInquirer import prompt
import datetime
import os
from termcolor import colored
import textwrap
import pyperclip
import sys
import tty
import termios

# Function to clean tasks (remove leading hyphens and optionally mark as subtask)
def clean_task(task):
    """Remove leading hyphen or plus sign from the task description if present.
    Mark as subtask if it starts with a plus sign.
    """
    is_subtask = task.strip().startswith('+')  # Check if task is a subtask
    cleaned_task = task.lstrip('-+ ').strip()  # Remove leading hyphens and plus signs
    if is_subtask:
        cleaned_task = f"subtask: {cleaned_task}"  # Mark it as a subtask
    return cleaned_task


# Function to get a single character input
def get_ch():
    """Get a single character input, works on Unix/Linux."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Clear the terminal screen
os.system('clear')  # For Unix/Linux

# Get the current date
date = datetime.date.today()

# Specify the directory for the output file
dir_path = "/Users/jay/dropbox/roam/accountability/"

# Create a new file with the current date in the filename
file_path = f"{dir_path}tasks-{date}.org"

# Use textwrap to limit the width of the text output
def print_wrapped(text, width=70):
    """Wrap the text within the specified width."""
    wrapped_text = textwrap.fill(text, width=width)
    print(wrapped_text)

# Step 1: Define Your Daily Goals and Tasks
print_wrapped(colored("\nStep 1: Define Your Daily Goals and Tasks", 'white'))
print_wrapped("- Brainstorm a list of everything you need to do.")
print_wrapped("- Make sure each item is actionable and specific.")

# Read the clipboard content
clipboard_content = pyperclip.paste().strip()


# Check if the clipboard starts with a hyphen and a space
if clipboard_content.startswith("- "):
    print(colored("\nThe clipboard contains the following task list:", 'white'))
    # Print each line to preserve line breaks
    for line in clipboard_content.split("\n"):
        print(colored(line, 'white'))

    print("Do you want to use this as your input? [Y/n]: ", end='', flush=True)

    # Get a single character input for confirmation
    confirm = get_ch()

    print()  # Print a newline for better formatting
    # This is for when clipboard is used
    if confirm.lower() in ["", "y", "\r", "\n"]:
        tasks = clipboard_content.split("\n")
        tasks = [clean_task(task) for task in tasks]
    else:
        print_wrapped("\nPlease enter your tasks for today, one per line. Press RETURN twice to finish.")
        tasks = []
        while True:
            task = input()
            if task:
                cleaned_task = clean_task(task)
                tasks.append(cleaned_task)
            else:
                break


# This is for when tasks are manually entered
else:
    print_wrapped("\nPlease enter your tasks for today, one per line. Press RETURN twice to finish.")
    tasks = []
    while True:
        task = input()
        if task:
            cleaned_task = clean_task(task)
            tasks.append(cleaned_task)
        else:
            break

# Step 2: Identify the Most Important Task
print_wrapped(colored("\nStep 2: Identify the Most Important Tasks", 'white'))
print_wrapped("\nWhich tasks are the MOST IMPORTANT ONES? Use the arrow keys to move, SPACE to select, and RETURN to finish.")
questions = [
    {
        'type': 'checkbox',
        'message': 'Select your most important tasks (frogs)',
        'name': 'frogs',
        'choices': [{'name': task} for task in tasks]
    }
]
answers = prompt(questions)
frogs = answers['frogs']

# Step 3: Work on the Most Important Task First
print_wrapped(colored("\nStep 3: Find the frog", 'white'))
print_wrapped("- Review your list of tasks and ask yourself: If I could only accomplish ONE task today, which one would have the greatest positive impact on my life or work?")
print_wrapped("- This task is your frog for the day --- the task you'll focus on first because it's the most important and probably also the most intimidating.")
print_wrapped("- By swallowing the frog first thing and staying on task until it's done, you'll strengthen your ability to accept discomfort.")
print_wrapped("\nRank your most important tasks in order of priority. Hit RETURN to select.")
ranking = []
for i in range(len(frogs)):
    questions = [
        {
            'type': 'list',
            'message': f'Which is your #{i+1} MOST IMPORTANT TASK today?',
            'name': 'rank',
            'choices': [{'name': frog} for frog in frogs if frog not in ranking]
        }
    ]
    answer = prompt(questions)
    ranking.append(answer['rank'])


# Get today's date in YYYY-MM-DD format
today_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Write high-priority tasks to file
with open(file_path, "w") as f:
    f.write(f"** Dailies for {today_date}\n*** High-Priority Tasks [0/{len(tasks)}]\n")
    for i, rank in enumerate(ranking, start=1):
        if rank.startswith('subtask: '):  # Check for subtasks
            rank = rank.replace('subtask: ', '')  # Remove 'subtask: ' prefix
            f.write(f"***** TODO [#A] 🐸 FROG #{i}: {rank}\n")  # Add extra asterisk
        else:
            f.write(f"**** TODO [#A] 🐸 FROG #{i}: {rank}\n")

    for task in tasks:
        if task not in ranking:
            if task.startswith('subtask: '):  # Check for subtasks
                task = task.replace('subtask: ', '')  # Remove 'subtask: ' prefix
                f.write(f"***** TODO {task}\n")  # Add extra asterisk
            else:
                f.write(f"**** TODO {task}\n")


# Step 4: Define Low-Priority Tasks
print_wrapped(colored("\nStep 4: Define Low-Priority Tasks for Today", 'white'))
print_wrapped("Please enter your low-priority tasks for today, one per line. These are tasks that you done't necessarily have to do. You're listening them here as a form of CAPTURE, to get them out of your head so you can stop worrying about trying to remember them. You don't have to do these tasks today, but the point is that you've defined them as LOW-PRIORITY, so don't work on them until you've finished your high-priority tasks. Think of them as a DO NOT DO list --- at least while you're being productive on your other tasks. Press RETURN twice to finish.")
low_priority_tasks = []
while True:
    task = input()
    if task:
        low_priority_tasks.append(task)
    else:
        break


# Append low-priority tasks to the file
with open(file_path, "a") as f:
    f.write("\n*** Low-Priority Tasks (Save These for LATER!!)\n")
    for task in low_priority_tasks:
        if task.startswith('subtask: '):  # Check for subtasks
            task = task.replace('subtask: ', '')  # Remove 'subtask: ' prefix
            f.write(f"***** TODO 🕘 {task}\n")  # Add extra asterisk
        else:
            f.write(f"**** TODO 🕘 {task}\n")



# Display the file using bat
print_wrapped("- Start your workday by focusing on your 'frog'. Resist the temptation to start with easier, less important tasks.")
print_wrapped("- If the task is large, complex, or otherwise daunting, break it down into smaller, manageable steps and start with the first step.")
os.system(f'bat {file_path}')

# Copy the output to the clipboard
os.system(f'cat {file_path} | pbcopy')
