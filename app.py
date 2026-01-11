from flask import Flask, render_template, request, session, redirect, url_for
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"

# ---------------------------
# Binary Tree implementation
# ---------------------------
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None

    def insert_left(self, parent, value):
        if parent.left is None:
            parent.left = Node(value)
        else:
            new_node = Node(value)
            new_node.left = parent.left
            parent.left = new_node
        return True

    def insert_right(self, parent, value):
        if parent.right is None:
            parent.right = Node(value)
        else:
            new_node = Node(value)
            new_node.right = parent.right
            parent.right = new_node
        return True

    def preorder(self, node, res=""):
        vals = []
        def _pre(n):
            if n:
                vals.append(str(n.value))
                _pre(n.left)
                _pre(n.right)
        _pre(node)
        return " ".join(vals).strip()

    def inorder(self, node, res=""):
        vals = []
        def _in(n):
            if n:
                _in(n.left)
                vals.append(str(n.value))
                _in(n.right)
        _in(node)
        return " ".join(vals).strip()

    def postorder(self, node, res=""):
        vals = []
        def _post(n):
            if n:
                _post(n.left)
                _post(n.right)
                vals.append(str(n.value))
        _post(node)
        return " ".join(vals).strip()

    def search(self, node, key):
        if node is None:
            return False
        if str(node.value) == str(key):
            return True
        return self.search(node.left, key) or self.search(node.right, key)

    def find_node(self, node, key):
        if node is None:
            return None
        if str(node.value) == str(key):
            return node
        left = self.find_node(node.left, key)
        if left:
            return left
        return self.find_node(node.right, key)

    def get_deepest(self):
        queue = [(self.root, None)]
        last, parent = None, None
        while queue:
            node, par = queue.pop(0)
            last, parent = node, par
            if node.left:
                queue.append((node.left, node))
            if node.right:
                queue.append((node.right, node))
        return last, parent

    def delete(self, key):
        if self.root is None:
            return False

        node_to_delete = self.find_node(self.root, key)
        if node_to_delete is None:
            return False

        deepest, parent = self.get_deepest()
        if deepest is None:
            return False

        if node_to_delete == deepest:
            if parent is None:
                self.root = None
            elif parent.left == deepest:
                parent.left = None
            else:
                parent.right = None
            return True

        node_to_delete.value = deepest.value

        if parent.left == deepest:
            parent.left = None
        else:
            parent.right = None

        return True

    def get_max_value(self, node):
        if node is None:
            return None

        left_max = self.get_max_value(node.left) if node.left else None
        right_max = self.get_max_value(node.right) if node.right else None

        # pick the maximum among node.value, left_max, right_max
        candidates = [c for c in (node.value, left_max, right_max) if c is not None]

        def to_number_if_possible(x):
            try:
                return float(x)
            except Exception:
                return None

        # if all numeric comparables exist, compare numerically, otherwise fall back to string compare
        nums = [to_number_if_possible(c) for c in candidates]
        if all(n is not None for n in nums) and len(nums) > 0:
            max_index = nums.index(max(nums))
            return candidates[max_index]

        # fallback to string comparison
        return max(map(str, candidates)) if candidates else None

    def get_min_value(self, node):
        if node is None:
            return None

        left_min = self.get_min_value(node.left) if node.left else None
        right_min = self.get_min_value(node.right) if node.right else None

        candidates = [c for c in (node.value, left_min, right_min) if c is not None]

        def to_number_if_possible(x):
            try:
                return float(x)
            except Exception:
                return None

        nums = [to_number_if_possible(c) for c in candidates]
        if all(n is not None for n in nums) and len(nums) > 0:
            min_index = nums.index(min(nums))
            return candidates[min_index]

        return min(map(str, candidates)) if candidates else None

    def find_height(self, node):
        if node is None:
            return -1
        left_h = self.find_height(node.left)
        right_h = self.find_height(node.right)
        return max(left_h, right_h) + 1

    def bst_insert(self, value):
        """Insert a value into the tree following BST ordering.

        Comparison: try numeric comparison first; if conversion fails, use string comparison.
        """
        if value is None or str(value).strip() == "":
            return False

        if self.root is None:
            self.root = Node(value)
            return True

        def less(a, b):
            try:
                return float(a) < float(b)
            except Exception:
                return str(a) < str(b)

        cur = self.root
        while True:
            if less(value, cur.value):
                if cur.left is None:
                    cur.left = Node(value)
                    return True
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = Node(value)
                    return True
                cur = cur.right

    def _compare(self, a, b):
        """Return -1 if a<b, 0 if equal, 1 if a>b. Numeric compare preferred."""
        try:
            fa = float(a)
            fb = float(b)
            if fa < fb:
                return -1
            if fa > fb:
                return 1
            return 0
        except Exception:
            sa = str(a)
            sb = str(b)
            if sa < sb:
                return -1
            if sa > sb:
                return 1
            return 0

    def _min_node(self, node):
        cur = node
        if cur is None:
            return None
        while cur.left:
            cur = cur.left
        return cur

    def bst_delete(self, key):
        """Delete a node by key following BST deletion rules.

        Returns True if a node was deleted, False otherwise.
        """
        def delete_node(node, key):
            if node is None:
                return node, False

            cmp = self._compare(key, node.value)
            if cmp < 0:
                node.left, deleted = delete_node(node.left, key)
                return node, deleted
            elif cmp > 0:
                node.right, deleted = delete_node(node.right, key)
                return node, deleted
            else:
                # found the node to delete
                # Case 1: leaf
                if node.left is None and node.right is None:
                    return None, True
                # Case 2: one child
                if node.left is None:
                    return node.right, True
                if node.right is None:
                    return node.left, True
                # Case 3: two children -> find inorder successor (min in right subtree)
                succ = self._min_node(node.right)
                node.value = succ.value
                node.right, _ = delete_node(node.right, succ.value)
                return node, True

        self.root, deleted = delete_node(self.root, key)
        return deleted


