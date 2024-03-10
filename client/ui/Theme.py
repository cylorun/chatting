from tkinter import ttk
import os, json

class Theme:
    theme_json = os.path.join(os.getcwd(),'config','theme.json')
    
    def dark(root):
        style = ttk.Style(root)

        style.theme_use("clam")

        style.configure(".", background="#2B2B2B", foreground="#A9B7C6")

        style.configure("TLabel", background="#2B2B2B", foreground="#A9B7C6", font=("Arial", 12))

        style.configure("TButton", background="#3C3F41", foreground="#A9B7C6", borderwidth=0)
        style.map("TButton", background=[("active", "#4E5254"), ("pressed", "#313335")], foreground=[("disabled", "#555555")])

        style.configure("TEntry", background="#3C3F41", foreground="#A9B7C6", fieldbackground="#3C3F41", borderwidth=0)
        style.map("TEntry", background=[("focus", "#4E5254")], foreground=[("disabled", "#555555")])

        style.configure("TCanvas", background="#2B2B2B", highlightthickness=0)

        style.configure("TFrame", background="#2B2B2B", highlightthickness=0)

        style.configure("TScrollbar", background="#3C3F41", troughcolor="#2B2B2B", borderwidth=0)
        style.map("TScrollbar", background=[("active", "#4E5254")])
        style.configure("TNotebook", background="#2B2B2B", borderwidth=0)

        style.configure("TNotebook.Tab", background="#3C3F41", foreground="#A9B7C6", borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", "#4E5254"), ("active", "#313335")])
        Theme.save_theme('dark')

    def aurora(root):
        style = ttk.Style(root)

        style.theme_use("clam")

        style.configure(".", background="#000000", foreground="#FFFFFF")

        style.configure("TLabel", background="#000000", foreground="#FFFFFF", font=("Arial", 12))

        style.configure("TButton", background="#002B36", foreground="#FFFFFF", borderwidth=0)
        style.map("TButton", background=[("active", "#073642"), ("pressed", "#586E75")], foreground=[("disabled", "#657B83")])

        style.configure("TEntry", background="#002B36", foreground="#FFFFFF", fieldbackground="#002B36", borderwidth=0)
        style.map("TEntry", background=[("focus", "#073642")], foreground=[("disabled", "#657B83")])

        style.configure("TCanvas", background="#000000", highlightthickness=0)

        style.configure("TFrame", background="#000000", highlightthickness=0)

        style.configure("TScrollbar", background="#002B36", troughcolor="#000000", borderwidth=0)
        style.map("TScrollbar", background=[("active", "#073642")])
        style.configure("TNotebook", background="#000000", borderwidth=0)

        style.configure("TNotebook.Tab", background="#002B36", foreground="#FFFFFF", borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", "#073642"), ("active", "#586E75")])
        Theme.save_theme('aurora')
        
    def light(root):
        style = ttk.Style(root)

        style.theme_use("clam")

        style.configure(".", background="#F0F0F0", foreground="#333333")

        style.configure("TLabel", background="#F0F0F0", foreground="#333333", font=("Arial", 12))

        style.configure("TButton", background="#E0E0E0", foreground="#333333", borderwidth=0)
        style.map("TButton", background=[("active", "#D0D0D0"), ("pressed", "#C0C0C0")], foreground=[("disabled", "#999999")])

        style.configure("TEntry", background="#E0E0E0", foreground="#333333", fieldbackground="#E0E0E0", borderwidth=0)
        style.map("TEntry", background=[("focus", "#D0D0D0")], foreground=[("disabled", "#999999")])

        style.configure("TCanvas", background="#F0F0F0", highlightthickness=0)

        style.configure("TFrame", background="#F0F0F0", highlightthickness=0)

        style.configure("TScrollbar", background="#E0E0E0", troughcolor="#F0F0F0", borderwidth=0)
        style.map("TScrollbar", background=[("active", "#D0D0D0")])
        style.configure("TNotebook", background="#F0F0F0", borderwidth=0)

        style.configure("TNotebook.Tab", background="#E0E0E0", foreground="#333333", borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", "#D0D0D0"), ("active", "#C0C0C0")])
        Theme.save_theme('light')
    
    def save_theme(theme):
        with open(Theme.theme_json, 'w+') as file:
                        json.dump({"theme":theme}, file, indent=2)
    def get_theme():
        if os.path.exists(Theme.theme_json):
            try:
                with open(Theme.theme_json) as file:
                    return json.load(file)['theme']
            except KeyError:
                return None
        return None
    
    def load_prev(root):
        prev = Theme.get_theme()
        Theme.set_theme(prev, root)
    
    def set_theme(theme, root):
        match theme:
            case 'light':
                Theme.light(root)
            case 'dark':
                Theme.dark(root)
            case 'aurora':
                Theme.aurora(root)
            case _: # default case
                Theme.light(root)