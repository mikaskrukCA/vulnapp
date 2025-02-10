import os

def run_command(user_input):
    """
    This function naively appends user-provided input directly to an
    operating system command, making the code susceptible to command injection.
    """
    command = "echo " + user_input
    os.system(command)  # Potentially dangerous when user_input is untrusted.

if __name__ == "__main__":
    user_input = input("Enter something to echo: ")
    run_command(user_input)
