Communication Contract: Delivery Notification Microservice

This microservice monitors for package delivery events and sends a notification email to a predefined administrator. Other programs communicate with it via text files in the io/ directory. This contract must not change after being published.

How to Programmatically **REQUEST** Data:

Other programs trigger this microservice by writing to the following file:

•	File path: io/email-service.txt

•	Format: A single line with the tracking number and email, separated by a pipe (|)

Example format:

456|dole@oregonstate.edu
  
Example request (Python code):

    with open("io/email-service.txt", "w") as f:
        f.write("456|dole@oregonstate.edu")
        
This tells the microservice to send a delivery email for package 456 to dole@oregonstate.edu.

How to Programmatically **RECEIVE** Data:

The microservice will respond by writing to this file:

•	File path: io/email-response.txt

•	Format: A single line containing either a success or error message

Example format:

SUCCESS: Email sent for package 456 to dole@oregonstate.edu
 
ERROR: [error message]

Example response check (Python code):

    import time
    import os
    
    path = "io/email-response.txt"
    timeout = 5
    start = time.time()
    
    while not os.path.exists(path):
        if time.time() - start > timeout:
            print("Timed out waiting for response")
            break
        time.sleep(0.2)
        
        if os.path.exists(path):
            with open(path, "r") as f:
                print("Response:", f.read().strip())
            os.remove(path)

UML Sequence Diagram:
 ![image](https://github.com/user-attachments/assets/3ca05e45-bfeb-4c32-861f-05c76b522448)

