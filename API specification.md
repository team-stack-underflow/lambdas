# Runnable API Specification

## Overview 

The Runnable backend consists of a web socket API, with the following functions:
1. Connect
2. Launch
3. Input
4. Output
5. Disconnect

All requests (client to server) and responses (server to client) are to be in the form of strings that can be parsed into JSON format.

## System-triggered Functions

These functions are invoked automatically by the system. No user input is required.

### 1. Connect

This function is automatically invoked when a new connection is being established between client and server. **However, there is currently no functionality attached.**

Responses: None.

### 2. Output

When a running user program writes a line to standard output, this function is automatically invoked. It will send the string of output back to the client.

Response properties:
- `"output"`: Output string from the REPL environment or compiled program.
- `"containerId"`: Identifies which container instance produced the output. Clients may use this field to filter out responses from unwanted containers.

Example response:
```json
{"output": "Hello World!", "containerId": "b19ee7bd-75f5-4444-8542-1eb307dfc176"}
```

### 3. Disconnect

This function is automatically invoked when a client has disconnected. It cleans up allocated resources such as running containers and message queues.

Responses: None.

## User-triggered Functions

These functions are invoked by the user as required.

### 1. Launch

This function is to be invoked when the user wishes to launch a new container instance to run a program.

Request properties:
- `"action"`: Must always be `"launch"`.
- `"lang"`: Language of the program to be run. Current available options are `"python"`, `"c"`, `"java"`, `"javascript"`.
- `"mode"`: Execution mode. Current available options are `"repl"`, `"compile"`.
- `"prog"`: Required only if `"mode"` is `"compile"`. A string containing the source code of the program to be run.

Example requests:
```json
{"action": "launch", "lang": "c", "mode": "repl"}
{"action": "launch", "lang": "python", "mode": "compile", "prog": "print(input())"}
```

Response properties:
- `"containerId"`: String containing the ID of the container instance that was launched, which is needed for future interactions.

Example response:
```json
{"containerId": "b19ee7bd-75f5-4444-8542-1eb307dfc176"}
```

### 2. Input

This function is to be invoked when the user wishes to send input to the running user program, be it a line of code in a REPL environment or supplying standard input to a compiled program.

Request properties:
- `"action"`: Must always be `"input"`.
- `"input"`: String of input to be sent to the program.
- `"input"`: String containing the ID of the container instance where the input is to be sent.

Example request:
```json
{"action": "input", "input": "Hello World!", "containerId": "b19ee7bd-75f5-4444-8542-1eb307dfc176"}
```