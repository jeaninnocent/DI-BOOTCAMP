##Exercice 1
from typing import List, Dict

class Phone:
    """Represents a mobile phone with call and messaging capabilities."""
    
    def __init__(self, phone_number: str) -> None:
        """Initializes the Phone with a number, an empty call history, and an empty message list."""
        self.phone_number = phone_number
        self.call_history: List[str] = []
        # Using a list of dictionaries to store messages
        self.messages: List[Dict[str, str]] = []

    def call(self, other_phone: 'Phone') -> None:
        """
        Simulates a call to another phone.
        Prints the action and adds it to the caller's call history.
        """
        call_record = f"{self.phone_number} called {other_phone.phone_number}"
        print(call_record)
        self.call_history.append(call_record)
        # Optionally, we could also log this in the receiver's history:
        # other_phone.call_history.append(f"Received call from {self.phone_number}")

    def show_call_history(self) -> None:
        """Prints the entire call history of the phone."""
        print(f"\n--- Call History for {self.phone_number} ---")
        if not self.call_history:
            print("No calls made yet.")
        for record in self.call_history:
            print(record)

    def send_message(self, other_phone: 'Phone', content: str) -> None:
        """
        Sends a message to another phone.
        Saves the message in both the sender's and the receiver's message history.
        """
        message_data = {
            "to": other_phone.phone_number,
            "from": self.phone_number,
            "content": content
        }
        
        # Save to sender's outbox
        self.messages.append(message_data)
        # Save to receiver's inbox
        other_phone.messages.append(message_data)
        
        print(f"Message successfully sent from {self.phone_number} to {other_phone.phone_number}")

    def show_outgoing_messages(self) -> None:
        """Filters and prints only the messages sent by this phone."""
        print(f"\n--- Outgoing Messages ({self.phone_number}) ---")
        outgoing = [msg for msg in self.messages if msg["from"] == self.phone_number]
        
        if not outgoing:
            print("No outgoing messages.")
        for msg in outgoing:
            print(f"To {msg['to']}: {msg['content']}")

    def show_incoming_messages(self) -> None:
        """Filters and prints only the messages received by this phone."""
        print(f"\n--- Incoming Messages ({self.phone_number}) ---")
        incoming = [msg for msg in self.messages if msg["to"] == self.phone_number]
        
        if not incoming:
            print("No incoming messages.")
        for msg in incoming:
            print(f"From {msg['from']}: {msg['content']}")

    def show_messages_from(self, other_phone: 'Phone') -> None:
        """Filters and prints messages received from a specific phone number."""
        print(f"\n--- Messages from {other_phone.phone_number} ---")
        specific_messages = [
            msg for msg in self.messages 
            if msg["from"] == other_phone.phone_number and msg["to"] == self.phone_number
        ]
        
        if not specific_messages:
            print("No messages from this number.")
        for msg in specific_messages:
            print(f"> {msg['content']}")


# --- Test de l'exercice ---
if __name__ == "__main__":
    # Instantiation de trois téléphones
    my_phone = Phone("+225 01 02 03 04 05")
    alice_phone = Phone("+225 05 04 03 02 01")
    bob_phone = Phone("+225 07 08 09 10 11")

    # Tests des appels
    print("--- TESTING CALLS ---")
    my_phone.call(alice_phone)
    my_phone.call(bob_phone)
    my_phone.show_call_history()

    # Tests des messages
    print("\n--- TESTING MESSAGES ---")
    my_phone.send_message(alice_phone, "Hey Alice, are we still meeting for the project?")
    alice_phone.send_message(my_phone, "Yes, absolutely! See you at 10 AM.")
    bob_phone.send_message(my_phone, "Did you finish the GitHub setup?")

    # Vérification des boîtes de réception/envoi
    my_phone.show_outgoing_messages()
    my_phone.show_incoming_messages()

    # Vérification des messages d'un contact spécifique
    my_phone.show_messages_from(alice_phone)