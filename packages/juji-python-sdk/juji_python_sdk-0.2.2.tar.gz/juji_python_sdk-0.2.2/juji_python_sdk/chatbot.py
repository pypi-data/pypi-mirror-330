from typing import Optional, Dict, Any, Callable, List
import requests
import websocket
import threading
import json
import time
from queue import Queue

class MessageHandler:
    def __init__(self):
        self.message_queue = Queue()
        self.callbacks: List[Callable] = []

    def on_message(self, ws, message):
        parsed = json.loads(message)
        if "data" in parsed:
            if "chat" in parsed["data"]:
                chat_data = parsed["data"]["chat"]
                if "role" in chat_data and chat_data["role"] == "rep":
                    self.message_queue.put(chat_data)
                    # Execute any registered callbacks
                    for callback in self.callbacks:
                        callback(chat_data)

                    if chat_data["type"] == "user-joined":
                        print("=== Welcome to Juji Bot ===")
                        
    def add_callback(self, callback: Callable[[str], None]):
        """Add a callback function to be called when messages are received"""
        self.callbacks.append(callback)

    def get_messages(self, timeout: Optional[float] = None) -> Optional[List[str]]:
        """Get the text messages from the queue until endOfMessage is True"""
        try:
            messages = []
            message = self.message_queue.get(timeout=timeout)
            while message and not message["endOfMessage"]:
                if message["type"] == "normal":
                    messages.append(message["text"])
                message = self.message_queue.get(timeout=timeout)
            return messages
        except:
            return None


def on_error(ws, error):
    print(f"###WebSocket error: {error}###")

def on_close(ws, close_status_code, close_msg):
    print("###WebSocket connection closed###")

def on_open(ws):
    print("###WebSocket connection opened###")


class Participation:
    """
    Represents an active chat session with a Juji chatbot.
    
    Attributes:
        url (str): The base URL of the session
        participation_id (str): Unique identifier for the chat session
        ws (websocket.WebSocketApp): WebSocket connection
        wst (threading.Thread): Thread for running the WebSocket connection
        message_handler (MessageHandler): Handles incoming messages
    """
    
    def __init__(self, chat_info: Dict[Any, Any], ws: websocket.WebSocketApp, 
                 wst: threading.Thread, message_handler: MessageHandler):
        """
        Initialize a Participation instance.
        
        Args:
            chat_info (Dict[Any, Any]): Chat session information
            ws (websocket.WebSocketApp): WebSocket connection
            wst (threading.Thread): Thread for running the WebSocket connection
            message_handler (MessageHandler): Handles incoming messages
        """
        self.participation_id = chat_info["participationId"]
        self.url = chat_info["websocketUrl"]
        self.ws = ws
        self.wst = wst
        self.message_handler = message_handler

    def get_messages(self) -> Optional[List[str]]:
        """
        Get the text messages from the queue until endOfMessage is True
        """
        return self.message_handler.get_messages(timeout=10)
    
    def send_chat_msg(self, user_msg: str) -> Optional[List[str]]:
        """
        Send a message to the chatbot and get the response.
        
        Args:
            user_msg (str): Message to send to the chatbot
            
        Returns:
            Optional[List[str]]: The chatbot's response, or None if no response received
        """
        self.ws.send("""
        mutation {{
                    saveChatMessage(input: {{
                        type: "normal"
                        pid: "{0}"
                        text: "{1}"
                    }}) {{
                        success
                    }}
                }}
        """.format(self.participation_id, user_msg))
        
        # Wait for and return the response
        return self.message_handler.get_messages(timeout=10)
    
    def add_message_callback(self, callback: Callable[[str], None]):
        """
        Add a callback function to handle incoming messages.
        
        Args:
            callback (Callable[[str], None]): Function to call with each message
        """
        self.message_handler.add_callback(callback)
    
    def end(self) -> None:
        """
        End the current chat session.
        """
        self.ws.close()
        self.wst.join()


class Chatbot:
    """
    A class to interact with a Juji chatbot.
    
    Attributes:
        url (str): The base URL of the chatbot
    """
    
    def __init__(self, url: str):
        """
        Initialize a Chatbot instance.
        
        Args:
            url (str): The base URL of the chatbot
        """
        self.url = url.rstrip('/')  # Remove trailing slash if present
        
    def start_chat(self, first_name: str = "Stranger", last_name: str = None, email: str = None) -> Participation:
        """
        Start a new chat session with the chatbot.
        
        Returns:
            Participation: A new chat session instance
        """
        response = requests.post(f"{self.url}", data={'firstName': first_name, 'lastName': last_name, 'email': email})
        response.raise_for_status()
        chat_info = response.json()
        
        # Create message handler
        message_handler = MessageHandler()
        
        # Create WebSocket connection
        ws = websocket.WebSocketApp(
            chat_info["websocketUrl"],
            on_open=on_open,
            on_message=message_handler.on_message,
            on_error=on_error,
            on_close=on_close
        )
        
        # Start WebSocket thread
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()

        # Wait for connection
        conn_timeout = 5
        while not ws.sock.connected and conn_timeout:
            time.sleep(1)
            conn_timeout -= 1

        if not ws.sock.connected:
            raise Exception("Failed to connect to the chatbot") 

        # Subscribe to chat messages
        ws.send("""
        subscription {{
                chat(input: {{
                    participationId: "{0}"
                }}) {{
                    role
                    text
                    type
                    endOfMessage
                    display{{
                        data{{
                            questions{{
                                heading
                                kind
                            }}
                        }}
                    }}
                }}
            }}""".format(chat_info["participationId"]))
        
        return Participation(chat_info, ws, wst, message_handler)