# ---------------------------
# Serialization helpers
# ---------------------------
def serialize(node):
    if node is None:
        return None
    return {
        "value": node.value,
        "left": serialize(node.left),
        "right": serialize(node.right),
    }

def deserialize(data):
    if data is None:
        return None
    node = Node(data["value"])
    node.left = deserialize(data["left"])
    node.right = deserialize(data["right"])
    return node

def rebuild_tree():
    tree = BinaryTree()
    if "tree_data" in session:
        tree.root = deserialize(session["tree_data"])
    return tree

def save_tree(tree):
    session["tree_data"] = serialize(tree.root)


# ---------------------------
# Queue / Deque structures
# ---------------------------
class NodeQ:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):
        new = NodeQ(data)
        if self.tail:
            self.tail.next = new
            self.tail = new
        else:
            self.head = new
            self.tail = new

    def dequeue(self):
        if not self.head:
            return None
        removed = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return removed

    def convert_to_list(self):
        arr = []
        cur = self.head
        while cur:
            arr.append(cur.data)
            cur = cur.next
        return arr

def rebuild_queue():
    q = Queue()
    for item in session.get("queue_data", []):
        q.enqueue(item)
    return q

def save_queue(q):
    session["queue_data"] = q.convert_to_list()


class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_front(self, data):
        new = NodeQ(data)
        if self.head:
            new.next = self.head
            self.head = new
        else:
            self.head = new
            self.tail = new

    def add_rear(self, data):
        new = NodeQ(data)
        if self.tail:
            self.tail.next = new
            self.tail = new
        else:
            self.head = new
            self.tail = new

    def remove_front(self):
        if not self.head:
            return None
        removed = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return removed

    def remove_rear(self):
        if not self.head:
            return None
        if self.head == self.tail:
            removed = self.head.data
            self.head = None
            self.tail = None
            return removed
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
        removed = self.tail.data
        cur.next = None
        self.tail = cur
        return removed

    def convert_to_list(self):
        arr = []
        cur = self.head
        while cur:
            arr.append(cur.data)
            cur = cur.next
        return arr

