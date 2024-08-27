import tkinter as tk
from tkinter import colorchooser, messagebox
import random
import os
import datetime
import socket

# Global reference to desktop for changing background color
desktop = None

# Function to handle terminal commands
def handle_command(entry, output):
    command = entry.get().strip()
    entry.delete(0, tk.END)
    
    if command.startswith("Calculator"):
        open_calculator()
        output.configure(state='normal')
        output.insert(tk.END, "Opening Calculator...\n")
        output.configure(state='disabled')
    elif command.startswith("log"):
        output.configure(state='normal')
        output.insert(tk.END, f"Log: {command[4:]}\n")
        output.configure(state='disabled')
    elif command.startswith("KRNL install"):
        output.configure(state='normal')
        output.insert(tk.END, f"Installing {command[13:]}...\n")
        output.configure(state='disabled')
    elif command == "Restart":
        output.configure(state='normal')
        output.insert(tk.END, "Restarting...\n")
        output.configure(state='disabled')
        # Implement restart logic here
    elif command == "Shutdown":
        output.configure(state='normal')
        output.insert(tk.END, "Shutting down...\n")
        output.configure(state='disabled')
        desktop.quit()
    elif command == "ResetGUI":
        output.configure(state='normal')
        output.insert(tk.END, "Resetting GUI...\n")
        output.configure(state='disabled')
        # Implement GUI reset logic here
    elif command == "update":
        output.configure(state='normal')
        output.insert(tk.END, "Updating system...\n")
        output.configure(state='disabled')
        # Implement update logic here
    elif command == "clear":
        output.configure(state='normal')
        output.delete(1.0, tk.END)
        output.configure(state='disabled')
    elif command == "help":
        output.configure(state='normal')
        output.insert(tk.END, "Available commands: Calculator, log, KRNL install <text>, Restart, Shutdown, ResetGUI, update, clear, help, Print(\"<text>\"), RandomNumber, Date, Weather <location>, ListFiles, Ping <host>\n")
        output.configure(state='disabled')
    elif command.startswith("Print(") and command.endswith(")"):
        output.configure(state='normal')
        output.insert(tk.END, f"{command[6:-1]}\n")
        output.configure(state='disabled')
    elif command == "RandomNumber":
        output.configure(state='normal')
        output.insert(tk.END, f"Random Number: {random.randint(1, 500)}\n")
        output.configure(state='disabled')
    elif command == "Date":
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output.configure(state='normal')
        output.insert(tk.END, f"Current Date and Time: {now}\n")
        output.configure(state='disabled')
    elif command.startswith("Weather "):
        location = command[8:].strip()
        # Mock-up weather response
        output.configure(state='normal')
        output.insert(tk.END, f"Weather at {location}: Sunny, 25°C\n")
        output.configure(state='disabled')
    elif command == "ListFiles":
        files = os.listdir('.')
        output.configure(state='normal')
        output.insert(tk.END, "Files in current directory:\n" + "\n".join(files) + "\n")
        output.configure(state='disabled')
    elif command.startswith("Ping "):
        host = command[5:].strip()
        try:
            response = socket.gethostbyname(host)
            output.configure(state='normal')
            output.insert(tk.END, f"Ping to {host} successful. IP address: {response}\n")
            output.configure(state='disabled')
        except socket.error:
            output.configure(state='normal')
            output.insert(tk.END, f"Ping to {host} failed.\n")
            output.configure(state='disabled')
    elif command.startswith("Help "):
        specific_command = command[5:].strip()
        help_text = {
            "Calculator": "Opens the calculator application.",
            "log": "Logs the provided message.",
            "KRNL install <text>": "Installs the specified kernel.",
            "Restart": "Restarts the system.",
            "Shutdown": "Shuts down the system.",
            "ResetGUI": "Resets the graphical user interface.",
            "update": "Updates the system.",
            "clear": "Clears the terminal output.",
            "Print(\"<text>\")": "Prints the specified text.",
            "RandomNumber": "Generates a random number between 1 and 500.",
            "Date": "Displays the current date and time.",
            "Weather <location>": "Displays weather information for the specified location.",
            "ListFiles": "Lists the files in the current directory.",
            "Ping <host>": "Pings the specified host.",
        }
        output.configure(state='normal')
        output.insert(tk.END, help_text.get(specific_command, "No help available for this command.\n"))
        output.configure(state='disabled')
    else:
        output.configure(state='normal')
        output.insert(tk.END, "Unknown command. Type 'help' for a list of commands.\n")
        output.configure(state='disabled')

