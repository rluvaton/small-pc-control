# Small PC Control

> Built with Python 2.7

## Commands

- [Connect](https://github.com/rluvaton/small-pc-control#connect)
- [Login](https://github.com/rluvaton/small-pc-control#login)
- [Register](https://github.com/rluvaton/small-pc-control#register)
- [Signup](https://github.com/rluvaton/small-pc-control#signup)
- [Time](https://github.com/rluvaton/small-pc-control#time)
- [Name](https://github.com/rluvaton/small-pc-control#name)
- [Exit](https://github.com/rluvaton/small-pc-control#exit)
- [Screenshot](https://github.com/rluvaton/small-pc-control#screenshot)
- [Run Program](https://github.com/rluvaton/small-pc-control#run-program)
- [Get Folder](https://github.com/rluvaton/small-pc-control#get-folder)
- [File Content](https://github.com/rluvaton/small-pc-control#file-content)
- [Stop Keep Alive](https://github.com/rluvaton/small-pc-control#stop-keep-alive)
- [Stop Heartbeat](https://github.com/rluvaton/small-pc-control#stop-heartbeat)

### Connect
Connect the user
> user must to be registered

**Format:** `connect: <user-name> <password>`

**Example:** `connect: myUserName 123123`

You can also use [`login`](https://github.com/rluvaton/small-pc-control#login)

### Login
Login the user
> user must to be registered

**Format:** `login: <user-name> <password>`

**Example:** `login: myUserName 123123`

You can also use [`connect`](https://github.com/rluvaton/small-pc-control#connect)

### Register
Register user

**Format:** `register: <user-name> <password>`

**Example:** `register: myUserName 123123`

You can also use [`signup`](https://github.com/rluvaton/small-pc-control#signup)

### Signup
Signup user

**Format:** `signup: <user-name> <password>`

**Example:** `signup: myUserName 123123`

You can also use [`register`](https://github.com/rluvaton/small-pc-control#register)

### Time
Get current time
> user must be logged in

**Format:** `time`

**Example:** `time`


### Name
Get the name of the computer
> user must be logged in

**Format:** `name`

**Example:** `name`


### Exit
Exit from the connections
> It will close the program

**Format:** `exit`

**Example:** `exit`


### Screenshot
Take screenshot of the server screen and save it in the server name folder in the client
> user must be logged in

**Format:** `screenshot`

**Example:** `screenshot`


### Run Program
Run program by path
> user must be logged in

**Format:** `run program: <program path>`

**Example:** `run program: C:\Program.exe`


### Get Folder
Get Folder content (files and folder) in the server
> user must be logged in

**Format:** `get folder: <path>`

**Example:** `get folder: C:\`


### File Content
Get File content in the server
> user must be logged in

**Format:** `file content: <file url>`

**Example:** `file content: C:\demo.txt`


### Stop Keep Alive
Stop keep alive messages
> The Server connection will expire after 10 seconds

**Format:** `stop keep alive`

**Example:** `stop keep alive`

You can also use [`stop heartbeat`](https://github.com/rluvaton/small-pc-control#stop-heartbeat)

### Stop Heartbeat
Stop heartbeat messages
> The Server connection will expire after 10 seconds

**Format:** `stop heartbeat`

**Example:** `stop heartbeat`

You can also use [`stop keep alive`](https://github.com/rluvaton/small-pc-control#stop-keep-alive)