def rebuild_deque():
    dq = Deque()
    for i in session.get("deque_data", []):
        dq.add_rear(i)
    return dq

def save_deque(dq):
    session["deque_data"] = dq.convert_to_list()


# ---------------------------
# SVG BINARY TREE RENDERER
# ---------------------------
def svg_from_tree(root):
    if root is None:
        return ""

    nodes = []
    edges = []
    counter = {"i": 0}
    positions = {}

    def inorder_assign(node, depth=0):
        if node is None:
            return
        inorder_assign(node.left, depth + 1)
        x = counter["i"]
        positions[id(node)] = {"node": node, "x_index": x, "depth": depth}
        counter["i"] += 1
        inorder_assign(node.right, depth + 1)

    inorder_assign(root)

    x_spacing = 110
    y_spacing = 90
    node_w = 64
    node_h = 34

    for info in positions.values():
        x = info["x_index"] * x_spacing + 50
        y = info["depth"] * y_spacing + 40
        nodes.append({"node": info["node"], "x": x, "y": y})

    node_by_id = {id(n["node"]): n for n in nodes}

    for n in nodes:
        node = n["node"]
        if node.left:
            edges.append((n["x"], n["y"], node_by_id[id(node.left)]["x"], node_by_id[id(node.left)]["y"]))
        if node.right:
            edges.append((n["x"], n["y"], node_by_id[id(node.right)]["x"], node_by_id[id(node.right)]["y"]))

    max_x = max(n["x"] for n in nodes) + node_w
    max_y = max(n["y"] for n in nodes) + node_h + 20

    width = max(max_x + 20, 360)
    height = max_y + 20

    svg = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<defs><style>.edge{stroke:#666;stroke-width:2}.node-rect{fill:white;stroke:#2c7;stroke-width:1.5;rx:8;}.node-text{font-family:Arial; font-size:14px; fill:#222; font-weight:700;text-anchor:middle;dominant-baseline:middle;}</style></defs>')

    for x1, y1, x2, y2 in edges:
        svg.append(f'<line class="edge" x1="{x1}" y1="{y1+20}" x2="{x2}" y2="{y2-20}" />')

    for n in nodes:
        x, y = n["x"], n["y"]
        v = n["node"].value
        svg.append(f'''
        <g>
            <rect class="node-rect" x="{x-32}" y="{y-17}" width="64" height="34" rx="10"></rect>
            <text class="node-text" x="{x}" y="{y}">{v}</text>
        </g>
        ''')

    svg.append('</svg>')
    return "".join(svg)


# ---------------------------
# ROUTES (RESTORED ORIGINAL NAMES)
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/works")
def works():
    return render_template("workspage.html")

# ORIGINAL ROUTE NAME RESTORED
@app.route("/queue", methods=["GET", "POST"])
def queue():
    if "queue_data" not in session:
        session["queue_data"] = []

    q = rebuild_queue()
    message = ""

    if request.method == "POST":
        action = request.form.get("action")
        item = request.form.get("item", "").strip()

        if action == "add" and item:
            q.enqueue(item)
            save_queue(q)
            message = f"Enqueued: {item}"

        elif action == "remove":
            removed = q.dequeue()
            save_queue(q)
            message = f"Dequeued: {removed}" if removed else "Queue empty!"

    return render_template("queue.html", items=q.convert_to_list(), message=message)


# ORIGINAL NAME RESTORED
@app.route("/deque", methods=["GET", "POST"])
def deque():
    if "deque_data" not in session:
        session["deque_data"] = []

    dq = rebuild_deque()
    message = ""

    if request.method == "POST":
        action = request.form.get("action")
        item = request.form.get("item", "").strip()

        if action == "add_front" and item:
            dq.add_front(item)
            message = f"Added to front: {item}"

        elif action == "add_rear" and item:
            dq.add_rear(item)
            message = f"Added to rear: {item}"

        elif action == "remove_front":
            removed = dq.remove_front()
            message = f"Removed front: {removed}"

        elif action == "remove_rear":
            removed = dq.remove_rear()
            message = f"Removed rear: {removed}"

        save_deque(dq)

    return render_template("deque.html", items=dq.convert_to_list(), message=message)


# ORIGINAL TREE ROUTE NAME RESTORED
@app.route("/tree", methods=["GET"])
def tree():
    tree = rebuild_tree()
    traversals = {
        "preorder": tree.preorder(tree.root) if tree.root else "",
        "inorder": tree.inorder(tree.root) if tree.root else "",
        "postorder": tree.postorder(tree.root) if tree.root else "",
    }
    svg = svg_from_tree(tree.root)
    return render_template("tree.html", traversals=traversals, svg_html=Markup(svg), message="")

@app.route("/tree/insert", methods=["POST"])
def tree_insert():
    tree = rebuild_tree()
    parent_val = request.form.get("parent", "").strip()
    value = request.form.get("value", "").strip()
    side = request.form.get("side", "left")

    if tree.root is None:
        tree.root = Node(parent_val)
        save_tree(tree)

    parent = tree.find_node(tree.root, parent_val)
    if not parent:
        svg = svg_from_tree(tree.root)
        return render_template("tree.html", traversals={}, svg_html=Markup(svg), message=f"Parent '{parent_val}' not found.")

    if side == "left":
        tree.insert_left(parent, value)
    else:
        tree.insert_right(parent, value)

    save_tree(tree)

    traversals = {
        "preorder": tree.preorder(tree.root),
        "inorder": tree.inorder(tree.root),
        "postorder": tree.postorder(tree.root),
    }
    svg = svg_from_tree(tree.root)

    return render_template("tree.html", traversals=traversals, svg_html=Markup(svg),
                           message=f"Inserted '{value}' at {side} of '{parent_val}'")


@app.route("/tree/search", methods=["POST"])
def tree_search():
    tree = rebuild_tree()
    key = request.form.get("search_key", "").strip()
    found = tree.search(tree.root, key)

    message = f"'{key}' found!" if found else f"'{key}' NOT found."

    traversals = {
        "preorder": tree.preorder(tree.root),
        "inorder": tree.inorder(tree.root),
        "postorder": tree.postorder(tree.root),
    }

    svg = svg_from_tree(tree.root)
    return render_template("tree.html", traversals=traversals, svg_html=Markup(svg), message=message)


@app.route("/tree/delete", methods=["POST"])
def tree_delete():
    tree = rebuild_tree()
    key = request.form.get("delete_key", "").strip()
    ok = tree.delete(key)

    message = f"Deleted '{key}'." if ok else f"'{key}' not found."

    save_tree(tree)

    traversals = {
        "preorder": tree.preorder(tree.root),
        "inorder": tree.inorder(tree.root),
        "postorder": tree.postorder(tree.root),
    }

    svg = svg_from_tree(tree.root)
    return render_template("tree.html", traversals=traversals, svg_html=Markup(svg), message=message)


@app.route("/bst", methods=["GET"])
def bst():
    tree = rebuild_tree()
    traversals = {
        "preorder": tree.preorder(tree.root) if tree.root else "",
        "inorder": tree.inorder(tree.root) if tree.root else "",
        "postorder": tree.postorder(tree.root) if tree.root else "",
    }
    svg = svg_from_tree(tree.root)
    return render_template("bst.html", traversals=traversals, svg_html=Markup(svg), message="")


@app.route("/bst/search", methods=["POST"])
def bst_search():
    tree = rebuild_tree()
    key = request.form.get("search_key", "").strip()
    found = tree.search(tree.root, key)
    message = f"'{key}' found!" if found else f"'{key}' NOT found."
    traversals = {
        "preorder": tree.preorder(tree.root),
        "inorder": tree.inorder(tree.root),
        "postorder": tree.postorder(tree.root),
    }
    svg = svg_from_tree(tree.root)
    return render_template("bst.html", traversals=traversals, svg_html=Markup(svg), message=message)


@app.route("/bst/delete", methods=["POST"])
def bst_delete():
    tree = rebuild_tree()
    key = request.form.get("delete_key", "").strip()
    ok = tree.bst_delete(key)
    message = f"Deleted '{key}'." if ok else f"'{key}' not found."
    if ok:
        save_tree(tree)
    traversals = {
        "preorder": tree.preorder(tree.root),
        "inorder": tree.inorder(tree.root),
        "postorder": tree.postorder(tree.root),
    }
    svg = svg_from_tree(tree.root)
    return render_template("bst.html", traversals=traversals, svg_html=Markup(svg), message=message)


@app.route("/bst/max", methods=["POST"])
def bst_max():
    tree = rebuild_tree()
    if tree.root is None:
        message = "Tree is empty."
    else:
        m = tree.get_max_value(tree.root)
        message = f"Max value: {m}" if m is not None else "No values found."

    traversals = {
        "preorder": tree.preorder(tree.root) if tree.root else "",
        "inorder": tree.inorder(tree.root) if tree.root else "",
        "postorder": tree.postorder(tree.root) if tree.root else "",
    }
    svg = svg_from_tree(tree.root)
    return render_template("bst.html", traversals=traversals, svg_html=Markup(svg), message=message)


@app.route("/bst/min", methods=["POST"])
def bst_min():
    tree = rebuild_tree()
    if tree.root is None:
        message = "Tree is empty."
    else:
        m = tree.get_min_value(tree.root)
        message = f"Min value: {m}" if m is not None else "No values found."

    traversals = {
        "preorder": tree.preorder(tree.root) if tree.root else "",
        "inorder": tree.inorder(tree.root) if tree.root else "",
        "postorder": tree.postorder(tree.root) if tree.root else "",
    }
    svg = svg_from_tree(tree.root)
    return render_template("bst.html", traversals=traversals, svg_html=Markup(svg), message=message)


@app.route("/bst/height", methods=["POST"])
def bst_height():
    tree = rebuild_tree()
    key = request.form.get("height_key", "").strip()
    node = tree.find_node(tree.root, key)
    if node is None:
        message = f"Node '{key}' not found."
    else:
        h = tree.find_height(node)
        message = f"Height of node '{key}': {h}"

    traversals = {
        "preorder": tree.preorder(tree.root) if tree.root else "",
        "inorder": tree.inorder(tree.root) if tree.root else "",
        "postorder": tree.postorder(tree.root) if tree.root else "",
    }
    svg = svg_from_tree(tree.root)
    return render_template("bst.html", traversals=traversals, svg_html=Markup(svg), message=message)


@app.route("/bst/insert", methods=["POST"])
def bst_insert():
    tree = rebuild_tree()
    value = request.form.get("value", "").strip()
    if value == "":
        message = "No value provided."
    else:
        # If there's no root, create it; otherwise, perform BST insert
        if tree.root is None:
            tree.root = Node(value)
        else:
            tree.bst_insert(value)
        save_tree(tree)
        message = f"Inserted '{value}' into BST."

    traversals = {
        "preorder": tree.preorder(tree.root) if tree.root else "",
        "inorder": tree.inorder(tree.root) if tree.root else "",
        "postorder": tree.postorder(tree.root) if tree.root else "",
    }
    svg = svg_from_tree(tree.root)
    return render_template("bst.html", traversals=traversals, svg_html=Markup(svg), message=message)


# CONTACT PAGE ROUTE
@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------------------
# MRT/LRT Graph Structure with BFS
# ---------------------------
class MRTGraph:
    def __init__(self):
        # MRT Line 3 (Blue), LRT Line 1 (Yellow), LRT Line 2 (Purple/Violet)
        # Transfer stations (where lines physically intersect):
        # - Araneta Center-Cubao: MRT3 ↔ LRT2 (lines intersect)
        # - Taft Avenue/EDSA: MRT3 ↔ LRT1 (lines intersect)
        # - Recto/Doroteo Jose: LRT2 ↔ LRT1 (lines intersect)
        # Note: Duplicate station names (e.g., "Santolan") are separate stations in the same area, NOT connected
        
        self.stations = {
            # MRT Line 3 
            "North Avenue": ["Quezon Avenue"],
            "Quezon Avenue": ["North Avenue", "GMA Kamuning"],
            "GMA Kamuning": ["Quezon Avenue", "Araneta Center-Cubao"],
            "Araneta Center-Cubao": ["GMA Kamuning", "Santolan (MRT)", "Betty Go-Belmonte"],  # Transfer to LRT2
            "Santolan (MRT)": ["Araneta Center-Cubao", "Ortigas"], 
            "Ortigas": ["Santolan (MRT)", "Shaw Boulevard"],
            "Shaw Boulevard": ["Ortigas", "Boni"],
            "Boni": ["Shaw Boulevard", "Guadalupe"],
            "Guadalupe": ["Boni", "Buendia"],
            "Buendia": ["Guadalupe", "Ayala"],
            "Ayala": ["Buendia", "Magallanes"],
            "Magallanes": ["Ayala", "Taft Avenue"],
            "Taft Avenue": ["Magallanes", "EDSA"],  # Transfer to LRT1
            
            # LRT Line 2 
            "Recto": ["Legarda", "Doroteo Jose"],  # Transfer to LRT1
            "Legarda": ["Recto", "Pureza"],
            "Pureza": ["Legarda", "v Mapa"],
            "v Mapa": ["Pureza", "J. Ruiz"],
            "J. Ruiz": ["v Mapa", "Gilmore"],
            "Gilmore": ["J. Ruiz", "Betty Go-Belmonte"],
            "Betty Go-Belmonte": ["Gilmore", "Araneta Center-Cubao"],  # Transfer to MRT3
            "Anonas": ["Araneta Center-Cubao", "Katipunan"],
            "Katipunan": ["Anonas", "Santolan (LRT2)"],
            "Santolan (LRT2)": ["Katipunan"],  
            
            # LRT Line 1 
            "Monumento": ["Balintawak", "5th Avenue"],
            "Balintawak": ["Roosevelt", "Monumento"],
            "Roosevelt": ["Malvar", "Balintawak"],
            "Malvar": ["Roosevelt"],
            "5th Avenue": ["Monumento", "R. Papa"],
            "R. Papa": ["5th Avenue", "Abad Santos"],
            "Abad Santos": ["R. Papa", "Blumentritt"],
            "Blumentritt": ["Abad Santos", "Tayuman"],
            "Tayuman": ["Blumentritt", "Bambang"],
            "Bambang": ["Tayuman", "Doroteo Jose"],
            "Doroteo Jose": ["Bambang", "Carriedo", "Recto"],  # Transfer to LRT2
            "Carriedo": ["Doroteo Jose", "Central Terminal"],
            "Central Terminal": ["Carriedo", "United Nations"],
            "United Nations": ["Central Terminal", "Pedro Gil"],
            "Pedro Gil": ["United Nations", "Quirino"],
            "Quirino": ["Pedro Gil", "Vito Cruz"],
            "Vito Cruz": ["Quirino", "Gil Puyat"],
            "Gil Puyat": ["Vito Cruz", "Libertad"],
            "Libertad": ["Gil Puyat", "EDSA"],
            "EDSA": ["Libertad", "Baclaran", "Taft Avenue"],  # Transfer to MRT3
            "Baclaran": ["EDSA"]
        }

    def bfs_shortest_path(self, start, end):
        """Find shortest path using BFS (Breadth-First Search) with Python queue."""
        if start not in self.stations or end not in self.stations:
            return None, "One or both stations not found."
        
        if start == end:
            return [start], f"Already at {start}."
        
        # BFS sya
        queue = Queue()
        queue.enqueue((start, [start]))  
        visited = {start}
        
        while queue.head is not None:
            current, path = queue.dequeue()
            
            # lf neighbor
            for neighbor in self.stations.get(current, []):
                if neighbor == end:
                    return path + [neighbor], None
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue((neighbor, path + [neighbor]))
        
        return None, "No path found between stations."



mrt_graph = MRTGraph()


@app.route("/graph", methods=["GET", "POST"])
def graph():
    """MRT/LRT Graph shortest path finder using BFS."""
    message = ""
    path = []
    start_station = ""
    end_station = ""
    
    if request.method == "POST":
        start_station = request.form.get("start_station", "").strip()
        end_station = request.form.get("end_station", "").strip()
        
        if start_station and end_station:
            path, error = mrt_graph.bfs_shortest_path(start_station, end_station)
            if error:
                message = f"Error: {error}"
            elif path:
                stations_count = len(path) - 1
                message = f"Shortest path found! ({stations_count} station{'s' if stations_count != 1 else ''} away)"
            else:
                message = "No path found."
        else:
            message = "Please select both start and end stations."
    
    
    all_stations = sorted(mrt_graph.stations.keys())
    
    return render_template("graph.html", 
                         stations=all_stations,
                         path=path,
                         start_station=start_station,
                         end_station=end_station,
                         message=message)


# ---------------------------
# Sorting Algorithms
# ---------------------------
def bubble_sort(arr):
    """Bubble Sort - compares adjacent elements and swaps them.
    Time Complexity: O(n²) - Best: O(n), Worst: O(n²), Average: O(n²)
    Space Complexity: O(1)
    """
    arr = arr.copy()
    steps = []
    n = len(arr)
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            steps.append({"array": arr.copy(), "comparing": [j, j+1], "sorted": list(range(n-i, n))})
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                steps.append({"array": arr.copy(), "swapped": [j, j+1], "sorted": list(range(n-i, n))})
        if not swapped:
            break
    
    steps.append({"array": arr.copy(), "comparing": [], "sorted": list(range(n))})
    return arr, steps

def selection_sort(arr):
    """Selection Sort - finds minimum element and places it at beginning.
    Time Complexity: O(n²) - Best: O(n²), Worst: O(n²), Average: O(n²)
    Space Complexity: O(1)
    """
    arr = arr.copy()
    steps = []
    n = len(arr)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            steps.append({"array": arr.copy(), "comparing": [min_idx, j], "sorted": list(range(i))})
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append({"array": arr.copy(), "swapped": [i, min_idx], "sorted": list(range(i+1))})
    
    steps.append({"array": arr.copy(), "comparing": [], "sorted": list(range(n))})
    return arr, steps

def insertion_sort(arr):
    """Insertion Sort - builds sorted array one element at a time.
    Time Complexity: O(n²) - Best: O(n), Worst: O(n²), Average: O(n²)
    Space Complexity: O(1)
    """
    arr = arr.copy()
    steps = []
    n = len(arr)
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        steps.append({"array": arr.copy(), "comparing": [i], "sorted": list(range(i))})
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            steps.append({"array": arr.copy(), "comparing": [j, j+1], "sorted": []})
            j -= 1
        
        arr[j + 1] = key
        steps.append({"array": arr.copy(), "comparing": [], "sorted": list(range(i+1))})
    
    steps.append({"array": arr.copy(), "comparing": [], "sorted": list(range(n))})
    return arr, steps

def merge_sort(arr):
    """Merge Sort - divides array and merges sorted halves.
    Time Complexity: O(n log n) - Best: O(n log n), Worst: O(n log n), Average: O(n log n)
    Space Complexity: O(n)
    """
    steps = []
    
    def merge_sort_helper(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            
            merge_sort_helper(arr, left, mid)
            merge_sort_helper(arr, mid + 1, right)
            merge(arr, left, mid, right)
    
    def merge(arr, left, mid, right):
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            steps.append({"array": arr.copy(), "comparing": [left + i, mid + 1 + j], "sorted": []})
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1
            steps.append({"array": arr.copy(), "comparing": [], "sorted": []})
        
        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
            steps.append({"array": arr.copy(), "comparing": [], "sorted": []})
        
        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
            steps.append({"array": arr.copy(), "comparing": [], "sorted": []})
    
    arr = arr.copy()
    merge_sort_helper(arr, 0, len(arr) - 1)
    steps.append({"array": arr.copy(), "comparing": [], "sorted": list(range(len(arr)))})
    return arr, steps

def quicksort(arr):
    """Quicksort - partitions array around pivot element.
    Time Complexity: O(n log n) - Best: O(n log n), Worst: O(n²), Average: O(n log n)
    Space Complexity: O(log n)
    """
    steps = []
    
    def quicksort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quicksort_helper(arr, low, pi - 1)
            quicksort_helper(arr, pi + 1, high)
    
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        
        steps.append({"array": arr.copy(), "comparing": [high], "sorted": [], "pivot": high})
        
        for j in range(low, high):
            steps.append({"array": arr.copy(), "comparing": [j, high], "sorted": [], "pivot": high})
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append({"array": arr.copy(), "swapped": [i, j], "sorted": [], "pivot": high})
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append({"array": arr.copy(), "swapped": [i+1, high], "sorted": []})
        return i + 1
    
    arr = arr.copy()
    quicksort_helper(arr, 0, len(arr) - 1)
    steps.append({"array": arr.copy(), "comparing": [], "sorted": list(range(len(arr)))})
    return arr, steps


@app.route("/sorting", methods=["GET", "POST"])
def sorting():
    """Sorting algorithms demonstration page."""
    message = ""
    result = None
    algorithm_info = {
        "bubble": {
            "name": "Bubble Sort",
            "time_best": "O(n)",
            "time_avg": "O(n²)",
            "time_worst": "O(n²)",
            "space": "O(1)",
            "description": "Repeatedly compares adjacent elements and swaps them if they're in wrong order."
        },
        "selection": {
            "name": "Selection Sort",
            "time_best": "O(n²)",
            "time_avg": "O(n²)",
            "time_worst": "O(n²)",
            "space": "O(1)",
            "description": "Finds the minimum element and places it at the beginning, repeatedly."
        },
        "insertion": {
            "name": "Insertion Sort",
            "time_best": "O(n)",
            "time_avg": "O(n²)",
            "time_worst": "O(n²)",
            "space": "O(1)",
            "description": "Builds the sorted array one element at a time by inserting elements in their correct position."
        },
        "merge": {
            "name": "Merge Sort",
            "time_best": "O(n log n)",
            "time_avg": "O(n log n)",
            "time_worst": "O(n log n)",
            "space": "O(n)",
            "description": "Divides array into halves, sorts them, and merges them back together."
        },
        "quick": {
            "name": "Quicksort",
            "time_best": "O(n log n)",
            "time_avg": "O(n log n)",
            "time_worst": "O(n²)",
            "space": "O(log n)",
            "description": "Selects a pivot element and partitions array around it, recursively sorting partitions."
        }
    }
    
    if request.method == "POST":
        algorithm = request.form.get("algorithm")
        input_str = request.form.get("array_input", "").strip()
        
        if not input_str:
            message = "Please enter numbers to sort."
        else:
            try:
                # Parse input
                arr = [int(x.strip()) for x in input_str.replace(",", " ").split() if x.strip()]
                
                if len(arr) == 0:
                    message = "Please enter at least one number."
                elif len(arr) > 20:
                    message = "Please enter 20 or fewer numbers for visualization."
                else:
                    original = arr.copy()
                    
                    if algorithm == "bubble":
                        sorted_arr, steps = bubble_sort(arr)
                    elif algorithm == "selection":
                        sorted_arr, steps = selection_sort(arr)
                    elif algorithm == "insertion":
                        sorted_arr, steps = insertion_sort(arr)
                    elif algorithm == "merge":
                        sorted_arr, steps = merge_sort(arr)
                    elif algorithm == "quick":
                        sorted_arr, steps = quicksort(arr)
                    else:
                        message = "Invalid algorithm selected."
                        return render_template("sorting.html", message=message, 
                                             algorithms=algorithm_info, result=None)
                    
                    result = {
                        "original": original,
                        "sorted": sorted_arr,
                        "steps": steps,
                        "algorithm": algorithm,
                        "info": algorithm_info[algorithm]
                    }
                    message = f"Sorted using {algorithm_info[algorithm]['name']}!"
                    
            except ValueError:
                message = "Please enter valid integers only."
    
    return render_template("sorting.html", message=message, 
                         algorithms=algorithm_info, result=result)


# ---------------------------
# Run server
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