# Function to open the terminal window
def open_terminal(fullscreen=False, readonly=False):
    terminal = tk.Toplevel()
    terminal.title("KernelOS Terminal")
    if fullscreen:
        terminal.attributes('-fullscreen', True)
    else:
        terminal.geometry("600x400")
    terminal.configure(bg='black')
    terminal.attributes('-topmost', True)

    output = tk.Text(terminal, bg='black', fg='white', insertbackground='white', state='disabled')
    output.pack(fill="both", expand=True)
    
    if readonly:
        output.configure(state='normal')
        output.insert(tk.END, "Reading files...\nLoading GUI...\nLoading files...\nLoading Main.core\nHello world v0.2\n")
        output.configure(state='disabled')
    else:
        entry = tk.Entry(terminal, bg='black', fg='white', insertbackground='white')
        entry.pack(fill="x")
        entry.bind("<Return>", lambda event: handle_command(entry, output))

def open_text_editor(initial_text=""):
    editor = tk.Toplevel()
    editor.title("KernelOS Text Editor")
    editor.geometry("400x300")
    editor.attributes('-topmost', True)
    
    text_area = tk.Text(editor)
    text_area.pack(fill="both", expand=True)
    text_area.insert(tk.END, initial_text)

def open_calculator():
    calc = tk.Toplevel()
    calc.title("KernelOS Calculator")
    calc.geometry("250x300")
    calc.attributes('-topmost', True)
    
    # Simple calculator UI
    entry = tk.Entry(calc, width=16, font=('Arial', 24), bd=8, insertwidth=4, justify='right')
    entry.grid(row=0, column=0, columnspan=4)
    
    # Calculator buttons
    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        'C', '0', '=', '+'
    ]
    
    row, col = 1, 0
    for button in buttons:
        action = lambda x=button: on_calculator_click(x, entry)
        tk.Button(calc, text=button, padx=20, pady=20, command=action).grid(row=row, column=col)
        col += 1
        if col > 3:
            col = 0
            row += 1

def on_calculator_click(button, entry):
    if button == 'C':
        entry.delete(0, tk.END)
    elif button == '=':
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    else:
        entry.insert(tk.END, button)

def open_files():
    files_app = tk.Toplevel()
    files_app.title("KernelOS Files")
    files_app.geometry("300x200")
    files_app.attributes('-topmost', True)

    def open_file(file_type):
        if file_type == "Test1":
            open_text_editor("Test1")
        else:
            open_terminal()

    # Create buttons for different file types
    test1_button = tk.Button(files_app, text="Test1", command=lambda: open_file("Test1"))
    test1_button.pack(pady=5)

    loader_button = tk.Button(files_app, text="Loader", command=lambda: open_file("Loader"))
    loader_button.pack(pady=5)

    cursor_button = tk.Button(files_app, text="Cursor", command=lambda: open_file("Cursor"))
    cursor_button.pack(pady=5)

    main_button = tk.Button(files_app, text="Main", command=lambda: open_file("Main"))
    main_button.pack(pady=5)

    main_os_loader_button = tk.Button(files_app, text="MainOSLoader", command=lambda: open_terminal(readonly=True))
    main_os_loader_button.pack(pady=5)

def open_main_console():
    main_console = tk.Toplevel()
    main_console.title("KernelOS MainConsole")
    main_console.geometry("600x400")
    main_console.attributes('-topmost', True)
    
    # Create a text area for the MainConsole with block cursor effect
    text_area = tk.Text(main_console, bg='black', fg='green', insertbackground='green', font=('Courier', 12), blockcursor=True)
    text_area.pack(fill="both", expand=True)
    
    # Define tags for different colors
    text_area.tag_configure("dollar", foreground="purple")
    text_area.tag_configure("brackets", foreground="yellow")
    text_area.tag_configure("numbers", foreground="blue")
    text_area.tag_configure("angle", foreground="brown")
    
    # Function to apply syntax highlighting
    def highlight_syntax():
        text_area.mark_set("range_start", "1.0")
        text_area.mark_set("range_end", "1.0")
        
        while True:
            index = text_area.search(r'\S', text_area.index("range_end"), stopindex=tk.END, nocase=True, regexp=True)
            if not index:
                break
            text_area.mark_set("range_start", index)
            text_area.mark_set("range_end", f"{index}+1c")
            
            char = text_area.get("range_start", "range_end")
            if char == '$':
                text_area.tag_add("dollar", "range_start", "range_end")
            elif char in '[]{}()':
                text_area.tag_add("brackets", "range_start", "range_end")
            elif char.isdigit():
                text_area.tag_add("numbers", "range_start", "range_end")
            elif char in '<>':
                text_area.tag_add("angle", "range_start", "range_end")
    
    # Bind syntax highlighting to text changes
    text_area.bind("<KeyRelease>", lambda event: highlight_syntax())
    
    # Manually trigger syntax highlighting on initial load
    highlight_syntax()

