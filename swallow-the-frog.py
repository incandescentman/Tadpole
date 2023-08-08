from PyInquirer import prompt
import datetime
import os

# Get the current date
date = datetime.date.today()

# Specify the directory for the output file
dir_path = "/Users/jay/dropbox/roam/accountability/"

# Create a new file with the current date in the filename
file_path = f"{dir_path}tasks-{date}.org"

# Ask for tasks, one per line
print("Please enter your tasks for today, one per line. Press RETURN twice to finish.")
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

# Ask for the most important tasks
questions = [
    {
        'type': 'checkbox',  # Checkbox allows multiple selection
        'message': 'Which tasks are the MOST IMPORTANT ONES? Use the arrow keys to move, SPACE to select, and RETURN to finish.',
        'name': 'frogs',  # Name of the field to save the answers
        'choices': [{'name': task} for task in tasks]  # Choices are the tasks entered by the user
    }
]

# Display the prompt and get the answers from the user
answers = prompt(questions)
# Extract the list of most important tasks (frogs) from the answers
frogs = answers['frogs']

# Ask for the ranking of the frogs
ranking = []
for i in range(len(frogs)):
    questions = [
        {
            'type': 'list',  # List allows single selection
            'message': f'Which is your #{i+1} MOST IMPORTANT TASK today? Hit RETURN to select.',
            'name': 'rank',  # Name of the field to save the answer
            'choices': [{'name': frog} for frog in frogs if frog not in ranking]  # Choices are the frogs not yet ranked
        }
    ]
    # Display the prompt and get the answer from the user
    answer = prompt(questions)
    # Add the selected frog to the ranking list
    ranking.append(answer['rank'])

# Write tasks to file
with open(file_path, "w") as f:
    # Write the task count to the file
    f.write(f"** Tasks for today [0/{len(tasks)}]\n")
    # Write the frogs to the file, in ranked order
    for i, rank in enumerate(ranking, start=1):
        f.write(f"*** TODO [#A] Frog #{i}: {rank}\n")
    # Write the remaining tasks to the file
    for task in tasks:
        if task not in ranking:
            f.write(f"*** TODO {task}\n")

# Display the file using bat
os.system(f'bat {file_path}')

# Copy the output to the clipboard
os.system(f'cat {file_path} | pbcopy')
