import os
from datetime import datetime

class MemoryManager:
    def __init__(self, chat_file='chat.md',memory_file='memory.md'):
        """Initializes the MemoryManager.

        Args:
            memory_file (str): The path to the markdown file used for memory.
        """
        self.memory_file = memory_file
        self.chat_file = chat_file
        # Create the file if it doesn't exist
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                f.write("# Shared Memory Log\n\n")
        if not os.path.exists(self.chat_file):
            with open(self.chat_file, 'w') as f:
                f.write("# Shared Chat Log\n\n")

    def add_entry(self, agent_name, entry):
        """Adds a new entry to the memory file.

        Args:
            agent_name (str): The name of the agent making the entry.
            entry (str): The content to add to the memory.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.memory_file, 'a') as f:
            f.write(f"**[{timestamp}] {agent_name}:**\n{entry}\n\n")

    def get_memory(self):
        """Reads and returns the entire content of the memory file."""
        with open(self.memory_file, 'r') as f:
            return f.read()

    def clear_memory(self):
        """Clears the memory file, keeping the initial header."""
        with open(self.memory_file, 'w') as f:
            f.write("# Shared Memory Log\n\n")
        print("Memory cleared.")

    def add_memory_chat_convo(self,query,entry):
        """Adds a new entry to the chat file."""
        with open(self.chat_file, 'a') as f:
            f.write(f"**[User:**\n{query}\n\n")
            f.write(f"**[Response:**\n{entry}\n\n")
        


# Example Usage:
if __name__ == '__main__':
    memory_manager = MemoryManager()

    # Example of an agent adding an entry
    memory_manager.add_entry("WebSearchAgent", "Found a relevant article on Stack Overflow about Python decorators.")
    memory_manager.add_entry("CodeRunnerAgent", "Executed the user's script successfully. Output: 'Hello, World!'")

    # Reading the memory
    print("--- Current Memory ---")
    print(memory_manager.get_memory())

    # Clearing the memory
    # memory_manager.clear_memory()
    # print("--- Memory After Clearing ---")
    # print(memory_manager.get_memory())
