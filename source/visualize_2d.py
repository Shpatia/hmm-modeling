from source.hmm import len_nod, ker, hmm_sum, hmm_mod

def draw_model_2d(canvas, xmin, xmax, ymin, ymax, n_cells, aspect=1.0,
                  show_values=True, show_grid=False, model="LenNOD"):
    canvas.delete("all")
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    cols = int(n_cells)
    rows = int(n_cells * aspect)
    cell_w = w / cols
    cell_h = h / rows

    # Модель выбора функции
    func_map = {
        "LenNOD": lambda x, y: len_nod(int(x), int(y)),
        "Ker": lambda x, y: ker(int(x) * int(y)),
        "SUM": lambda x, y: hmm_sum(x, y),
        "MOD": lambda x, y: hmm_mod(int(x), int(y))
    }
    func = func_map.get(model, lambda x, y: 0)

    values = []
    for j in range(rows):
        y = ymin + j * (ymax - ymin) / rows
        row = []
        for i in range(cols):
            x = xmin + i * (xmax - xmin) / cols
            row.append(func(x, y))
        values.append(row)

    flat = [v for row in values for v in row]
    min_val, max_val = min(flat), max(flat)

    for j in range(rows):
        for i in range(cols):
            val = values[j][i]
            norm = (val - min_val) / (max_val - min_val) if max_val > min_val else 0
            r = int(255 * norm)
            g = int(255 * (1 - norm))
            color = f'#{r:02x}{g:02x}00'

            x1 = i * cell_w
            y1 = j * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black" if show_grid else "")

            if show_values and cell_w > 12 and cell_h > 12:
                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(val), fill="black", font=("Arial", 8))

    canvas.config(scrollregion=canvas.bbox("all"))
