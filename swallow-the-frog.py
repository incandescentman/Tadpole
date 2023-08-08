from PyInquirer import prompt
import datetime

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
    task = input()
    if task:
        tasks.append(task)
    else:
        break

# Ask for the most important tasks
questions = [
    {
        'type': 'checkbox',
        'message': 'Which tasks are the most important ones? Use arrow keys to move, RETURN to select.',
        'name': 'frogs',
        'choices': [{'name': task} for task in tasks]
    }
]

answers = prompt(questions)
frogs = answers['frogs']

# Ask for the ranking of the frogs
questions = [
    {
        'type': 'list',
        'message': 'Please rank your important tasks. Use arrow keys to move and return to submit.',
        'name': 'ranking',
        'choices': [{'name': frog} for frog in frogs]
    }
]

answers = prompt(questions)
ranking = answers['ranking']

# Write tasks to file
with open(file_path, "w") as f:
    f.write(f"* Tasks for today [{len(tasks)}/0]\n")
    for i, task in enumerate(tasks, start=1):
        f.write(f"  - [ ] {task}\n")

    # Write the 'frogs' to file
    f.write("* Frogs for today\n")
    for rank in ranking:
        f.write(f"  - [ ] {rank}\n")

# Display the file
with open(file_path, "r") as f:
    print(f.read())
