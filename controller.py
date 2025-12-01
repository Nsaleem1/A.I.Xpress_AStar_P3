# controller.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import functions
from main import Container   # your class

class Controller:
    def __init__(self, root):
        self.root = root
        from ui import ShipUI
        self.ui = ShipUI(root, self)

        self.path = []
        self.current_index = 0
        self.initialState = None
        self.foundGoal = None

    # User clicked "Load Manifest"
    def load_manifest_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Manifest",
            filetypes=[("Text Files", "*.txt")]
        )
        if not file_path:
            return

        # --- Load containers (your original code) ---
        containers = []
        with open(file_path, "r") as f:
            for line in f:
                parts = [p.strip() for p in line.split(", ")]
                loc = parts[0][1:-1]
                r, c = loc.split(",")
                weight = int(parts[1][1:-1])
                contents = parts[2]
                containers.append(Container((int(r), int(c)), weight, contents))

        # --- Build state ---
        grid = functions.shipGrid(containers)
        left = functions.left(grid)
        right = functions.right(grid)
        goal = functions.reachGoal(grid)

        self.initialState = functions.state(grid, left, right, goal, 0, parent=None)

        # --- Solve ---
        if not functions.edgeCase(self.initialState, containers):
            self.foundGoal = functions.AStarOptimal(self.initialState)
        else:
            self.foundGoal = self.initialState

        # --- Build path ---
        self.path = []
        s = self.foundGoal
        while s:
            self.path.append(s)
            s = s.parent
        self.path.reverse()

        self.current_index = 0
        self.ui.load_path(self.path)

    # User clicks "Next Move"
    def next_move(self):
        if self.current_index + 1 >= len(self.path):
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            out = os.path.join(desktop, "UPDATED_MANIFEST.txt")
            functions.updateManifest(self.path[-1].grid, out)
            messagebox.showinfo("Done", f"Finished! Written to:\n{out}")
            self.ui.finish()
            return

        self.current_index += 1
        self.ui.draw_grid(self.path[self.current_index].grid)

if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()

