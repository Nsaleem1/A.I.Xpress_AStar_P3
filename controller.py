import tkinter as tk
from tkinter import filedialog, messagebox
import os
from functions import Container
import functions
from ui import PARK

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

        self.fileName = os.path.basename(file_path)  # <-- ADD THIS LINE

        # --- Load containers (your original code) ---
        containers = []
        with open(file_path, "r") as f:
            for line in f:
                parts = [p.strip() for p in line.split(", ")]
                loc = parts[0][1:-1]
                r, c = loc.split(",")
                weight = int(parts[1][1:-1])
                contents = parts[2]
                containers.append(Container((int(r), int(c)), weight, contents, coord=parts[0]))

        # --- Build state ---
        grid = functions.shipGrid(containers)
        left = functions.left(grid)
        right = functions.right(grid)
        goal = functions.reachGoal(grid)

        self.initialState = functions.state(grid, left, right, goal, 0, parent=None)

        # --- Solve ---
        if not functions.edgeCase(self.initialState, containers):
            self.foundGoal = functions.AStar(self.initialState)
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
        ui = self.ui
        path = ui.path
        idx = ui.current_index
        
        curr_state = path[idx]

        # if idx == 0 and not ui.previewed:
        #     # source_override = PARK
        #     next_state = path[idx + 1]
        #     ui.highlight_move(curr_state, next_state, source_override = PARK)
        #     self.ui.info.config(text = f"start from PARK\n" )
        # elif idx == len(path) - 1:

        #     ui.highlight_move(curr_state, next_state, target_override = PARK)
        #     self.ui.info.config(text = f"end at PARK\n" )

        # if idx == 0 and not ui.previewed:
        #     # First move: source is PARK
        #     curr_state = path[0]
        #     next_state = path[0] if len(path) == 1 else path[1]
        #     source_override = PARK
        #     target_override = None
        #     for r in range(1, 9):
        #         for c in range(1, 13):
        #             w1, _ = curr_state.grid[r][c]
        #             w2, _ = next_state.grid[r][c]
        #             if w1 != 0 and w2 == 0:
        #                 target_override = (r, c)
        #                 break
        #         if target_override:
        #             break 
        # elif idx == len(path) - 1:
        #     # Last move: target is PARK
        #     curr_state = path[idx]
        #     next_state = curr_state
        #     target_override = PARK
        #     source_override = None
        #     for r in range(1, 9):
        #         for c in range(1, 13):
        #             w1, _ = path[idx - 1].grid[r][c]
        #             w2, _ = curr_state.grid[r][c]
        #             if w1 == 0 and w2 != 0:
        #                 source_override = (r, c)
        #                 break
        #         if source_override:
        #             break

        # else:
        #     curr_state = path[idx]
        #     next_state = path[idx + 1]
        #     source_override = None
        #     target_override = None


        # curr_state = path[idx]
        if idx == len(path) - 1 and not ui.previewed:
            ui.finish()
            return


        if idx == len(path) - 1 and ui.previewed:
            next_state = curr_state            

        else:
            next_state = path[idx + 1]

        if not ui.previewed:
        # First click: show preview only
            ui.highlight_move(curr_state, next_state)
            ui.previewed = True
            return
        else:
            # Second click: perform move
            ui.draw_grid(next_state.grid)
            ui.current_index += 1
            ui.previewed = False
        
            if ui.current_index == len(path) - 1:
                # Last move has now been executed → show final grid
                # ui.info.config(text="All moves have been completed.\nPress ENTER to finish.")
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                out = os.path.join(desktop, f"{self.fileName[0:-4]}OUTBOUND.txt")
                functions.updateManifest(self.path[-1].grid, out)
                self.ui.info.config(text = f"Done!!\n" 
                                    f"An updated manifest has been written to the desktop as\n"
                                    f"{self.fileName[0:-4]}OUTBOUND.txt\n"
                                    f"Email it to the captain.\n"
                                    f"Hit ENTER when done.")
                return   # DO NOT call finish yet
            
            return
        
        # if self.current_index + 1 >= len(self.path):
        #     desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        #     out = os.path.join(desktop, f"{self.fileName[0:-4]}OUTBOUND.txt")
        #     functions.updateManifest(self.path[-1].grid, out)
        #     messagebox.showinfo("Done", f"An updated manifest has been written to the desktop as\n"
        #                         f"{self.fileName[0:-4]}OUTBOUND.txt\n"
        #                         "Email it to the captain.\n"
        #                         "Hit ENTER when done.")
        #     self.ui.finish()
        #     return
        
        curr_state = self.path[self.current_index]
        #if idx != len(path) - 1:
        next_state = self.path[self.current_index + 1]

        # Get the move string from your existing function (already in correct format)
        move_text = functions.getAction(curr_state.grid, next_state.grid)
        self.ui.info.config(text=f"{move_text}")

        # Draw next grid with highlighted source/target
        self.ui.draw_grid(next_state.grid)

        # Highlight the move
        self.ui.highlight_move(curr_state, next_state)
        self.current_index += 1
        #self.ui.draw_grid(self.path[self.current_index].grid)

if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()

