#!/usr/bin/env python3
"""
Random Color Addon - Development Helper
Một script duy nhất với UI để quản lý tất cả chức năng development
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import sys
import shutil
import subprocess
import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AddonDevHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Random Color Addon - Development Helper")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Paths
        self.project_root = Path(__file__).parent
        self.addon_path = self.project_root / "random_color_addon"
        
        # Blender paths
        self.blender_paths = [
            Path.home() / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / "4.4" / "scripts" / "addons",
            Path.home() / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / "4.3" / "scripts" / "addons",
            Path("D:/UngDung/Blender/4.4/scripts/addons"),
            Path("D:/UngDung/Blender/4.3/scripts/addons"),
        ]
        
        self.blender_addons_path = None
        self.find_blender_addons_path()
        
        # File watcher
        self.observer = None
        self.watching = False
        
        self.setup_ui()
        
    def find_blender_addons_path(self):
        """Tìm đường dẫn Blender addons"""
        for path in self.blender_paths:
            if path.exists():
                self.blender_addons_path = path
                break
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Random Color Addon - Development Helper", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Blender path label
        blender_text = f"Blender Addons: {self.blender_addons_path}" if self.blender_addons_path else "Blender Addons: Not found"
        self.blender_label = ttk.Label(status_frame, text=blender_text, foreground="blue" if self.blender_addons_path else "red")
        self.blender_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Actions frame
        actions_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        actions_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        self.install_btn = ttk.Button(actions_frame, text="Install Addon", command=self.install_addon)
        self.install_btn.grid(row=0, column=0, padx=(0, 10), pady=5)
        
        self.update_btn = ttk.Button(actions_frame, text="Update Addon", command=self.update_addon)
        self.update_btn.grid(row=0, column=1, padx=(0, 10), pady=5)
        
        self.check_btn = ttk.Button(actions_frame, text="Check Syntax", command=self.check_syntax)
        self.check_btn.grid(row=0, column=2, padx=(0, 10), pady=5)
        
        self.open_blender_btn = ttk.Button(actions_frame, text="Open Blender", command=self.open_blender)
        self.open_blender_btn.grid(row=0, column=3, padx=(0, 10), pady=5)
        
        self.zip_btn = ttk.Button(actions_frame, text="Create ZIP", command=self.create_zip)
        self.zip_btn.grid(row=0, column=4, padx=(0, 10), pady=5)
        
        # File watcher frame
        watcher_frame = ttk.LabelFrame(main_frame, text="File Watcher", padding="10")
        watcher_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.watch_btn = ttk.Button(watcher_frame, text="Start Watching", command=self.toggle_watching)
        self.watch_btn.grid(row=0, column=0, padx=(0, 10), pady=5)
        
        self.watch_status_label = ttk.Label(watcher_frame, text="Not watching", foreground="red")
        self.watch_status_label.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initial log
        self.log("Development Helper started")
        if self.blender_addons_path:
            self.log(f"Found Blender addons: {self.blender_addons_path}")
        else:
            self.log("Blender addons directory not found!", "ERROR")
    
    def log(self, message, level="INFO"):
        """Thêm message vào log"""
        timestamp = time.strftime("%H:%M:%S")
        color = {"INFO": "black", "ERROR": "red", "SUCCESS": "green"}.get(level, "black")
        
        self.log_text.insert(tk.END, f"[{timestamp}] {level}: {message}\n")
        self.log_text.see(tk.END)
        
        # Update status
        self.status_label.config(text=message)
        
        self.root.update_idletasks()
    
    def install_addon(self):
        """Cài đặt addon"""
        if not self.blender_addons_path:
            messagebox.showerror("Error", "Blender addons directory not found!")
            return
        
        def install():
            try:
                self.log("Installing addon...")
                
                target_path = self.blender_addons_path / "random_color_addon"
                
                # Remove existing
                if target_path.exists():
                    shutil.rmtree(target_path)
                    self.log("Removed existing addon")
                
                # Copy addon
                shutil.copytree(self.addon_path, target_path)
                self.log(f"Addon installed: {target_path}", "SUCCESS")
                
            except Exception as e:
                self.log(f"Install failed: {e}", "ERROR")
        
        threading.Thread(target=install, daemon=True).start()
    
    def update_addon(self):
        """Cập nhật addon"""
        if not self.blender_addons_path:
            messagebox.showerror("Error", "Blender addons directory not found!")
            return
        
        def update():
            try:
                self.log("Updating addon...")
                
                target_path = self.blender_addons_path / "random_color_addon"
                
                if not target_path.exists():
                    self.log("Addon not installed! Install first.", "ERROR")
                    return
                
                # Remove existing
                shutil.rmtree(target_path)
                self.log("Removed existing addon")
                
                # Copy updated addon
                shutil.copytree(self.addon_path, target_path)
                self.log(f"Addon updated: {target_path}", "SUCCESS")
                self.log("Please reload addon in Blender: Disable and enable again")
                
            except Exception as e:
                self.log(f"Update failed: {e}", "ERROR")
        
        threading.Thread(target=update, daemon=True).start()
    
    def create_zip(self):
        """Tạo file ZIP của addon"""
        def create():
            try:
                import zipfile
                from datetime import datetime
                
                self.log("Creating ZIP file...")
                
                # Tạo tên file với timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                zip_filename = f"random_color_addon_{timestamp}.zip"
                zip_path = self.project_root / zip_filename
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in self.addon_path.rglob('*'):
                        if file_path.is_file():
                            # Tạo relative path trong zip
                            arcname = file_path.relative_to(self.addon_path.parent)
                            zipf.write(file_path, arcname)
                
                self.log(f"ZIP created: {zip_path}", "SUCCESS")
                self.log(f"File size: {zip_path.stat().st_size / 1024:.1f} KB")
                
                # Mở thư mục chứa file ZIP
                os.startfile(self.project_root)
                
            except Exception as e:
                self.log(f"ZIP creation failed: {e}", "ERROR")
        
        threading.Thread(target=create, daemon=True).start()
    
    def check_syntax(self):
        """Kiểm tra syntax"""
        def check():
            try:
                self.log("Checking syntax...")
                
                import ast
                all_good = True
                
                for py_file in self.addon_path.rglob("*.py"):
                    try:
                        with open(py_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        ast.parse(content)
                        self.log(f"✅ {py_file.name}: OK")
                    except SyntaxError as e:
                        self.log(f"❌ {py_file.name}: {e}", "ERROR")
                        all_good = False
                    except Exception as e:
                        self.log(f"❌ {py_file.name}: {e}", "ERROR")
                        all_good = False
                
                if all_good:
                    self.log("All files have valid syntax!", "SUCCESS")
                else:
                    self.log("Some files have syntax errors!", "ERROR")
                    
            except Exception as e:
                self.log(f"Syntax check failed: {e}", "ERROR")
        
        threading.Thread(target=check, daemon=True).start()
    
    def open_blender(self):
        """Mở Blender"""
        blender_paths = [
            "D:/UngDung/Blender/blender.exe",
            "blender.exe",  # In PATH
        ]
        
        blender_exe = None
        for path in blender_paths:
            if os.path.exists(path):
                blender_exe = path
                break
        
        if not blender_exe:
            try:
                result = subprocess.run(["where", "blender"], capture_output=True, text=True)
                if result.returncode == 0:
                    blender_exe = result.stdout.strip().split('\n')[0]
            except:
                pass
        
        if blender_exe:
            self.log(f"Opening Blender: {blender_exe}")
            subprocess.Popen([blender_exe])
        else:
            messagebox.showerror("Error", "Blender executable not found!")
    
    def toggle_watching(self):
        """Bật/tắt file watcher"""
        if self.watching:
            self.stop_watching()
        else:
            self.start_watching()
    
    def start_watching(self):
        """Bắt đầu watch files"""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class FileHandler(FileSystemEventHandler):
                def __init__(self, helper):
                    self.helper = helper
                    self.last_reload = 0
                    self.reload_delay = 2
                
                def on_modified(self, event):
                    if event.is_directory or not event.src_path.endswith('.py'):
                        return
                    
                    current_time = time.time()
                    if current_time - self.last_reload < self.reload_delay:
                        return
                    
                    self.last_reload = current_time
                    file_name = os.path.basename(event.src_path)
                    self.helper.log(f"File changed: {file_name}")
                    self.helper.auto_update()
            
            self.observer = Observer()
            self.observer.schedule(FileHandler(self), str(self.addon_path), recursive=True)
            self.observer.start()
            
            self.watching = True
            self.watch_btn.config(text="Stop Watching")
            self.watch_status_label.config(text="Watching...", foreground="green")
            self.log("File watcher started")
            
        except ImportError:
            messagebox.showerror("Error", "watchdog package not found!\nRun: pip install watchdog")
        except Exception as e:
            self.log(f"Failed to start watcher: {e}", "ERROR")
    
    def stop_watching(self):
        """Dừng watch files"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        
        self.watching = False
        self.watch_btn.config(text="Start Watching")
        self.watch_status_label.config(text="Not watching", foreground="red")
        self.log("File watcher stopped")
    
    def auto_update(self):
        """Tự động cập nhật addon"""
        def update():
            try:
                if not self.blender_addons_path:
                    return
                
                target_path = self.blender_addons_path / "random_color_addon"
                if not target_path.exists():
                    return
                
                # Remove existing
                shutil.rmtree(target_path)
                
                # Copy updated addon
                shutil.copytree(self.addon_path, target_path)
                
                self.log("Auto-updated addon", "SUCCESS")
                self.log("Please reload addon in Blender")
                
            except Exception as e:
                self.log(f"Auto-update failed: {e}", "ERROR")
        
        threading.Thread(target=update, daemon=True).start()
    
    def run(self):
        """Chạy ứng dụng"""
        try:
            self.root.mainloop()
        finally:
            if self.observer:
                self.stop_watching()

if __name__ == "__main__":
    # Install required packages if needed
    try:
        import watchdog
    except ImportError:
        print("Installing watchdog package...")
        subprocess.run([sys.executable, "-m", "pip", "install", "watchdog"])
    
    # Run the helper
    app = AddonDevHelper()
    app.run()
