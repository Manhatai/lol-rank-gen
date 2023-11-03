import tkinter as tk

def block_input():
    entry_widget.configure(state='disabled')

def unblock_input():
    entry_widget.configure(state='normal')

app = tk.Tk()
app.title("Block Input Example")

entry_widget = tk.Entry(app)
entry_widget.pack()

block_button = tk.Button(app, text="Block Input", command=block_input)
block_button.pack()

unblock_button = tk.Button(app, text="Unblock Input", command=unblock_input)
unblock_button.pack()

app.mainloop()