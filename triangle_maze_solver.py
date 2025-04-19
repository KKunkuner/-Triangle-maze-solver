import tkinter as tk

class TriangleMazeSolver:
    def __init__(self, root):
        self.root = root
        self.dot_radius = 10
        self.canvas = tk.Canvas(root, width=800, height=800, bg='white')
        self.canvas.pack()
        
        self.input_frame = tk.Frame(root)
        self.input_frame.pack()

        tk.Label(self.input_frame, text="行数:").pack(side=tk.LEFT)
        self.rows_entry = tk.Entry(self.input_frame, width=5)
        self.rows_entry.pack(side=tk.LEFT)
        tk.Button(self.input_frame, text="确定", command=self.setup_triangle).pack(side=tk.LEFT)

        self.solve_button = tk.Button(root, text="显示路径", command=self.solve_and_draw_path, state=tk.DISABLED)
        self.solve_button.pack()

        self.reset_button = tk.Button(root, text="重置", command=self.reset, state=tk.DISABLED)
        self.reset_button.pack()

    def setup_triangle(self):
        self.canvas.delete("all")
        self.rows = int(self.rows_entry.get())
        self.is_red = [[0]*(i+1) for i in range(self.rows)]
        self.circles = [[None]*(i+1) for i in range(self.rows)]
        self.positions = [[(0,0)]*(i+1) for i in range(self.rows)]
        self.path_lines = []
        self.draw_triangle()
        self.canvas.bind("<Button-1>", self.toggle_red)
        self.solve_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

    def draw_triangle(self):
        spacing = 40
        center_x = 400
        for i in range(self.rows):
            start_x = center_x - i * spacing // 2
            for j in range(i+1):
                x = start_x + j * spacing
                y = 40 + i * spacing
                self.positions[i][j] = (x, y)
                circle = self.canvas.create_oval(
                    x - self.dot_radius, y - self.dot_radius,
                    x + self.dot_radius, y + self.dot_radius,
                    fill='black'
                )
                self.circles[i][j] = circle

    def toggle_red(self, event):
        for i in range(self.rows):
            for j in range(i+1):
                x, y = self.positions[i][j]
                if (x - event.x)**2 + (y - event.y)**2 <= self.dot_radius**2:
                    self.is_red[i][j] = 1 - self.is_red[i][j]
                    color = 'red' if self.is_red[i][j] else 'black'
                    self.canvas.itemconfig(self.circles[i][j], fill=color)

    def solve_and_draw_path(self):
        dp = [[0]*(i+1) for i in range(self.rows)]
        path = [[-1]*(i+1) for i in range(self.rows)]

        dp[0][0] = self.is_red[0][0]

        for i in range(1, self.rows):
            for j in range(i+1):
                left = dp[i-1][j-1] if j > 0 else -1
                right = dp[i-1][j] if j < i else -1
                if left > right:
                    dp[i][j] = left + self.is_red[i][j]
                    path[i][j] = j - 1
                else:
                    dp[i][j] = right + self.is_red[i][j]
                    path[i][j] = j

        # 回溯路径
        last_row = dp[-1]
        j = last_row.index(max(last_row))
        route = []
        for i in reversed(range(self.rows)):
            route.append((i, j))
            j = path[i][j]
        route.reverse()

        # 画路径线条
        for k in range(len(route)-1):
            i1, j1 = route[k]
            i2, j2 = route[k+1]
            x1, y1 = self.positions[i1][j1]
            x2, y2 = self.positions[i2][j2]
            line = self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)
            self.path_lines.append(line)

    def reset(self):
        # 还原所有点为黑色
        for i in range(self.rows):
            for j in range(i+1):
                self.is_red[i][j] = 0
                self.canvas.itemconfig(self.circles[i][j], fill='black')
        # 删除所有蓝色路径线
        for line in self.path_lines:
            self.canvas.delete(line)
        self.path_lines.clear()


# 启动界面
if __name__ == "__main__":
    root = tk.Tk()
    root.title("三角迷阵solver")
    app = TriangleMazeSolver(root)
    root.mainloop()
