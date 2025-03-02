from asyncio import proactor_events
from email import message
import uuid


class Protocol_Common():
  
    def ActionInquire(self,sender,receiver,cmd):
        return {
              "headers": {
                "protocol_version": "1.0",
                "timestamp": "2024-11-08T10:00:00Z",
                "sender": sender,
                "receiver": receiver,
                "message_name": "ActionInquire",
                "conversation_id": uuid.uuid4().hex,
              },
              "body": { 
                "cmd": cmd,
              }
            }
    def ResponseActionComplete(self,message):
        return {
              "headers": {
                "protocol_version": "1.0",
                "timestamp": "2024-11-08T10:00:00Z",
                "sender": message['headers']['receiver'],
                "receiver": message['headers']['sender'],
                "message_name": "ResponseActionComplete",
                "conversation_id": message['headers']['conversation_id'],
              },
              "body": { 
                "status": True,
              }
            }
        
