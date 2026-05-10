from datetime import datetime
class Todo:
    id: int
    title: str
    description: str
    completed: bool
    priority: int
    


    def __init__(self, id: int, title: str, description: str, completed: bool, priority: int):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority
        self.created_at = datetime.now()