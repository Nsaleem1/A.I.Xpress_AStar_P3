# ui.py
import tkinter as tk

CELL = 50
ROWS = 8
COLS = 12

class ShipUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        root.title("Ship Balancer")

        self.canvas = tk.Canvas(
            root,
            width=COLS * CELL,
            height=ROWS * CELL,
            bg="white"
        )
        self.canvas.pack(pady=15)

        self.info = tk.Label(root, text="Load a manifest.", font=("Arial", 14))
        self.info.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Load Manifest",
                  command=self.controller.load_manifest_file).grid(row=0, column=0, padx=20)

        self.next_btn = tk.Button(btn_frame, text="Next Move",
                                  state="disabled",
                                  command=self.controller.next_move)
        self.next_btn.grid(row=0, column=1, padx=20)

    def load_path(self, path):
        self.path = path
        self.info.config(text=f"Loaded – {len(path)-1} moves.")
        self.next_btn.config(state="normal")
        self.draw_grid(path[0].grid)

    def draw_grid(self, grid):
        self.canvas.delete("all")

        for r in range(1, ROWS+1):
            for c in range(1, COLS+1):

                weight, contents = grid[r][c]

                # CORRECT ORIENTATION FOR YOUR GRID:
                x0 = (c - 1) * CELL
                y0 = (ROWS - r) * CELL    # row 1 bottom, row 8 top

                x1 = x0 + CELL
                y1 = y0 + CELL

                # Color
                if contents == "NAN":
                    color = "black"
                elif weight == 0:
                    color = "white"
                else:
                    color = "green"

                self.canvas.create_rectangle(x0, y0, x1, y1,
                                             fill=color,
                                             outline="gray15")

                if weight > 0:
                    self.canvas.create_text((x0 + CELL/2),
                                            (y0 + CELL/2),
                                            text=str(weight),
                                            font=("Arial", 12, "bold"))

    def finish(self):
        self.next_btn.config(state="disabled")
        self.info.config(text="Finished – manifest saved.")
