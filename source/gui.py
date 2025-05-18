import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from source.visualize_1d import (
    draw_1d_canvas, draw_1d_grid, draw_1d_bar_chart,
    draw_1d_spiral
)
from source.visualize_2d import draw_model_2d
from source.database import create_and_fill_db, DB_PATH
import sqlite3


def run_app():
    create_and_fill_db()
    root = tk.Tk()
    root.title("HMM modeling")
    root.geometry("1100x700")

    # Центрирование главного окна
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    root.geometry(f"+{(screen_width//2 - window_width//2)}+{(screen_height//2 - window_height//2)}")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # === ВКЛАДКА 1D ===
    frame_1d = ttk.Frame(notebook)
    notebook.add(frame_1d, text="1D-моделирование")

    params_1d = tk.Frame(frame_1d)
    params_1d.pack(side="left", fill="y", padx=10, pady=10)

    def int_field(label, default):
        tk.Label(params_1d, text=label).pack(anchor="w")
        var = tk.StringVar(value=str(default))
        tk.Entry(params_1d, textvariable=var).pack(fill="x", pady=2)
        return var

    a_var = int_field("Начало (a)", 5)
    d_var = int_field("Шаг (d)", 3)
    n_var_1d = int_field("Количество (n)", 100)
    def regenerate_1d():
        try:
            a = int(a_var.get())
            d = int(d_var.get())
            n = int(n_var_1d.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые значения")
            return
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM numbers WHERE type = '1D'")
        for i in range(n):
            val = a + i * d
            cur.execute("INSERT INTO numbers (value, type) VALUES (?, '1D')", (val,))
        conn.commit()
        conn.close()
        draw_1d_canvas(canvas_1d)

    tk.Button(params_1d, text="Сформировать", command=regenerate_1d).pack(pady=10, fill="x")

    # Кнопка справки для 1D
    def show_1d_help():
        help_win = tk.Toplevel(root)
        help_win.title("Справка по 1D моделям")
        help_win.geometry("600x400")
        help_win.update_idletasks()
        screen_width = help_win.winfo_screenwidth()
        screen_height = help_win.winfo_screenheight()
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (290 // 2)
        help_win.geometry(f"600x290+{x}+{y}")
        help_win.title("Справка по 1D моделям")
        help_text = """
    1D Моделирование - визуализация числовых последовательностей
    Параметры:
    - a: начальное значение
    - d: шаг прогрессии
    - n: количество элементов

    Визуализации:
    1. Градиентная лента - показывает значения в виде цветных вертикальных линий
    2. Замощение - отображает значения в виде цветных прямоугольников в сетке
    3. Столбчатая диаграмма - классическая столбчатая диаграмма значений
    4. Цветовая спираль - визуализация в виде спирали с цветовым кодированием

    Для масштабирования графика спирали удерживайте клавишу Ctrl и прокручивайте колесико мыши
    """
        tk.Label(help_win, text=help_text, justify="left", padx=20, pady=20).pack()
        help_win.transient(root)


    tk.Button(params_1d, text="📘 Справка 1D", command=show_1d_help).pack(pady=5, fill="x")

    canvas_frame_1d = tk.Frame(frame_1d)
    canvas_frame_1d.pack(side="left", fill="both", expand=True, padx=10)
    canvas_1d = tk.Canvas(canvas_frame_1d, bg="white")
    canvas_1d.pack(fill='both', expand=True)


    btns_frame = tk.Frame(canvas_frame_1d)
    btns_frame.pack(pady=5)
    tk.Button(btns_frame, text="Градиентная лента", command=lambda: draw_1d_canvas(canvas_1d)).grid(row=0, column=0, padx=5)
    tk.Button(btns_frame, text="Замощение", command=lambda: draw_1d_grid(canvas_1d)).grid(row=0, column=1, padx=5)
    tk.Button(btns_frame, text="Столбчатая диаграмма", command=lambda: draw_1d_bar_chart(canvas_1d)).grid(row=0, column=2, padx=5)

    def draw_spiral_with_scale():
        try:
            scale_percent = int(100)
            if scale_percent <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительный масштаб в процентах")
            return
        draw_1d_spiral(canvas_1d)

    tk.Button(btns_frame, text="Цветовая спираль", command=draw_spiral_with_scale).grid(row=0, column=3, padx=5)


    # === ВКЛАДКА 2D ===
    frame_2d = ttk.Frame(notebook)
    notebook.add(frame_2d, text="2D-моделирование")

    controls_frame = tk.Frame(frame_2d)
    controls_frame.pack(side="left", fill="y", padx=10, pady=10)

    tk.Label(controls_frame, text="Модель:").pack(anchor="w")
    model_var = tk.StringVar(value="LenNOD")
    model_box = ttk.Combobox(controls_frame, textvariable=model_var,
                             values=["LenNOD", "Ker", "SUM", "MOD"])
    model_box.pack(fill="x", pady=5)

    def float_entry(label_text, default):
        tk.Label(controls_frame, text=label_text).pack(anchor="w")
        var = tk.StringVar(value=str(default))
        tk.Entry(controls_frame, textvariable=var).pack(fill="x", pady=2)
        return var

    ymax_var = float_entry("Ymax=", 10)
    ymin_var = float_entry("Ymin=", 1)
    xmax_var = float_entry("Xmax=", 10)
    xmin_var = float_entry("Xmin=", 1)
    n_var = float_entry("N=", 20)
    aspect_var = float_entry("Aspect=", 1.0)

    show_values = tk.BooleanVar(value=True)
    tk.Checkbutton(controls_frame, text="Показывать значения", variable=show_values).pack(anchor="w")
    show_grid = tk.BooleanVar(value=False)
    tk.Checkbutton(controls_frame, text="Показывать сетку", variable=show_grid).pack(anchor="w")

    canvas_frame = tk.Frame(frame_2d)
    canvas_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    canvas_2d = tk.Canvas(canvas_frame, bg="white", width=700, height=500)
    canvas_2d.grid(row=0, column=0, sticky="nsew")
    vsb = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas_2d.yview)
    vsb.grid(row=0, column=1, sticky="ns")
    hsb = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas_2d.xview)
    hsb.grid(row=1, column=0, sticky="ew")
    canvas_2d.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)

    formula_label = tk.Label(frame_2d, text="HMM = ...", font=("Arial", 12))
    formula_label.pack(pady=2)

    def on_calculate():
        try:
            xmin = float(xmin_var.get())
            xmax = float(xmax_var.get())
            ymin = float(ymin_var.get())
            ymax = float(ymax_var.get())
            n = int(float(n_var.get()))
            aspect = float(aspect_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные параметры")
            return

        model = model_var.get()
        formula_map = {
            "LenNOD": "HMM = lenNOD(x,y)",
            "Ker": "HMM = ker(x*y)",
            "SUM": "HMM = int(x + y)",
            "MOD": "HMM = x % y"
        }
        formula_label.config(text=formula_map.get(model, "HMM = ..."))

        draw_model_2d(
            canvas=canvas_2d,
            xmin=xmin, xmax=xmax,
            ymin=ymin, ymax=ymax,
            n_cells=n, aspect=aspect,
            show_values=show_values.get(),
            show_grid=show_grid.get(),
            model=model
        )

    buttons_frame = tk.Frame(frame_2d)
    buttons_frame.pack(side="bottom", fill="x", pady=10)

    def show_2d_help():
        help_win = tk.Toplevel(root)
        help_win.title("Справка по 2D моделям")
        help_win.geometry("600x400")
        help_win.update_idletasks()
        screen_width = help_win.winfo_screenwidth()
        screen_height = help_win.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (290 // 2)
        help_win.geometry(f"500x290+{x}+{y}")
        help_win.title("Справка по 2D моделям")
        help_text = """
    2D Моделирование - анализ числовых пар

    Доступные модели:
    1. LenNOD - длина алгоритма Евклида для пары чисел (количество шагов)
    2. Ker - ядро числа (рекурсивная сумма цифр произведения чисел)
    3. SUM - сумма двух чисел
    4. MOD - остаток от деления первого числа на второе

    Параметры:
    - Xmin/Xmax - диапазон значений по оси X
    - Ymin/Ymax - диапазон значений по оси Y
    - N - количество ячеек
    - Aspect - соотношение сторон (ширина/высота)
    """
        tk.Label(help_win, text=help_text, justify="left", padx=20, pady=20).pack()
        help_win.transient(root)

    tk.Button(controls_frame, text="📘 Справка 2D", command=show_2d_help).pack(pady=5, fill="x")

    tk.Button(buttons_frame, text="🔄 Расчёт", command=on_calculate).pack(side="left", padx=10)
    tk.Button(buttons_frame, text="❌ Закрыть", command=root.quit).pack(side="right", padx=10)

    # Меню
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    menu_data = tk.Menu(menubar, tearoff=0)


    menu_data.add_separator()
    menu_data.add_command(label="Выход", accelerator="Ctrl+X", command=root.quit)
    menubar.add_cascade(label="Файл", menu=menu_data)

    menu_help = tk.Menu(menubar, tearoff=0)
    menu_help.add_command(
        label="Справка",
        accelerator="F1",
        command=lambda: messagebox.showinfo(
            "Справка",
            "Хромоматематическое моделирование\n\n"
            "Горячие клавиши:\n"
            "  F1         — Справка\n"
            "  Ctrl+F1    — О программе\n"
            "  F2         — Визуализация 1D (столбцы, сетка, спираль, точки)\n"
            "  F5         — Визуализация 2D (анализ Ker и LenNOD)\n"
            "  Esc        — Выход из программы\n\n"
            "Описание:\n"
            "1D — визуализация числовой последовательности (арифметическая прогрессия)\n"
            "2D — анализ числовых пар в координатной сетке (Ker, LenNOD)\n"
            "Выражаю огромную благодарность родителям - Поповой Ольге и Попову Семену "
            "за хорошее воспитание, заботу, поддержку. Еще раз благодарю вас от всего сердца "
            "за вашу веру в меня и вашу неоценимую помощь."
        )
    )

    menu_help.add_command(
        label="О программе",
        accelerator="Ctrl+F1",
        command=lambda: messagebox.showinfo(
            "О программе",
            "Хромоматематическое моделирование\n"
            "Версия 4.0\n\n"
            "Автор: Голубева Е.С.\n"
            "Город: Москва\n"
            "Год: 2025\n\n"
            "Объект 1D:\n"
            "— визуализация чисел по индексам в виде графиков и узоров\n\n"
            "Объект 2D:\n"
            "— анализ пар чисел с математическими моделями\n\n"
            "Модели:\n"
            "— Ker(x * y): рекурсивная сумма цифр произведения\n"
            "— LenNOD(x, y): длина алгоритма Евклида (количество шагов)"
        )
    )
    menubar.add_cascade(label="Справка", menu=menu_help)
    root.bind("<F2>", lambda e: notebook.select(frame_1d))
    root.bind("<F5>", lambda e: notebook.select(frame_2d))
    root.bind("<Escape>", lambda e: root.quit())
    root.bind("<Control-x>", lambda e: root.quit())
    root.bind("<F1>", lambda e: messagebox.showinfo(
        "Справка",
        "Хромоматематическое моделирование\n\n"
        "Горячие клавиши:\n"
        "  F1         — Справка\n"
        "  Ctrl+F1    — О программе\n"
        "  F2         — Визуализация 1D (столбцы, сетка, спираль, точки)\n"
        "  F5         — Визуализация 2D (анализ Ker и LenNOD)\n"
        "  Esc        — Выход из программы\n\n"
        "Описание:\n"
        "1D — визуализация числовой последовательности (арифметическая прогрессия)\n"
        "2D — анализ числовых пар в координатной сетке (Ker, LenNOD)\n"
        "Выражаю огромную благодарность родителям - Поповой Ольге и Попову Семену "
        "за хорошее воспитание, заботу, поддержку. Еще раз благодарю вас от всего сердца "
        "за вашу веру в меня и вашу неоценимую помощь."
    ))

    root.bind("<Control-F1>", lambda e: messagebox.showinfo(
        "О программе",
        "Хромоматематическое моделирование\n"
        "Версия 4.0\n\n"
        "Автор: Голубева Е.С.\n"
        "Город: Москва\n"
        "Год: 2025\n\n"
        "Объект 1D:\n"
        "— визуализация чисел по индексам в виде графиков и узоров\n\n"
        "Объект 2D:\n"
        "— анализ пар чисел с математическими моделями\n\n"
        "Модели:\n"
        "— Ker(x * y): рекурсивная сумма цифр произведения\n"
        "— LenNOD(x, y): длина алгоритма Евклида (количество шагов)"
    ))

    root.mainloop()


