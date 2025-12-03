# ui.py
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
        ##
        # self.current_index = 0
        # self.phase = "preview"
        self.previewed = False
        ##
        root.title("Ship Balancer")

        # log stuff 
        self.session_start = functions.timestamp_now()   # store start timestamp

        self.log_entries = []                            # list of all log lines
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        #
        self.canvas = tk.Canvas(
            root,
            width=COLS * CELL,
            height=(ROWS + 1) * CELL,
            bg="white"
        )
        self.canvas.pack(pady=15)

        # self.info = tk.Label(root, text="Enter a manifest.", font=("Arial", 14))
        # self.info.pack()
        self.info = tk.Text(root, width=67, height=8, font=("Arial", 12), state="disabled")
        self.info.pack(padx=10, pady=(10,5))

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        #log stuff 
        tk.Button(btn_frame, text="Add Comment",
          command=self.add_comment_popup).grid(row=0, column=2, padx=20)
        ##

        tk.Button(btn_frame, text="Load Manifest",
                  command=self.controller.load_manifest_file).grid(row=0, column=0, padx=20)

        self.next_btn = tk.Button(btn_frame, text="Enter",
                                  state="disabled",
                                  command=self.controller.next_move)
        self.next_btn.grid(row=0, column=1, padx=20)

    def load_path(self, path):
        self.path = path
        #
        self.current_index = 0
        self.phase = "preview"
        path[0].is_first = True
        path[-1].is_last = True
        # self.info.config(text=f"A solution has been found! It will take\n"
        #                  f"{len(path)-1} move(s) and {path[-1].time} minute(s)\n"
        #                  f"Hit ENTER to begin")
        ## write to log
        self.log(f"Balance solution found, it will require {len(path)-1} move(s) and {path[-1].time} minutes.")
        ##
        self.append_info(f"A solution has been found! It will take\n"
                            f"{len(path)-1} move(s) and {path[-1].time} minute(s)\n"
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

                # CORRECT ORIENTATION FOR YOUR GRID:
                x0 = (c - 1) * CELL
                y0 = (ROWS - r + 1) * CELL    # row 1 bottom, row 8 top

                x1 = x0 + CELL
                y1 = y0 + CELL

                if c <= COLS // 2:
                    border = "black"
                else:
                    border = "blue"

                # Color
                if contents == "NAN":
                    fill = "black"
                elif weight == 0:
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
                if weight > 0:
                    self.canvas.create_text((x0 + CELL/2),
                                            (y0 + CELL/2),
                                            # text=str(contents),
                                            text=text,
                                            font=("Arial", 12, "bold"),
                                            fill="black")
        park_r, park_c = PARK
        x0 = (park_c - 1) * CELL
        #y0 = ROWS * CELL       # directly above row 8
        y0 = 0
        x1 = x0 + CELL
        #y1 = y0 + CELL
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

    def highlight_move(self, curr_state, next_state, source_override = None, target_override = None):
        """Find source and target for next move and redraw grid with colors."""
        # source = target = None
        for r in range(1, ROWS+1):
            for c in range(1, COLS+1):
                w1, _ = curr_state.grid[r][c]
                w2, _ = next_state.grid[r][c]

                if w1 != 0 and w2 == 0:
                    source = (r, c)
                elif w1 == 0 and w2 != 0:
                    target = (r, c)
        
    #     if getattr(curr_state, "is_first", False) and source is None:
    #         source = PARK

    # # LAST MOVE ends at park
    #     if getattr(next_state, "is_last", False) and target is None:
    #         target = PARK
        
        if source_override:
            source = source_override
        if target_override:
            target = target_override
        #move_text = functions.getAction(curr_state.grid, next_state.grid)
        #self.append_info(f"Next move: {move_text}")
        self.draw_grid(curr_state.grid, source, target)


    def finish(self):
        self.next_btn.config(state="disabled")
        self.clearGrid()  # <-- you should implement this in your UI class

        self.append_info("Enter a manifest.")
        self.path = []
        self.current_index = 0
        self.foundGoal = None
        self.initialState = None
        #self.manifest_name = None

    def clearGrid(self):
        self.canvas.delete("all")
        self.info.config(state="normal") 
        self.info.delete("1.0", tk.END)
        self.info.config(state="normal") 

    def append_info(self, text):
        self.info.config(state="normal")
        self.info.insert("end", text + "\n")
        self.info.config(state="disabled")
        self.info.see("end")   # auto-scroll

    ## log stuff
    def log(self, text):
        """Add a timestamped event to the session log."""
        ts = functions.timestamp_now().strftime("%m %d %Y: %I%M")  # uniform format
        entry = f"{ts} {text}"
        self.log_entries.append(entry)
    
    def write_log_file(self):
        """Write final log to desktop when program shuts down."""
        import os
        
        dt = self.session_start
        
        manifest = self.controller.manifest_name[0:-4]

        fname = f"{manifest}_{dt.strftime('%m_%d_%Y_%I%M')}.txt"

        ## write to log
        self.log(f"Finished a Cycle. Manifest {fname} was written to desktop.")
        # 

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
                self.log(comment)
                # self.append_info(f"NOTE logged: {comment}")
            win.destroy()

        tk.Button(win, text="Save", command=save).pack(pady=10)

    ##



