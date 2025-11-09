from flask import Flask, render_template, request, session

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):
        new_node = Node(data)
        if self.tail:
            self.tail.next = new_node
            self.tail = new_node

        else:
            self.tail = new_node
            self.head = new_node

    def search(self, data):
        current_node = self.head

        while current_node:
            if current_node.data == data:
                return True
            else:
                current_node = current_node.next
        return False
        

    def dequeue(self):
        if self.head:
            removed_data = self.head.data
            self.head = self.head.next

            if not self.head:
                self.tail = None

            return removed_data

        else:
            return None
        
    def is_empty(self):
        return self.head is None
    
    def front(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.head.data
    
    def size(self):
        i = 0
        cur = self.head
        while cur:
            i += 1
            cur = cur.next
        return i
    
    def convert_to_list(self):
        list = []
        current = self.head
        while current:
            list.append(current.data)
            current = current.next
        return list


class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_front(self, data):
        new_node = Node(data)
        if self.head:
            new_node.next = self.head
            self.head = new_node

        else:
            self.tail = new_node
            self.head = new_node

    def add_rear(self, data):
        new_node = Node(data)
        if self.head:
            self.tail.next = new_node
            self.tail = new_node
        
        else:
            self.head = new_node
            self.tail = new_node
       

    def search(self, data):
        current_node = self.head

        while current_node:
            if current_node.data == data:
                return True
            else:
                current_node = current_node.next
        return False
        

    def remove_front(self):
        if self.head:
            removed_data = self.head.data
            self.head = self.head.next

            if not self.head:
                self.tail = None

            return removed_data

        else:
            return None

    def remove_rear(self):
        if not self.head:
            return None

        if self.head == self.tail:
            removed_data = self.head.data
            self.head = None
            self.tail = None
            return removed_data

        current_node = self.head
        while current_node.next != self.tail:
            current_node = current_node.next

        removed_data = self.tail.data
        self.tail = current_node
        current_node.next = None
        return removed_data
    
    def is_empty(self):
        return self.head is None

    def front(self):
        if self.is_empty():
            raise Exception("Deque is empty")
        return self.head.data

    def rear(self):
        if self.is_empty():
            raise Exception("Deque is empty")
        return self.tail.data

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def convert_to_list(self):
        """Convert deque to a list for display"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

def rebuild_queue():
    """Create a Queue from session data"""
    queue = Queue()
    if 'queue_data' in session:
        for item in session['queue_data']:
            queue.enqueue(item)
    return queue

def save_queue(queue):
    """Save queue to session"""
    session['queue_data'] = queue.convert_to_list()

def rebuild_deque():
    """Create a Deque from session data"""
    deque = Deque()
    if 'deque_data' in session:
        for item in session['deque_data']:
            deque.add_rear(item)
    return deque

def save_deque(deque):
    """Save deque to session"""
    session['deque_data'] = deque.convert_to_list()

app = Flask(__name__)
app.secret_key = 'key'

@app.route('/works')
def works():
    return render_template('workspage.html')

@app.route('/queue', methods=['GET', 'POST'])
def queue():
    
    if 'queue_data' not in session:
        session['queue_data'] = []
    
    message = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        queue = rebuild_queue()
        
        if action == 'add':
            item = request.form.get('item', '').strip()
            if item:
                queue.enqueue(item)
                save_queue(queue)
                message = f"Enqueued: {item}"
        
        elif action == 'remove':
            if not queue.is_empty():
                removed = queue.dequeue()
                save_queue(queue)
                message = f"Dequeued: {removed}"
            else:
                message = "Queue is empty!"
    
    queue = rebuild_queue()
    items = queue.convert_to_list()
    
    return render_template('queue.html', 
                         items=items, 
                         message=message,
                         is_empty=queue.is_empty())

@app.route('/deque', methods=['GET', 'POST'])
def deque():
    
    if 'deque_data' not in session:
        session['deque_data'] = []
    
    message = ""
    
    if request.method == 'POST':
        action = request.form.get('action')
        deque = rebuild_deque()
        
        if action == 'add_front':
            item = request.form.get('item', '').strip()
            if item:
                deque.add_front(item)
                save_deque(deque)
                message = f"Added to front: {item}"
        
        elif action == 'add_rear':
            item = request.form.get('item', '').strip()
            if item:
                deque.add_rear(item)
                save_deque(deque)
                message = f"Added to rear: {item}"
        
        elif action == 'remove_front':
            if not deque.is_empty():
                removed = deque.remove_front()
                save_deque(deque)
                message = f"Removed from front: {removed}"
            else:
                message = "Deque is empty!"
        
        elif action == 'remove_rear':
            if not deque.is_empty():
                removed = deque.remove_rear()
                save_deque(deque)
                message = f"Removed from rear: {removed}"
            else:
                message = "Deque is empty!"
    
    deque = rebuild_deque()
    items = deque.convert_to_list()
    
    return render_template('deque.html', 
                         items=items, 
                         message=message,
                         is_empty=deque.is_empty())

@app.route('/')
def home():
    return render_template('index.html')   

@app.route('/contact')
def contact():
    return render_template('contact.html')  

if __name__ == '__main__':
    app.run(debug=True)