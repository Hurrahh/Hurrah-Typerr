import tkinter as tk
from hurrah_typer import HurrahTyper

__version__ = "1.0.0"

hurrah_typer = HurrahTyper(mode="code")

root = tk.Tk()
root.title("Hurrah Typer")
root.geometry("700x580")
root.resizable(False, False)

tk.Label(root, text="Hurrah Typer", font=("Courier", 30, "bold")).pack(pady=(10, 5))


updates_label = tk.Label(
    root, text=f"v{__version__} - AI-powered typing assistant", cursor="hand2"
)
updates_label.pack()

tk.Label(
    root,
    text="Capture screen and process with AI",
    font=("Arial", 12)
).pack(pady=(10, 20))

mode_frame = tk.Frame(root)
mode_frame.pack(anchor=tk.W, padx=20, pady=10)

tk.Label(mode_frame, text="Mode:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

mode_var = tk.StringVar(value=hurrah_typer.mode)

for mode in hurrah_typer.modes:
    radio = tk.Radiobutton(
        mode_frame,
        text=mode.capitalize(),
        value=mode,
        font=("Arial", 12),
        variable=mode_var,
        command=lambda m=mode: hurrah_typer.set_mode(m),
    )
    radio.pack(side=tk.LEFT, padx=10)

options_frame = tk.Frame(root)
options_frame.pack(anchor=tk.W, padx=20, pady=10)

remove_auto_brackets = tk.BooleanVar(value=hurrah_typer.remove_auto_brackets)
tk.Checkbutton(
    options_frame,
    text="Remove Auto Brackets",
    font=("Arial", 12),
    variable=remove_auto_brackets,
    command=lambda: hurrah_typer.set_remove_auto_brackets(remove_auto_brackets.get()),
).pack(anchor=tk.W)

info_frame = tk.Frame(root)
info_frame.pack(pady=10)

tk.Label(
    info_frame,
    text="Controls: Ctrl = Capture | F8 = Pause/Resume | Alt = Stop",
    font=("Arial", 10),
    fg="gray"
).pack()

running_label = tk.Label(
    root,
    text="Hurrah Typer is running...",
    font=("Courier", 11, "bold"),
    fg="green"
)

is_enabled = tk.StringVar()
is_enabled.set("START")

def toggle():
    if is_enabled.get() == "START":
        hurrah_typer.start()
        is_enabled.set("STOP")
        running_label.pack()
        print("Hurrah Typer is enabled.")
    else:
        hurrah_typer.stop_listener()
        is_enabled.set("START")
        running_label.pack_forget()
        print("Hurrah Typer is disabled.")

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=(10, 10))

tk.Button(
    buttons_frame,
    textvariable=is_enabled,
    font=("Arial", 14, "bold"),
    command=toggle,
    width=15,
    fg="black",
    activebackground="#45a049"
).pack(side=tk.LEFT, padx=5)



description_frame = tk.Frame(root)
description_frame.pack(pady=10)

tk.Label(
    description_frame,
    text="• Code Mode: Captures question & types generated code (partial screen)\n• Quiz Mode: Captures question & shows answer in popup (full screen)",
    font=("Arial", 9),
    fg="gray",
    justify=tk.LEFT
).pack()

try:
    print("Hurrah Typer application started...")
    root.mainloop()
except KeyboardInterrupt:
    pass

hurrah_typer.stop_listener()
print("Hurrah Typer application closed.")


