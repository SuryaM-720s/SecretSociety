# SecretSociety/Team12

A multi-threaded chat server and client implementation inspired by Internet Relay Chat (IRC) principles, supporting multiple channels and concurrent client connections, built with Python for seamless cross-platform communication.

This project was completed as the Team Project Group Chat Service for the CSC 4220 Computer Networks course at Georgia State University.


**Watch the Demo**: [Project  Demo Video](https://www.youtube.com/watch?v=PsmxQ5aOmYc)

---

## Features

- **Multi-Channel Support**: Create and join multiple chat channels simultaneously, enabling organized group conversations.
- **Multi-Threaded Architecture**: Handles up to 100 concurrent client connections using threading for responsive, real-time communication.
- **IRC-Inspired Commands**: Familiar command-line interface with standard IRC commands like `/join`, `/leave`, `/nick`, and `/list`.
- **Object-Based Protocol**: All client-server communication uses JSON-based objects for structured, reliable message passing.
- **Automatic Idle Shutdown**: Server gracefully shuts down after 3 minutes of inactivity to conserve resources.
- **Graceful Shutdown**: Supports Ctrl+C for clean server termination with proper client disconnection handling.
- **Colored Terminal Output**: Enhanced user experience with customizable terminal colors for better message differentiation.
- **Activity Logging**: Comprehensive server-side logging of all user actions and events for debugging and monitoring.

## Demo

To see the full application lifecycle—from server startup to multi-client interaction—here are the key demonstration points:

### Server Initialization
The server starts with configurable port and debug level settings, ready to accept client connections.

### Multi-Client Connection
Multiple clients successfully connect to the server and join different channels, demonstrating concurrent connection handling.

### Real-Time Chat
Messages are broadcast in real time to all users in the same channel, demonstrating multi-threaded message handling.

### Channel Management
Users can create new channels, switch between channels, and see active channel listings with user counts.

## Prerequisites

This project requires Python 3.6 or higher, with the standard library supporting socket programming and threading.

| Component | Requirement | Notes |
|-----------|-------------|-------|
| Python | 3.6 or higher | Must support socket and threading modules |
| Network | Local network or localhost | For client-server communication |
| Terminal | ANSI color support (optional) | For colored terminal output feature |

## Project Structure

```
SecretSociety/
├── ChatServer.py           # Multi-threaded server implementation
├── ChatClient.py           # Interactive chat client
└── README.md              # Project documentation
```

### ChatServer.py

The server handles all client connections, channel management, and message broadcasting.

**Key Components:**
- `handle_client()`: Manages individual client connections and message routing
- `process_command()`: Parses and executes IRC-style commands
- `join_channel()`: Handles channel creation and user join events
- `leave_channel()`: Manages user departure from channels
- `broadcast_message()`: Sends messages to all users in a channel
- `shutdown_if_idle()`: Monitors server activity and handles automatic shutdown
- `graceful_shutdown()`: Ensures clean termination of all connections
- `main()`: Entry point handling argument parsing and server initialization

### ChatClient.py

The client provides an interactive terminal interface for connecting to the server and participating in chat channels.

**Key Components:**
- `receive_messages()`: Continuously listens for incoming server messages
- `connect_to_server()`: Establishes a connection to the specified server
- `send_json()`: Serializes and transmits JSON messages to the server
- `color_text()`: Applies ANSI color codes to terminal output (ref: [GeeksforGeeks](https://www.geeksforgeeks.org/python/print-colors-python-terminal/))
- `main()`: Handles user input, command processing, and client lifecycle

## Building and Running

### Starting the Server

Open a terminal and navigate to the project directory:

```bash
# Run with default port (5555) and minimal logging
python ChatServer.py

# Run with custom port
python ChatServer.py -p 8080

# Run with full debug logging
python ChatServer.py -p 5555 -d 1
```

**Command-Line Arguments:**
- `-p <port>`: Specify server port number (default: 5555)
- `-d <level>`: Set debug level (0 = errors only, 1 = all events)

### Connecting Clients

In separate terminal windows, start as many clients as needed:

```bash
python ChatClient.py
```

Upon execution, you'll be prompted for:
1. **Server IP Address**: Enter the server's IP (use `localhost` or `127.0.0.1` for local testing)
2. **Port Number**: Must match the server's port
3. **Nickname**: Your display name (should be unique)

### Available Commands

Once connected, you can use the following IRC-style commands:

| Command | Description | Example |
|---------|-------------|---------|
| `/connect <server> [port]` | Connect to a chat server | `/connect 127.0.0.1 5555` |
| `/nick <nickname>` | Set or change your nickname | `/nick Alice` |
| `/list` | Display all channels and user counts | `/list` |
| `/join <channel>` | Join or create a channel | `/join #general` |
| `/leave [channel]` | Leave current or specified channel | `/leave` or `/leave #general` |
| `/quit` | Disconnect from server and exit | `/quit` |
| `/help` | Display command reference | `/help` |

Any text that doesn't start with `/` is treated as a message and broadcast to your current channel.

## Testing Methodology

Our testing approach followed a progressive validation strategy:

### Phase 1: Basic Functionality
We verified core operations, including command execution, message sending, channel joining/leaving, and nickname changes. Each command was tested individually to ensure proper server responses and state updates.

### Phase 2: Configuration Testing
We validated custom port selection, verified client connectivity to non-default ports, and tested debug logging levels to ensure proper server configuration handling.

### Phase 3: Stress and Edge Cases
We pushed the system to its limits by:
- Connecting the maximum number of clients (4 concurrent threads)
- Testing rapid channel switching and message flooding
- Attempting duplicate server instances on the same port
- Verifying idle timeout functionality (3-minute inactivity)
- Testing graceful shutdown with active connections

### Phase 4: Multi-User Scenarios
We simulated real-world usage with multiple clients in different channels, verifying message isolation, proper broadcasting, and concurrent operation stability.

## Development Process & Team Roles

This project was a collaborative effort with well-defined responsibilities:

### Team Member

**Jennifer Barrera Vargas** (jbarreravargas1)
- Client-side message handling and user interface
- Color terminal implementation and user experience enhancements
- Testing and validation of client-side functionality

**Jairo Gonzalez-Fragoso** (jgonzalez68)
- Server architecture and multi-threading implementation
- Channel management and message broadcasting logic
- Network protocol design and optimization

**Roshan Savarimuthu** (rsavarimuthu1)
- JSON object protocol design and implementation
- Testing framework and stress testing procedures
- Documentation and code organization

**Suryaprakash Murugavvel** (smurugavvel1)
- Command processing and server-side logic
- Logging system and graceful shutdown implementation
- Integration testing and debugging

### Development Approach

We followed an iterative development model, building complexity in stages:

1. **Single-Channel, Single-Threaded Server**: Established basic client-server communication
2. **Multi-Channel, Single-Threaded Server**: Added channel management without concurrency
3. **Multi-Channel, Multi-Threaded Server**: Implemented threading for concurrent client handling (max 4 threads)

This staged approach allowed us to validate each feature layer before adding complexity, resulting in a stable and maintainable codebase.

## Observations & Reflections

### Technical Insights
- **Threading Challenges**: Managing shared state between threads required careful synchronization to prevent race conditions, particularly in the broadcast messaging system.
- **JSON Protocol**: The object-based protocol proved more maintainable than raw text parsing, with a clear structure for both commands and events.
- **Idle Detection**: Implementing the 3-minute idle timeout required careful tracking of all connection activity timestamps.


### Future Enhancements
If we were to extend this project, we would consider:
- Private messaging between users
- File sharing capabilities
- Encryption for secure communication

## Acknowledgments

- IRC Protocol specification: [RFC 1459](http://tools.ietf.org/html/rfc1459.html)
- Python terminal colors reference: [GeeksforGeeks](https://www.geeksforgeeks.org/python/print-colors-python-terminal/)

---

*This project demonstrates practical application of socket programming, multi-threading, and network protocol design principles in a real-world chat system implementation.*