def open_settings():
    settings = tk.Toplevel()
    settings.title("KernelOS Settings")
    settings.geometry("400x300")
    settings.attributes('-topmost', True)
    
    # Background color picker
    def choose_color():
        color = colorchooser.askcolor()[1]
        if color:
            desktop.configure(bg=color)
    
    color_button = tk.Button(settings, text="Change Background Color", command=choose_color)
    color_button.pack(pady=10)
    
    # Register change
    def register_change():
        messagebox.showinfo("Register Change", "Register change functionality not implemented.")
    
    register_button = tk.Button(settings, text="Register Change", command=register_change)
    register_button.pack(pady=10)
    
    # Info display
    def display_info():
        info_window = tk.Toplevel()
        info_window.title("KernelOS Information")
        info_window.geometry("300x200")
        info_window.attributes('-topmost', True)
        
        info_text = ("Built with: Python\n"
                     "Name: KernelOS\n"
                     "Version: 0.2\n"
                     "GUI: KRNLGUI\n"
                     "GUI version: v0.1")
        
        info_label = tk.Label(info_window, text=info_text, justify="left", padx=10, pady=10)
        info_label.pack(fill="both", expand=True)
    
    info_button = tk.Button(settings, text="Display Info", command=display_info)
    info_button.pack(pady=10)

def shutdown():
    desktop.quit()

def restart():
    desktop.quit()
    # Add logic to restart the application or system

def restart_in_command_prompt():
    open_terminal(fullscreen=True)

def create_desktop():
    # Create the main window (desktop)
    global desktop
    desktop = tk.Tk()
    desktop.title("KernelOS")
    desktop.attributes('-fullscreen', True)
    desktop.configure(bg='#129459')  # Set background color

    # Add canvas for drawing triangles
    canvas = tk.Canvas(desktop, bg='#129459', highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    
    # Draw three triangles
    canvas.create_polygon(100, 100, 150, 50, 200, 100, fill='yellow', outline='black')
    canvas.create_polygon(300, 100, 350, 50, 400, 100, fill='red', outline='black')
    canvas.create_polygon(500, 100, 550, 50, 600, 100, fill='blue', outline='black')

    # Bind the Escape key to exit fullscreen
    desktop.bind("<Escape>", lambda event: desktop.attributes('-fullscreen', False))
    
    return desktop

def create_taskbar(root):
    # Create a frame for the taskbar
    taskbar = tk.Frame(root, bg="grey", height=30)
    taskbar.pack(side="bottom", fill="x")

    # Create a Start button
    start_button = tk.Button(taskbar, text="Start", command=lambda: toggle_start_menu(root))
    start_button.pack(side="left")

    return taskbar

def toggle_start_menu(root):
    # Create a simple start menu
    start_menu = tk.Menu(root, tearoff=0)
    start_menu.add_command(label="Text Editor", command=open_text_editor)
    start_menu.add_command(label="Calculator", command=open_calculator)
    start_menu.add_command(label="Terminal", command=open_terminal)
    start_menu.add_command(label="Files", command=open_files)
    start_menu.add_command(label="Settings", command=open_settings)
    start_menu.add_command(label="Shutdown", command=shutdown)
    start_menu.add_command(label="Restart", command=restart)
    start_menu.add_command(label="Restart in CommandPrompt.KRNL mode", command=restart_in_command_prompt)
    
    # Display the start menu
    start_menu.post(10, root.winfo_height() - 60)

def create_desktop_icons(root):
    icon_frame = tk.Frame(root, bg="#129459", width=100)
    icon_frame.pack(side="left", fill="y")

    # Create icons for each application
    icons = [
        ("Calculator", open_calculator),
        ("Text Editor", open_text_editor),
        ("Terminal", open_terminal),
        ("MainConsole", open_main_console),
        ("Settings", open_settings),
        ("Files", open_files)
    ]

    for name, command in icons:
        button = tk.Button(icon_frame, text=name, command=command, width=12, height=2, bg="lightgrey")
        button.pack(pady=10)

# Initialize the desktop and taskbar
desktop = create_desktop()
taskbar = create_taskbar(desktop)
create_desktop_icons(desktop)

# Run the main loop
desktop.mainloop()
