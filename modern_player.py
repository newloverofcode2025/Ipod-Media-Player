import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import vlc
import os
import json
import random
import sys
from pathlib import Path
from datetime import datetime

class ModernMediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Media Player")
        self.root.geometry("1280x720")
        self.root.minsize(1024, 600)
        self.style = ttk.Style()
        self.configure_styles()
        
        # VLC initialization
        self.instance = vlc.Instance("--no-xlib")
        self.player = self.instance.media_player_new()
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_media_end)
        
        # App state
        self.playlist = []
        self.current_index = 0
        self.play_modes = ["Sequential", "Repeat All", "Repeat One", "Shuffle"]
        self.current_play_mode = 0
        self.is_playing = False
        
        self.create_widgets()
        self.setup_bindings()
        self.load_default_playlist()
        
    def configure_styles(self):
        style_config = {
            "TFrame": {"configure": {"background": "#2D2D2D"}},
            "TLabel": {"configure": {
                "background": "#2D2D2D",
                "foreground": "#FFFFFF",
                "font": ("Segoe UI", 10)
            }},
            "TButton": {"configure": {
                "anchor": "center",
                "padding": 8,
                "font": ("Segoe UI", 10, "bold"),
                "background": "#3A3A3A",
                "foreground": "#FFFFFF",
                "borderwidth": 0,
                "relief": "flat"
            }, "map": {
                "background": [("active", "#4A4A4A"), ("disabled", "#2A2A2A")],
                "foreground": [("disabled", "#666666")]
            }},
            "TScale": {"configure": {
                "sliderthickness": 15,
                "troughcolor": "#404040",
                "background": "#3A3A3A"
            }},
            "TCombobox": {
                "configure": {"fieldbackground": "#3A3A3A", "background": "#3A3A3A"},
                "map": {"fieldbackground": [("readonly", "#3A3A3A")]}
            },
            "Vertical.TScrollbar": {"configure": {"arrowsize": 14}},
        }
        
        self.style.theme_create("modern", parent="alt", settings=style_config)
        self.style.theme_use("modern")

    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Video display area
        self.video_frame = ttk.Frame(main_container)
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control panel
        control_panel = ttk.Frame(main_container)
        control_panel.pack(fill=tk.X, pady=10)
        
        # Media controls
        media_controls = ttk.Frame(control_panel)
        media_controls.pack(side=tk.LEFT, padx=20)
        
        # Add media button
        self.btn_add = ttk.Button(media_controls, text="+ Add Media", 
                                  command=self.add_media, style="Accent.TButton")
        self.btn_add.pack(side=tk.LEFT, padx=5)
        ToolTip(self.btn_add, "Add media files to the playlist")
        
        # Transport controls
        self.btn_prev = ttk.Button(media_controls, text="⏮", command=self.prev_track)
        self.btn_prev.pack(side=tk.LEFT, padx=5)
        ToolTip(self.btn_prev, "Play previous track")
        
        self.btn_play = ttk.Button(media_controls, text="▶", command=self.toggle_play)
        self.btn_play.pack(side=tk.LEFT, padx=5)
        ToolTip(self.btn_play, "Play/Pause current track")
        
        self.btn_next = ttk.Button(media_controls, text="⏭", command=self.next_track)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        ToolTip(self.btn_next, "Play next track")
        
        # Progress bar
        self.progress = ttk.Scale(control_panel, from_=0, to=100, command=self.on_seek)
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)
        
        # Volume control
        self.volume_scale = ttk.Scale(control_panel, from_=0, to=100, command=self.set_volume)
        self.volume_scale.set(80)
        self.volume_scale.pack(side=tk.RIGHT, padx=10)
        
        # Play mode selector
        self.mode_selector = ttk.Combobox(control_panel, 
                                          values=self.play_modes,
                                          state="readonly",
                                          width=12)
        self.mode_selector.current(0)
        self.mode_selector.pack(side=tk.RIGHT, padx=20)
        self.mode_selector.bind("<<ComboboxSelected>>", self.change_play_mode)
        
        # Playlist panel
        playlist_panel = ttk.Frame(main_container)
        playlist_panel.pack(fill=tk.BOTH, expand=True)
        
        # Playlist header
        playlist_header = ttk.Frame(playlist_panel)
        playlist_header.pack(fill=tk.X)
        
        ttk.Label(playlist_header, text="Playlist", font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT)
        ttk.Button(playlist_header, text="Clear", command=self.clear_playlist).pack(side=tk.RIGHT)
        
        # Playlist listbox
        self.playlist_box = tk.Listbox(playlist_panel, 
                                       bg="#3A3A3A", fg="white",
                                       selectbackground="#5A5A5A", 
                                       selectforeground="white",
                                       font=("Segoe UI", 10), 
                                       borderwidth=0,
                                       highlightthickness=0)
        self.playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(playlist_panel, command=self.playlist_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist_box.config(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Context menu
        self.create_context_menu()

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#3A3A3A", fg="white",
                                  activebackground="#5A5A5A", activeforeground="white")
        self.context_menu.add_command(label="Play", command=self.play_selected)
        ToolTip(self.context_menu, "Play selected track")
        self.context_menu.add_command(label="Remove", command=self.remove_selected_track)
        ToolTip(self.context_menu, "Remove selected track from playlist")
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Show in Explorer", command=self.show_in_explorer)
        ToolTip(self.context_menu, "Show selected track in file explorer")

    def setup_bindings(self):
        self.root.bind("<space>", lambda e: self.toggle_play())
        self.root.bind("<Left>", lambda e: self.prev_track())
        self.root.bind("<Right>", lambda e: self.next_track())
        self.root.bind("<Escape>", lambda e: self.stop_playback())
        self.playlist_box.bind("<Double-1>", lambda e: self.play_selected())
        self.playlist_box.bind("<Button-3>", self.show_context_menu)

    def load_default_playlist(self):
        default_path = Path.home() / "Music"
        if default_path.exists():
            try:
                self.playlist = [str(f) for f in default_path.iterdir() 
                               if f.suffix.lower() in (".mp3", ".mp4", ".avi", ".mkv")]
                if not self.playlist:
                    self.status_bar.config(text="No media files found in default directory")
                else:
                    self.update_playlist_display()
            except Exception as e:
                self.show_error(f"Error loading default playlist: {str(e)}")
        else:
            self.status_bar.config(text="Default directory does not exist")

    def update_playlist_display(self):
        self.playlist_box.delete(0, tk.END)
        for path in self.playlist:
            self.playlist_box.insert(tk.END, os.path.basename(path))

    def toggle_play(self):
        if self.player.is_playing():
            self.player.pause()
            self.is_playing = False
            self.btn_play.config(text="▶")
        else:
            if self.playlist:
                self.play_current_track()

    def on_media_end(self, event):
        self.next_track()

    def next_track(self):
        if not self.playlist:
            return
            
        if self.play_modes[self.current_play_mode] == "Shuffle":
            self.current_index = random.randint(0, len(self.playlist)-1)
        elif self.play_modes[self.current_play_mode] == "Repeat One":
            pass
        elif self.play_modes[self.current_play_mode] == "Repeat All":
            self.current_index = (self.current_index + 1) % len(self.playlist)
        else:
            if self.current_index < len(self.playlist)-1:
                self.current_index += 1
            else:
                self.stop_playback()
        
        if self.is_playing:
            self.play_current_track()

    def prev_track(self):
        if not self.playlist:
            return
            
        self.current_index = (self.current_index - 1) % len(self.playlist)
        if self.is_playing:
            self.play_current_track()

    def play_current_track(self):
        if not self.playlist:
            return
            
        try:
            media_path = self.playlist[self.current_index]
            if not Path(media_path).exists():
                raise FileNotFoundError(f"File not found: {media_path}")
            
            media = self.instance.media_new(media_path)
            self.player.set_media(media)
            
            if sys.platform.startswith('win'):
                self.player.set_hwnd(self.video_frame.winfo_id())
            else:
                self.player.set_xwindow(self.video_frame.winfo_id())
                
            self.player.play()
            self.is_playing = True
            self.btn_play.config(text="⏸")
            self.update_progress()
            self.highlight_current_track()
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text=f"Now playing: {os.path.basename(media_path)}")
            
        except Exception as e:
            self.show_error(f"Playback failed: {str(e)}")
            self.next_track()

    def highlight_current_track(self):
        self.playlist_box.selection_clear(0, tk.END)
        self.playlist_box.selection_set(self.current_index)
        self.playlist_box.activate(self.current_index)

    def stop_playback(self):
        self.player.stop()
        self.is_playing = False
        self.btn_play.config(text="▶")
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text="Playback stopped")

    def update_progress(self):
        if self.player.is_playing():
            length = self.player.get_length()
            if length > 0:
                pos = self.player.get_position()
                self.progress.set(pos * 100)
                self.root.after(500, self.update_progress)

    def on_seek(self, value):
        if self.player.get_state() == vlc.State.Playing:
            self.player.set_position(float(value) / 100)

    def set_volume(self, value):
        volume = int(float(value))
        if hasattr(self, 'status_bar'):
            if volume == 0:
                self.status_bar.config(text="Muted")
            else:
                self.status_bar.config(text=f"Volume: {volume}%")
        self.player.audio_set_volume(volume)

    def change_play_mode(self, event):
        self.current_play_mode = self.mode_selector.current()
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=f"Play mode changed to {self.play_modes[self.current_play_mode]}")
        if self.is_playing:
            self.play_current_track()

    def play_selected(self):
        selection = self.playlist_box.curselection()
        if selection:
            self.current_index = selection[0]
            self.play_current_track()
        else:
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="No track selected")

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def remove_selected_track(self):
        selection = self.playlist_box.curselection()
        if selection:
            index = selection[0]
            del self.playlist[index]
            self.update_playlist_display()
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="Track removed from playlist")
        else:
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="No track selected")

    def show_in_explorer(self):
        selection = self.playlist_box.curselection()
        if selection:
            path = self.playlist[selection[0]]
            if not os.path.exists(path):
                self.show_error(f"File not found: {path}")
                return
            if sys.platform == "win32":
                os.startfile(os.path.dirname(path))
            else:
                import subprocess
                subprocess.Popen(["xdg-open", os.path.dirname(path)])
        else:
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="No track selected")

    def clear_playlist(self):
        if messagebox.askyesno("Clear Playlist", "Are you sure you want to clear the playlist?"):
            if not self.playlist:
                if hasattr(self, 'status_bar'):
                    self.status_bar.config(text="Playlist is already empty")
            else:
                self.playlist = []
                self.playlist_box.delete(0, tk.END)
                if hasattr(self, 'status_bar'):
                    self.status_bar.config(text="Playlist cleared")

    def add_media(self):
        paths = filedialog.askopenfilenames(
            title="Select Media Files",
            filetypes=[
                ("Media Files", "*.mp3 *.mp4 *.avi *.mkv *.wav *.mov *.flac"),
                ("All Files", "*.*")
            ]
        )
        if paths:
            new_paths = [path for path in paths if path not in self.playlist]
            self.playlist.extend(new_paths)
            self.update_playlist_display()
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text=f"Added {len(new_paths)} items to playlist")
        else:
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="No files selected")

    def save_playlist(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Playlist Files", "*.json")]
        )
        if path:
            if not self.playlist:
                if hasattr(self, 'status_bar'):
                    self.status_bar.config(text="Playlist is empty")
                return
            try:
                with open(path, 'w') as f:
                    json.dump(self.playlist, f)
                if hasattr(self, 'status_bar'):
                    self.status_bar.config(text=f"Playlist saved to {path}")
            except Exception as e:
                self.show_error(f"Error saving playlist: {str(e)}")
        else:
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="Save operation cancelled")

    def load_playlist(self):
        path = filedialog.askopenfilename(
            filetypes=[("Playlist Files", "*.json")]
        )
        if path:
            try:
                with open(path, 'r') as f:
                    self.playlist = json.load(f)
                if not self.playlist:
                    if hasattr(self, 'status_bar'):
                        self.status_bar.config(text="Loaded playlist is empty")
                else:
                    self.update_playlist_display()
                    if hasattr(self, 'status_bar'):
                        self.status_bar.config(text=f"Playlist loaded from {path}")
            except Exception as e:
                self.show_error(f"Error loading playlist: {str(e)}")
        else:
            if hasattr(self, 'status_bar'):
                self.status_bar.config(text="Load operation cancelled")

    def show_error(self, message):
        messagebox.showerror("Error", message)
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=message)
        with open("error.log", "a") as log_file:
            log_file.write(f"{datetime.now()}: {message}\n")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event):
        "Display text in tooltip window"
        self.x = event.x + self.widget.winfo_rootx() + 20
        self.y = event.y + self.widget.winfo_rooty() + 20
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (self.x, self.y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=4)

    def hide(self, event):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMediaPlayer(root)
    
    # Menu bar
    menubar = tk.Menu(root, bg="#3A3A3A", fg="white", activebackground="#5A5A5A")
    root.config(menu=menubar)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0, bg="#3A3A3A", fg="white")
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Add Media", command=app.add_media)
    file_menu.add_command(label="Open Playlist", command=app.load_playlist)
    file_menu.add_command(label="Save Playlist", command=app.save_playlist)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    root.mainloop()