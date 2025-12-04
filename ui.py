import tkinter as tk
import functions

CELL = 50
ROWS = 8
COLS = 12
PARK = (9, 1)

class ShipUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.previewed = False
        root.title("Ship Balancer")

        # log timestamp
        self.session_start = functions.timestamp_now()   
        # list of all log lines
        self.log_entries = []                            
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.log("Program was started.")

        self.canvas = tk.Canvas(
            root,
            width=COLS * CELL,
            height=(ROWS + 1) * CELL,
            bg="white"
        )
        self.canvas.pack(pady=15)
        self.info = tk.Text(root, width=67, height=8, font=("Arial", 12), state="disabled")
        self.info.pack(padx=10, pady=(10,5))

        # begin program with manifest
        self.append_info("Enter a manifest.")

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        #log button
        tk.Button(btn_frame, text="Add Comment",
          command=self.add_comment_popup).grid(row=0, column=2, padx=20)
        
        tk.Button(btn_frame, text="Load Manifest",
                  command=self.controller.load_manifest_file).grid(row=0, column=0, padx=20)

        self.next_btn = tk.Button(btn_frame, text="Enter",
                                  state="disabled",
                                  command=self.controller.next_move)
        self.next_btn.grid(row=0, column=1, padx=20)

    def load_path(self, path):
        self.path = path
        
        self.current_index = 0
        self.phase = "preview"
        path[0].is_first = True
        path[-1].is_last = True

        # write solution to log
        self.log(f"Balance solution found, it will require {len(path)-1} move(s) and {functions.totalTime(path[-1])} minutes.")
        self.append_info(f"A solution has been found! It will take\n"
                            f"{len(path)-1} move(s) and {functions.totalTime(path[-1])} minute(s)\n"
                            f"Hit ENTER to begin\n")

        self.next_btn.config(state="normal")
        self.draw_grid(path[0].grid)
        self.total_moves = len(self.path) - 1
        self.move_counter = 0


    def draw_grid(self, grid, source=None, target=None):
        self.canvas.delete("all")

        for r in range(1, ROWS+1):
            for c in range(1, COLS+1):

                weight, contents = grid[r][c]

                # row 1 at the bottom
                x0 = (c - 1) * CELL
                y0 = (ROWS - r + 1) * CELL   

                x1 = x0 + CELL
                y1 = y0 + CELL

                if c <= COLS // 2:
                    border = "black"
                else:
                    border = "blue"

                # Color
                if contents == "NAN":
                    fill = "black"
                elif (contents == "UNUSED"):
                    fill = "white"
                else:
                    fill = "yellow"

                if source == (r, c):
                    fill = "green"
                elif target == (r, c):
                    fill = "red"
                    

                self.canvas.create_rectangle(x0, y0, x1, y1,
                                             fill=fill,
                                             outline=border,
                                             )
                text=str(contents)
                if len(text) > 6:
                    text = text[:4] + "..."
                if weight > 0 or (contents != "NAN" and contents != "UNUSED"):
                    self.canvas.create_text((x0 + CELL/2),
                                            (y0 + CELL/2),
                                            text=text,
                                            font=("Arial", 12, "bold"),
                                            fill="black")
        park_r, park_c = PARK
        x0 = (park_c - 1) * CELL
        y0 = 0
        x1 = x0 + CELL
        y1 = CELL

        self.canvas.create_rectangle(
            x0, y0, x1, y1,
            fill="grey",
            outline="grey",
            width=1
        )

        self.canvas.create_text(
            (x0 + CELL/2),
            (y0 + CELL/2),
            text="Park",
            font=("Arial", 10, "bold"),
            fill="black"
        )

        # Highlight PARK if it's source/target
        if source == PARK:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="green", outline="black")
        elif target == PARK:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="red", outline="black")

    def highlight_move(self, curr_state, next_state, pos, source_override = None, target_override = None):

        # finding src and target, redrawing grid

        #crane to grid 
        if curr_state == PARK:
            source = PARK
            target = pos
        
        # grid to crane
        elif next_state == PARK:
            source = pos
            target = PARK

        else:
            for r in range(1, ROWS+1):
                for c in range(1, COLS+1):
                    w1, _ = curr_state.grid[r][c]
                    w2, _ = next_state.grid[r][c]

                    if w1 != 0 and w2 == 0:
                        source = (r, c)
                    elif w1 == 0 and w2 != 0:
                        target = (r, c)
        
        if source_override:
            source = source_override
        if target_override:
            target = target_override

        if curr_state != PARK:
            self.draw_grid(curr_state.grid, source, target)
        else:
            self.draw_grid(next_state.grid, source, target)


    def finish(self):
        self.next_btn.config(state="disabled")
        self.clearGrid()  

        self.append_info("Enter a manifest.")
        self.path = []
        self.current_index = 0
        self.foundGoal = None
        self.initialState = None

    def clearGrid(self):
        self.canvas.delete("all")
        self.info.config(state="normal") 
        self.info.delete("1.0", tk.END)
        self.info.config(state="normal") 

    def append_info(self, text):
        self.info.config(state="normal")
        self.info.insert("end", text + "\n")
        self.info.config(state="disabled")
        self.info.see("end")   

    # log stamp
    def log(self, text):
        ts = functions.timestamp_now().strftime("%m %d %Y: %I:%M %p:")  
        entry = f"{ts} {text}"
        self.log_entries.append(entry)
    
    # save log file to desktop
    def write_log_file(self):
        
        import os
        dt = self.session_start
        manifest = self.controller.manifest_name[0:-4]
        fname = f"{manifest}_{dt.strftime('%m_%d_%Y_%I%M')}.txt"
        # self.log(f"Finished a Cycle. Manifest {fname} was written to desktop.")
    

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        path = os.path.join(desktop, fname)

        with open(path, "w") as f:
            for line in self.log_entries:
                f.write(line + "\n")

    def on_close(self):
        self.log("Program was shut down.")
        self.write_log_file()
        self.root.destroy()

    def add_comment_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Add Log Comment")

        tk.Label(win, text="Enter comment:").pack(pady=5)
        entry = tk.Text(win, width=50, height=5)
        entry.pack()

        def save():
            comment = entry.get("1.0", tk.END).strip()
            if comment:
                self.log(f"Comment: {comment}")
            win.destroy()

        tk.Button(win, text="Save", command=save).pack(pady=10)

    


