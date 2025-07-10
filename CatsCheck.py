import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

stations = ["Soup","Carrot","Cabbage","Juice","Corn","Acorn","Broccoli","Barbecue","Lemon","Honey","Wheat",
            "Radish","Pumpkin","Mushrooms","Celery","Lotus Root","Grapes","Sugarcane",
            "Grapes","Sugarcane","Strawberry","Oats","Garlic","Pineapple","Papaya","Sesame",
            "Cheese","Apples","Red Beans","Mangosteen","Asparagus","Potatoes","Avocado",
            "Onion","Peanut","Tomatoes","Olives","Beets","Oranges","Sunflower Seeds","Starfruit",
            "Bamboo Shoot","Basil","Watermelon","Eggplant","Tabasco Peppers","Pomegranate",
            "Sweet Potatoes","Ginseng","Coffee Beans","Buckwheat","Figs","Peaches","Bananas"]

def process_file(filepath, last_station, show_unmatched):
    cutoff_index = stations.index(last_station) + 1
    unlocked = stations[:cutoff_index]

    station_dict = {station: [] for station in unlocked}
    unmatched = []

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 4:
                continue
            name, skill, grade, hearts = map(str.strip, parts)
            try:
                grade = int(grade)
                hearts = int(hearts)
            except:
                continue
            cat = {"name": name, "skill": skill, "grade": grade, "hearts": hearts}
            if skill in station_dict:
                station_dict[skill].append(cat)
            else:
                unmatched.append(cat)

    output = []
    for station in unlocked:
        cats = station_dict[station]
        if cats:
            header = station.upper() if station.lower() in ["soup", "juice", "barbecue"] else station
            output.append(header)
            for c in sorted(cats, key=lambda x: (-x["grade"], -x["hearts"])):
                output.append(f"- {c['name']}, {c['grade']}*, {c['hearts']}")
            output.append("")

    if show_unmatched and unmatched:
        output.append("=== Unmatched Cats ===")
        for c in sorted(unmatched, key=lambda x: -x["hearts"]):
            output.append(f"- {c['name']}, {c['skill']}, {c['grade']}*, {c['hearts']}")

    return "\n".join(output)

def run_gui():
    def select_file():
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            file_var.set(path)

    def run_program():
        path = file_var.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Please select a valid file.")
            return
        station = station_combo.get()
        if not station:
            messagebox.showerror("Error", "Please select the last unlocked station.")
            return
        show_unmatched = unmatched_var.get()
        result = process_file(path, station, show_unmatched)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    root = tk.Tk()
    root.title("Cat Station Sorter")
    root.geometry("700x600")
    root.configure(bg="#FFC5EA")

    file_var = tk.StringVar()
    unmatched_var = tk.BooleanVar()

    def add_label(text):
        lbl = tk.Label(root, text=text, bg="#FFC5EA", font=("Segoe UI", 10, "bold"))
        lbl.pack(padx=10, pady=(10, 2))
        lbl.configure(anchor="center")
        return lbl

    add_label("Select cat list file (.txt):")
    tk.Entry(root, textvariable=file_var, width=80).pack(padx=10, pady=2)
    tk.Button(root, text="Browse", command=select_file).pack(padx=10, pady=2)

    add_label("Select Last Unlocked Station:")
    station_combo = ttk.Combobox(root, values=stations, width=50)
    station_combo.pack(padx=10, pady=5)

    tk.Checkbutton(root, text="Include unmatched cats", variable=unmatched_var, bg="#FFC5EA").pack(padx=10)

    tk.Button(root, text="Run", command=run_program).pack(pady=10)

    output_text = tk.Text(root, wrap="word", font=("Courier New", 10))
    output_text.pack(expand=True, fill="both", padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_gui()