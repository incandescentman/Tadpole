import datetime
import inquirer

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
        more = input("Do you have any more tasks? (y/n) ")
        if more.lower() != "y":
            break

# Ask for the most important tasks
questions = [
    inquirer.Checkbox('frogs',
                      message="Which tasks are the most important ones? Use arrow keys to move, space to select, and return to submit.",
                      choices=tasks,
                      ),
]
frogs = inquirer.prompt(questions)

# Ask for the ranking of the frogs
questions = [
    inquirer.List('ranking',
                  message="Please rank your important tasks. Use arrow keys to move and return to submit.",
                  choices=frogs['frogs'],
                  ),
]
ranking = inquirer.prompt(questions)

# Write tasks to file
with open(file_path, "w") as f:
    f.write(f"* Tasks for today [{len(tasks)}/0]\n")
    for i, task in enumerate(tasks, start=1):
        f.write(f"  - [ ] {task}\n")

    # Write the 'frogs' to file
    f.write("* Frogs for today\n")
    for rank in ranking['ranking']:
        f.write(f"  - [ ] {rank}\n")

    # Ask for any notes
    notes = input("Do you have any notes for today? ")

    # Write notes to file
    f.write("* Notes\n")
    f.write(notes + "\n")

# Display the file
with open(file_path, "r") as f:
    print(f.read())
