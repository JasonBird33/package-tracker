import os
import uuid
import time

# Directory where communication files live
IO = "io"

# Define file paths for input, output, and storage
CMD = os.path.join(IO, "package-service.txt")      # Where the main program sends commands
RES = os.path.join(IO, "package-response.txt")     # Where we send back a result
DATA = os.path.join(IO, "packages.txt")            # Where we store created packages

# Make a unique ID for each package
def generate_id():
    return "PKG" + str(uuid.uuid4())[:6].upper()

# This service runs in a loop forever, waiting for new commands
while True:
    if os.path.exists(CMD):
        # Read the command sent from main.py
        with open(CMD, 'r') as f:
            cmd = f.read().strip()
        os.remove(CMD)  # Delete the command file to mark it as processed

        parts = cmd.split("|")
        if parts[0] == "CREATE_PACKAGE":
            # Generate a unique package ID
            pid = generate_id()

            # Save package info to packages.txt
            with open(DATA, 'a') as f:
                f.write(f"{pid}|{parts[1]}|{parts[2]}\n")

            # Let the main program know it's done
            with open(RES, 'w') as f:
                f.write(f"Package Created: {pid}")

    time.sleep(0.1)  # Give the CPU a tiny break
