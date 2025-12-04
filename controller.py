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
        self.manifest_name = None

    # User clicked "Load Manifest"
    def load_manifest_file(self):

        # write to log
        # self.ui.log("Program was started.")
        
        file_path = filedialog.askopenfilename(
            title="Select Manifest",
            filetypes=[("Text Files", "*.txt")]
        )
        if not file_path:
            return

        self.manifest_name = os.path.basename(file_path)

        # Load containers 
        containers = []
        with open(file_path, "r") as f:
            for line in f:
                parts = [p.strip() for p in line.split(", ")]
                loc = parts[0][1:-1]
                r, c = loc.split(",")
                weight = int(parts[1][1:-1])
                contents = parts[2]
                containers.append(Container((int(r), int(c)), weight, contents))
        
        #count how many containers 
        count = 0
        weightCount = 0
        for container in containers:
            if (container.contents != "NAN" and container.contents != "UNUSED"):
                count = count + 1
            if container.weight > 0:
                weightCount = weightCount + 1

        # create initial state
        grid = functions.shipGrid(containers)
        left = functions.left(grid)
        right = functions.right(grid)
        goal = functions.reachGoal(grid)
        self.initialState = functions.state(grid, left, right, goal, 0, parent=None)

        # write to log file  
        self.ui.log(f"Manifest {self.manifest_name} is opened, there are {count} container(s) on the ship.")
        self.ui.append_info(f"{self.manifest_name[0:-4]} has {count} container(s)\n"
                    "Computing a Solution...\n")
        self.ui.root.update_idletasks()

        # solving using AStar
        if not functions.edgeCase(self.initialState, containers) and weightCount != 1:
            self.foundGoal = functions.AStar(self.initialState)
        else:
            self.foundGoal = self.initialState
            self.ui.log("Zero moves. Ship is already balanced.")
            self.ui.append_info("Done! Ship is already balanced!")

            # Draw the empty grid
            self.ui.draw_grid(self.initialState.grid)

            # Write outbound manifest automatically
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            out = os.path.join(desktop, f"{self.manifest_name[0:-4]}.txt")
            functions.updateManifest(self.initialState.grid, out)

            # Log writing the manifest
            self.ui.log(f"Finished a Cycle. Manifest {self.manifest_name[0:-4]}OUTBOUND.txt was written to desktop.")

            # Tell the user
            self.ui.append_info(
                f"\nAn updated manifest has been written to the desktop as\n"
                f"{self.manifest_name[0:-4]}OUTBOUND.txt\n"
                f"Email it to the captain.\n"
                f"Hit ENTER when done."
            )

            self.path = [self.initialState]  
            self.ui.path = self.path
            self.ui.current_index = 0
            self.ui.total_moves = 0
            self.ui.move_counter = 0

            # Allow the user to press ENTER to return to default screen
            self.ui.next_btn.config(state="normal")
            
            return

        # build path 
        self.path = []
        s = self.foundGoal

        #add grid -> crane as path, append goal state twice
        self.path.append(s)
        
        while s:
            self.path.append(s)
            s = s.parent
        
        #add crane --> grid, append initial state twice
        self.path.append(self.initialState)

        self.path.reverse()

        self.current_index = 0
        self.ui.load_path(self.path)

    # User clicks "Next Move"
    def next_move(self):

        ui = self.ui
        path = ui.path
        idx = ui.current_index
        curr_state = path[idx]

        # if on last state, delete everything
        if idx == len(path) - 1 and not ui.previewed:
            ui.finish()
            return
        
        # on last state, and need to perform move
        if idx == len(path) - 1 and ui.previewed:
            next_state = curr_state    

        # not on the last state
        else:
            next_state = path[idx + 1]

        # highlighting, previewing the moves
        if not ui.previewed:
            
            #first state (crane to grid)
            if idx == 0:
                time, _, pos = functions.craneToGrid(path[1].grid, path[2].grid)
                ui.highlight_move(PARK, next_state, pos)
                ui.previewed = True
                ui.move_counter += 1
                move_text = f"Move Crane from PARK to [{pos[0]:02d}, {pos[1]:02d}], {time} minute(s)"
                formatted = f"{ui.move_counter} of {ui.total_moves}: {move_text}"
                self.ui.append_info(formatted)
                self.ui.log(formatted)

            #last state (grid to crane)
            elif idx == len(path) - 2:
                time, moveContainer, pos = functions.gridToCrane(path[-3].grid, path[-2].grid)
                ui.highlight_move(curr_state, PARK, pos)
                ui.previewed = True
                ui.move_counter += 1
                move_text = f"Move Crane from [{pos[0]:02d}, {pos[1]:02d}] to PARK, {time} minute(s)"
                formatted = f"{ui.move_counter} of {ui.total_moves}: {move_text}"
                self.ui.append_info(formatted)
                self.ui.log(formatted)

            else:
                ui.highlight_move(curr_state, next_state, (0,0))
                ui.previewed = True
                ui.move_counter += 1
                move_text = functions.getAction(curr_state.grid, next_state.grid)
                formatted = f"{ui.move_counter} of {ui.total_moves}: {move_text}"
                self.ui.append_info(formatted)
                self.ui.log(formatted)
                
            return
        
        # not on last state, perform move
        else:

            ui.draw_grid(next_state.grid)
            ui.current_index += 1
            ui.previewed = False
            
            if ui.current_index == len(path) - 1:
                # last move --> final grid 
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                out = os.path.join(desktop, f"{self.manifest_name[0:-4]}.txt")
                functions.updateManifest(self.path[-1].grid, out)
                self.ui.log(f"Finished a Cycle. Manifest {f"{self.manifest_name[0:-4]}OUTBOUND.txt"} was written to desktop.")
                self.ui.append_info(f"\nDone!!\n" 
                                    f"An updated manifest has been written to the desktop as\n"
                                    f"{self.manifest_name[0:-4]}OUTBOUND.txt\n"
                                    f"Email it to the captain.\n"
                                    f"Hit ENTER when done.")
                return   
            return

if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()

