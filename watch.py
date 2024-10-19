#!/usr/bin/env python
import os
import sys
import asyncio
from websockets.asyncio.server import serve

global PREV
PREV = os.stat(sys.argv[1]).st_mtime


async def hello(websocket):
    print("Browser has connected!")
    while not watch_file():
        pass
    print("Notifying Browser!")
    await websocket.send("File Changed!")



async def main():
    async with serve(hello, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever


def watch_file():
    global PREV
    stats = os.stat(sys.argv[1])
    if stats.st_mtime != PREV:
        PREV = stats.st_mtime
        print("File changed!")
        return True
    else:
        return False


def inject_index_html(js_code):
    try:
        with open("./index.html", 'a') as file:  
            file.write('\n')  
            file.write(js_code) 
        print("JavaScript successfully injected into index.js")
    except FileNotFoundError:
        print("Error: index.js not found!")


def clean_index_html(js_code):
    try:
        # Read the original content of the HTML file
        with open("./index.html", 'r') as file:
            content = file.read()

        # Check if the JS code exists in the file
        if js_code in content:
            # Remove the JS block from the content
            updated_content = content.replace(js_code, "")

            # Write the updated content back to the HTML file
            with open("./index.html", 'w') as file:
                file.write(updated_content)

            print(f"JavaScript block successfully removed from ./index.html")
        else:
            print("JavaScript block not found in the index.html!")
    except FileNotFoundError:
        print(f"Error: ./index.html not found!")

if __name__ == "__main__":
    js_code = """
<script tag="WatcherScript">
const socket = new WebSocket('ws://localhost:8765');

socket.onmessage = function(event) {
console.log('Message received:', event.data);
location.reload();
};

socket.onopen = function() {
console.log('Connected to WebSocket server.');
};

socket.onclose = function() {
console.log('WebSocket connection closed.');
};
</script>
    """
    try:
        print("Injecting js into index.html")
        inject_index_html(js_code)
        asyncio.run(main())
    except KeyboardInterrupt:
        clean_index_html(js_code)
        print("Watcher should stop, removing js form index.html")
    
