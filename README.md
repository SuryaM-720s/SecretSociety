# SecretSociety

# Names/IDs of group members
Jennifer Barrera Vargas - jbarreravargas1
Jairo Gonzalez-Fragoso - jgonzalez68
Roshan Savarimuthu - rsavarimuthu1
Suryaprakash Murugavvel - smurugavvel1

# Web link to demonstration video
------

# A file/folder manifest to guide reading through the code
ChatClient.py
    1-5 Import necessary modules
    7-12 Create variables needed for communication

    receive_messages() - Function for the client to receive messages from the server 

    connect_to_server() - After the user selects the IP and port, this function will connect to the user to the server

    send_json() - Sends JSON messages to server

    color_text() -  Allows color customization of the user's terminal (ref. - https://www.geeksforgeeks.org/python/print-colors-python-terminal/)

    main() - Main function that executes when the program file is run. Prompts the user for the server IP, port number, and nickname for other users. Handles the client side of the IRC chat channel. 

ChatServer.py

    1-7 Import necessary modules 
    9-13 Declare variables and amount of threads for communication

    handle_client() - Function necessary to broadcast messages to other users within the same channel. Also outlines errors and having a client disconnect.

    process_command() - Server will accept user commands and respond with the correct action 

    join_channel() - Creates channels and broadcasts user join messages to other users in the channel 

    leave_channel() - Allows users to leave a channel and broadcast a message to other users in the channel when a user leaves

    broadcast_message() - Allows messages to be broadcast to clients in the same channel

    send_to_client() - Function to allow a message to be sent to a specific client

    disconnect_client() - Function to disconnect a client from the server

    remove_client() - Function to remove a client from a specific channel

    shutdown_if_idle() - Function that handles inactive servers by shutting down the server if no activity is detected within 180 seconds or 3 minutes. 

    graceful_shutdown() - Once Ctrl + C is pressed, the server will be shut down and disconnnect clients.

    main() - Main function that executes once the program file is run. Allows a specific port to be chosen and will log user actions. 




# Running the server/clients

The first step is to start the server. This can be done by opening a terminal and running "python ChatServer.py" (provided you are in the correct directory). By default, the server will choose port 5555 but with the addition of -p <port #>, a specific port can be chosen. With the server running, clients can now be started by opening another terminal and running "python ChatClient.py". Upon execution, prompts to enter the server's IP address, port number, and nickname will show up for the user. After successfully entering in the details, the user can use commands to join/leave a channel, change nickname, list all channels, and more. The server will shut down after no activity has been detected for 3 minutes or Ctrl + C is executed. All clients will be disconnected once either process happens. 

# Testing

Testing was done by first doing normal operations. We used basic commands and ensured that leaving, joining, and other functions worked as intended. After, we decided to test more niche features like choosing a different port number and whether clients could connect as intended. Next, we moved to testing the limits of the program like how many clients could be handled and what happens if another server is opened on the same port.

Overall, we first started testing with ensuring the basic functionalities worked before moving onto more niche and extreme cases. 

# Roles of each group member 

Jennifer Barrera Vargas - jbarreravargas1
    1


Jairo Gonzalez-Fragoso - jgonzalez68
    2


Roshan Savarimuthu - rsavarimuthu1
    3


Suryaprakash Murugavvel - smurugavvel1
    4


