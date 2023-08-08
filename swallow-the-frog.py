from PyInquirer import prompt
import datetime
import os
from termcolor import colored


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
'''


# Clear the terminal screen
os.system('clear')  # For Unix/Linux
# os.system('cls')  # For Windows

# Get the current date
date = datetime.date.today()

# Specify the directory for the output file
dir_path = "/Users/jay/dropbox/roam/accountability/"

# Create a new file with the current date in the filename
file_path = f"{dir_path}tasks-{date}.org"

# Step 1: Define Your Daily Goals and Tasks

print(colored("\nStep 1: Define Your Daily Goals and Tasks", 'white'))
print("- Brainstorm a list of everything you need to do.")
print("- Make sure each item is actionable and specific.")
print("\nPlease enter your tasks for today, one per line. Press RETURN twice to finish.")
tasks = []
while True:
    # Read a line of input from the user
    task = input()
    if task:
        # If the line is not empty, add it to the tasks list
        tasks.append(task)
    else:
        # If the line is empty (the user pressed RETURN), break out of the loop
        break

# Step 2: Identify the Most Important Task
print(colored("\nStep 2: Identify the Most Important Tasks", 'white'))
print("\nWhich tasks are the MOST IMPORTANT ONES? Use the arrow keys to move, SPACE to select, and RETURN to finish.")
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
print(colored("\nStep 3: Find the frog", 'white'))
print("- Review your list of tasks and ask yourself: If I could only accomplish ONE task today, which one would have the greatest positive impact on my life or work?")
print("- This task is your frog for the day --- the task you'll focus on first because it's the most important and probably also the most intimidating.")
print("- By swallowing the frog first thing and staying on task until it's done, you'll strengthen your ability to accept discomfort.")
print("\nRank your most important tasks in order of priority. Hit RETURN to select.")
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

# Write tasks to file
with open(file_path, "w") as f:
    f.write(f"** Tasks for today [0/{len(tasks)}]\n")
    for i, rank in enumerate(ranking, start=1):
        f.write(f"*** TODO [#A] Frog #{i}: {rank}\n")
    for task in tasks:
        if task not in ranking:
            f.write(f"*** TODO {task}\n")

# Display the file using bat
print("- Start your workday by focusing on your 'frog'. Resist the temptation to start with easier, less important tasks.")
print("- If the task is large, complex, or otherwise daunting, break it down into smaller, manageable steps and start with the first step.")
os.system(f'bat {file_path}')

# Copy the output to the clipboard
os.system(f'cat {file_path} | pbcopy')
