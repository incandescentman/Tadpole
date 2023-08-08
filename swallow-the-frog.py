from PyInquirer import prompt
import datetime
import os

'''
The following script incorporates several important productivity concepts:
...
'''

# Get the current date
date = datetime.date.today()

# Specify the directory for the output file
dir_path = "/Users/jay/dropbox/roam/accountability/"

# Create a new file with the current date in the filename
file_path = f"{dir_path}tasks-{date}.org"

# Step 1: Define Your Daily Goals and Tasks
print("\nStep 1: Define Your Daily Goals and Tasks")
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
print("\nStep 2: Identify the Most Important Tasks")
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
print("\nStep 3: Find the frog")
print("- Review your list of tasks and ask yourself: If I could only accomplish ONE task today, which one would have the greatest positive impact on my life or work?")
print("- Label this task as your 'frog' for the day. This is the task you'll focus on first.")
print("\nrank your most important tasks in order of priority. Hit RETURN to select.")
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
print("- If the task is large or complex, break it down into smaller, manageable parts and start with the first part.")
os.system(f'bat {file_path}')

# Copy the output to the clipboard
os.system(f'cat {file_path} | pbcopy')
