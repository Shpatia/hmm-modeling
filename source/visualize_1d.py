import sqlite3
import tkinter as tk
import math
from source.database import DB_PATH


def get_1d_values():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT value FROM numbers WHERE type = '1D'")
    values = [row[0] for row in cur.fetchall()]
    conn.close()
    return values


def normalize(value, min_val, max_val):
    return int(255 * (value - min_val) / (max_val - min_val)) if max_val > min_val else 0


def draw_1d_canvas(canvas):
    canvas.delete("all")
    values = get_1d_values()
    if not values:
        return

    w, h = canvas.winfo_width(), canvas.winfo_height()
    min_val, max_val = min(values), max(values)
    step = w / len(values)
    padding_left, padding_bottom = 40, 60  # Увеличен отступ снизу

    def draw_axes_legend():
        # Оси
        canvas.create_line(padding_left, h - padding_bottom, w, h - padding_bottom, fill="black")  # ось X с отступом слева и снизу
        canvas.create_line(padding_left, 0, padding_left, h - padding_bottom, fill="black")      # ось Y с отступом снизу

        # Деления оси Y и горизонтальные линии (пунктир)
        for frac, text in [(0, "0"), (0.5, str(max_val // 2)), (1, str(max_val))]:
            y = h - padding_bottom - frac * (h - padding_bottom)
            canvas.create_line(padding_left - 5, y, padding_left, y, fill="black")  # деление
            canvas.create_text(padding_left - 10, y, text=text, anchor="e", font=("Arial", 8))
            canvas.create_line(padding_left, y, w, y, fill="#cccccc", dash=(2, 4))  # сетка

        # Деления по оси X
        for i in range(len(values)):
            x = padding_left + i * step + step / 2
            if step > 30 or i % max(1, len(values) // 10) == 0:  # рисуем не все, а через равные промежутки
                canvas.create_line(x, h - padding_bottom, x, h - padding_bottom + 5, fill="black")
                canvas.create_text(x, h - padding_bottom + 25, text=str(i), anchor="n", font=("Arial", 8))

    draw_axes_legend()

    # Рисуем линии графика
    for i, val in enumerate(values):
        x = padding_left + i * step + step / 2
        bar_height = (val - min_val) / (max_val - min_val) * (h - padding_bottom)
        norm = normalize(val, min_val, max_val)
        color = f'#{norm:02x}{255 - norm:02x}00'
        canvas.create_line(x, h - padding_bottom, x, h - padding_bottom - bar_height, fill=color, width=2)
        if step > 15:
            canvas.create_text(x, h - padding_bottom - bar_height - 10, text=str(val), font=("Arial", 8), anchor="s")

    canvas.config(scrollregion=canvas.bbox("all"))


# Пример настройки прокрутки
def create_scrollable_canvas(root):
    frame = tk.Frame(root)
    hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    canvas = tk.Canvas(frame, xscrollcommand=hbar.set, yscrollcommand=vbar.set, width=600, height=300)

    def on_mousewheel(event):
        if event.delta > 0:
            spiral_state["scale"] *= 1.1
        else:
            spiral_state["scale"] /= 1.1
        draw_1d_spiral(canvas, scale=spiral_state["scale"])

    canvas.bind("<MouseWheel>", on_mousewheel)
    spiral_state = {"scale": 1.0}
    hbar.config(command=canvas.xview)
    vbar.config(command=canvas.yview)

    canvas.grid(row=0, column=0, sticky="nsew")
    hbar.grid(row=1, column=0, sticky="ew")
    vbar.grid(row=0, column=1, sticky="ns")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    return frame, canvas


def draw_1d_grid(canvas):
    canvas.delete("all")
    values = get_1d_values()
    if not values:
        return

    padding_left, padding_bottom = 40, 60  # увеличен отступ снизу
    w, h = canvas.winfo_width() - padding_left, canvas.winfo_height() - padding_bottom

    cols = int(math.sqrt(len(values)))
    rows = (len(values) + cols - 1) // cols
    cell_w, cell_h = w / cols, h / rows
    min_val, max_val = min(values), max(values)

    # Оси
    canvas.create_line(padding_left, 0, padding_left, h, fill="black")
    canvas.create_line(padding_left, h, padding_left + w, h, fill="black")

    # Горизонтальные пунктирные линии и подписи по Y (значения)
    for r in range(rows + 1):
        y = h - r * cell_h
        val = min_val + (max_val - min_val) * r / rows
        canvas.create_line(padding_left, y, padding_left + w, y, fill="#cccccc", dash=(2, 4))
        canvas.create_text(padding_left - 5, y, text=f"{val:.1f}", anchor="e", font=("Arial", 8))

    # Вертикальные деления и подписи по X (номера колонок)
    for c in range(cols + 1):
        x = padding_left + c * cell_w
        if c % max(1, cols // 10) == 0:
            canvas.create_line(x, h, x, h + 5, fill="black")
            canvas.create_text(x, h + 25, text=str(c), anchor="n", font=("Arial", 8))

    for i, val in enumerate(values):
        row, col = i // cols, i % cols
        x1 = padding_left + col * cell_w
        y1 = h - (row + 1) * cell_h
        x2 = x1 + cell_w
        y2 = y1 + cell_h

        norm = normalize(val, min_val, max_val)
        color = f'#{norm:02x}00{255 - norm:02x}'
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        if cell_w > 15 and cell_h > 12:
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(val), font=("Arial", 8))
    canvas.config(scrollregion=canvas.bbox("all"))


def draw_1d_bar_chart(canvas):
    canvas.delete("all")
    values = get_1d_values()
    if not values:
        return

    padding_left, padding_bottom = 40, 60  # увеличен отступ снизу
    w, h = canvas.winfo_width() - padding_left, canvas.winfo_height() - padding_bottom
    bar_w = w / len(values)
    min_val, max_val = min(values), max(values)

    # Оси
    canvas.create_line(padding_left, 0, padding_left, h, fill="black")
    canvas.create_line(padding_left, h, padding_left + w, h, fill="black")

    # Горизонтальные пунктирные линии с подписями
    for i in range(5):
        y = h - i * h / 4
        val = min_val + (max_val - min_val) * i / 4
        canvas.create_line(padding_left, y, padding_left + w, y, fill="#cccccc", dash=(2, 4))
        canvas.create_text(padding_left - 5, y, text=f"{val:.1f}", anchor="e", font=("Arial", 8))

    # Вертикальные деления по X
    for i in range(len(values)):
        x = padding_left + i * bar_w + bar_w / 2
        if bar_w > 30 or i % max(1, len(values) // 10) == 0:
            canvas.create_line(x, h, x, h + 5, fill="black")
            canvas.create_text(x, h + 25, text=str(i), anchor="n", font=("Arial", 8))

    for i, val in enumerate(values):
        x1 = padding_left + i * bar_w
        bar_h = (val / max_val) * h
        y1 = h - bar_h
        x2 = x1 + bar_w - 1
        y2 = h
        norm = normalize(val, min_val, max_val)
        color = f'#00{norm:02x}{255 - norm:02x}'
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        if bar_w > 15:
            canvas.create_text((x1 + x2) / 2, y1 - 8, text=str(val), font=("Arial", 8), anchor="s")

    canvas.config(scrollregion=canvas.bbox("all"))


def draw_1d_spiral(canvas):
    if not hasattr(canvas, "scale_factor"):
        canvas.scale_factor = 1.0

    def on_mousewheel(event):
        # Масштабируем только если Ctrl зажат
        if (event.state & 0x4) != 0:  # проверяем Ctrl (bitmask)
            if event.delta > 0:
                canvas.scale_factor *= 1.1
            else:
                canvas.scale_factor /= 1.1
            draw_1d_spiral(canvas)  # обновляем отрисовку
            return "break"  # предотвращаем прокрутку страницы/канваса

    canvas.delete("all")
    values = get_1d_values()
    if not values:
        return

    canvas.bind("<MouseWheel>", on_mousewheel)

    padding = 60
    w, h = canvas.winfo_width() - 2 * padding, canvas.winfo_height() - 2 * padding
    center_x = padding + w // 2
    center_y = padding + h // 2
    spacing = 5 * canvas.scale_factor
    angle_step = 0.3
    max_points = len(values)

    canvas.create_line(center_x, padding, center_x, padding + h, fill="black")
    canvas.create_line(padding, center_y, padding + w, center_y, fill="black")

    for i in range(1, 6):
        r = i * spacing * 20
        canvas.create_oval(center_x - r, center_y - r, center_x + r, center_y + r, outline="#cccccc", dash=(2, 4))

    points = []
    min_val, max_val = min(values), max(values)

    for i in range(max_points):
        angle = i * angle_step
        radius = spacing * angle
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))

    r = 3 * canvas.scale_factor
    for i, (x, y) in enumerate(points):
        val = values[i]
        color_val = normalize(val, min_val, max_val)
        color = f"#{color_val:02x}00{255 - color_val:02x}"
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")

    canvas.config(scrollregion=canvas.bbox("all"))

