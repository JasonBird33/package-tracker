import os
import time
import qrcode


# Folder where all microservices read/write their files
IO = "io"

# Write a command to a text file in the io/ folder
def write_command(filename, message):
    with open(os.path.join(IO, filename), 'w') as f:
        f.write(message)

# Wait for a microservice to respond by creating a file, then read it
def read_response(filename):
    path = os.path.join(IO, filename)
    while not os.path.exists(path):  # Wait until the response file exists
        time.sleep(0.1)
    with open(path, 'r') as f:
        result = f.read()
    os.remove(path)  # Clean up after reading
    return result

# Send a message to the logger microservice
def log_action(message):
    write_command("logger-service.txt", f"LOG|{message}")

# Handle creating a new package with sender and recipient
def create_package():
    # Get and confirm sender
    while True:
        sender = input("Enter sender name: ").strip()
        if not sender:
            print("Sender name is required.")
            continue
        confirm = input(f"You entered '{sender}' as the sender. This cannot be changed later. Is that correct? (yes/no): ").strip().lower()
        if confirm == "yes":
            break
        elif confirm == "no":
            print("Okay, let's try again.")
        else:
            print("Please type 'yes' or 'no'.")

    # Get and confirm recipient
    while True:
        recipient = input("Enter recipient name: ").strip()
        if not recipient:
            print("Recipient name is required.")
            continue
        confirm = input(f"You entered '{recipient}' as the recipient. This cannot be changed later. Is that correct? (yes/no): ").strip().lower()
        if confirm == "yes":
            break
        elif confirm == "no":
            print("Okay, let's try again.")
        else:
            print("Please type 'yes' or 'no'.")

    # Send command to microservice and log it
    write_command("package-service.txt", f"CREATE_PACKAGE|{sender}|{recipient}")
    response = read_response("package-response.txt")
    print(response)

    # Generate QR code for the package ID
    pid = response.split(":")[-1].strip()
    generate_qr_code(pid)

    log_action(f"{response} | Sender: {sender} | Recipient: {recipient}")

    # Ask if they want to see what was logged
    check = input("Would you like to verify the package log entry? (yes/no): ").strip().lower()
    if check == "yes":
        log_path = os.path.join(IO, "log.txt")
        if os.path.exists(log_path):
            with open(log_path, 'r') as log_file:
                lines = log_file.readlines()
                if lines:
                    print("\nLog entry recorded (io/log.txt):")
                    print(lines[-1].strip())
                else:
                    print("Log file is empty.")
        else:
            print("Log file not found.")
    else:
        print("Okay, returning to the main menu.")


# Handle updating the package status
def update_status():
    pid = input("Enter package ID: ").strip()
    status = input("Enter new status: ").strip()
    write_command("tracking-service.txt", f"UPDATE_STATUS|{pid}|{status}")
    response = read_response("tracking-response.txt")
    print(response)
    log_action(f"{pid} status updated to {status}")

# Handle checking the package status
def check_status():
    pid = input("Enter package ID: ").strip()
    write_command("tracking-service.txt", f"GET_STATUS|{pid}")
    response = read_response("tracking-response.txt")
    print(response)

# Handle updating the package location
def update_location():
    pid = input("Enter package ID: ").strip()
    loc = input("Enter new location: ").strip()
    write_command("location-service.txt", f"UPDATE_LOCATION|{pid}|{loc}")
    response = read_response("location-response.txt")
    print(response)
    log_action(f"{pid} location updated to {loc}")

# Handle checking the package location
def check_location():
    pid = input("Enter package ID: ").strip()
    write_command("location-service.txt", f"GET_LOCATION|{pid}")
    response = read_response("location-response.txt")
    print(response)

def view_log():
    log_path = os.path.join(IO, "log.txt")
    print("\n--- PACKAGE LOG ---")
    print("---  io/log.txt ---")
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            lines = f.readlines()
            if lines:
                for line in lines:
                    print(line.strip())
            else:
                print("Log file is empty.")
    else:
        print("No log file found.")

def generate_qr_code(package_id):
    qr = qrcode.make(package_id)
    file_path = os.path.join(IO, f"{package_id}.png")
    qr.save(file_path)
    print(f"QR code saved to {file_path}")

# CLI menu to run everything
def main():
    while True:
        print("\nPACKAGE TRACKING MENU")
        print("1. Create Package")
        print("2. Update Status")
        print("3. Check Status")
        print("4. Update Location")
        print("5. Check Location")
        print("6. Exit")
        print("7. View Log")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_package()
        elif choice == "2":
            update_status()
        elif choice == "3":
            check_status()
        elif choice == "4":
            update_location()
        elif choice == "5":
            check_location()
        elif choice == "6":
            print("Goodbye!")
            break
        elif choice == "7":
            view_log()
        else:
            print("Invalid choice.")

# Run the CLI if this is the main file being executed
if __name__ == "__main__":
    main()
