import tkinter
from tkinter import messagebox, Toplevel
import customtkinter as ctk
from tkinter import filedialog
import cv2
from PIL import Image
import os
from datetime import datetime
import threading
import queue
import sys

MOTION_SENSITIVITY_THRESHOLD = 500
FRAMES_TO_RECORD_AFTER_DETECTION = 150

class MeteorTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Meteor Tracker")
        self.geometry("840x700")
        self.configure(fg_color="#1c1c1e")
        self.resizable(False, False)
        self.withdraw()

        self.update_job = None
        self.capture = None
        self.is_running = False
        self.is_recording = False
        self.output_folder = os.path.join(os.path.expanduser("~"), "Desktop", "Meteor_Clips")
        self.last_frame = None
        self.video_writer = None
        self.detection_countdown = 0
        self.log_window = None
        self.log_textbox = None
        self.camera_queue = queue.Queue()
        self.log_history = []
        self.selected_camera_index = 0
        self.selected_camera_backend = cv2.CAP_MSMF
        self.available_camera_details = []

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.setup_ui()
        self.show_splash_screen()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.add_to_log("Programa iniciado.")

    def show_splash_screen(self):
        self.splash = Toplevel(self)
        self.splash.geometry("300x300")
        self.splash.overrideredirect(True)
        self.splash.configure(bg="#1c1c1e")
        x = self.winfo_screenwidth() // 2 - 150
        y = self.winfo_screenheight() // 2 - 150
        self.splash.geometry(f"+{x}+{y}")
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(__file__)
            
            logo_path = os.path.join(base_path, 'logo.png')
            
            logo_image = ctk.CTkImage(light_image=Image.open(logo_path), size=(200, 200))
            logo_label = ctk.CTkLabel(self.splash, image=logo_image, text="", bg_color="transparent")
            logo_label.pack(pady=50)
        except FileNotFoundError:
            logo_label = ctk.CTkLabel(self.splash, text="Meteor Tracker", font=ctk.CTkFont(size=24, weight="bold"), bg_color="transparent")
            logo_label.pack(pady=120)
        self.splash.after(1500, self.finish_splash)

    def finish_splash(self):
        self.splash.destroy()
        self.deiconify()
        self.update_frame()

    def setup_ui(self):
        ctk.set_appearance_mode("dark")
        self.camera_label = ctk.CTkLabel(self, text="", fg_color="#000000", width=800, height=450)
        self.camera_label.place(x=20, y=20)
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.place(relx=0.5, rely=0.84, anchor=tkinter.CENTER)
        self.start_button = ctk.CTkButton(button_frame, text="Iniciar", command=self.start_tracking, font=ctk.CTkFont(size=20, weight="bold"), width=180, height=45)
        self.start_button.pack(pady=5)
        self.stop_button = ctk.CTkButton(button_frame, text="Parar", command=self.stop_tracking, font=ctk.CTkFont(size=16), state="disabled", width=150, height=35, fg_color="#c84444", hover_color="#a23737")
        self.stop_button.pack(pady=5)
        self.settings_button = ctk.CTkButton(self, text="Configurações", command=self.open_settings_window, font=ctk.CTkFont(size=12), width=100, height=28, fg_color="#555555", hover_color="#444444")
        self.settings_button.place(x=20, y=650)
        self.log_button = ctk.CTkButton(self, text="Log", command=self.open_log_window, font=ctk.CTkFont(size=12), width=100, height=28, fg_color="#555555", hover_color="#444444")
        self.log_button.place(x=720, y=650)
    
    def start_tracking(self):
        backend_name = "MSMF"
        if self.selected_camera_backend == cv2.CAP_DSHOW: backend_name = "DSHOW"
        if self.selected_camera_backend == cv2.CAP_VFW: backend_name = "VFW"
        
        print(f"Tentando abrir câmera: Índice {self.selected_camera_index}, Backend: {backend_name}")
        self.capture = cv2.VideoCapture(self.selected_camera_index, self.selected_camera_backend)
        
        if not self.capture or not self.capture.isOpened():
            messagebox.showerror("Erro de Câmera", f"Não foi possível abrir a câmera no índice {self.selected_camera_index} com o backend {backend_name}.")
            self.capture = None
            return
            
        self.is_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.settings_button.configure(state="disabled")
        self.log_button.configure(state="disabled")
        self.add_to_log(f"Rastreio iniciado na câmera {self.selected_camera_index} ({backend_name}).")

    def threaded_camera_finder(self):
        print("Thread de busca iniciada...")
        details = []
        backends_to_try = [(cv2.CAP_MSMF, "MSMF"), (cv2.CAP_DSHOW, "DSHOW"), (cv2.CAP_VFW, "VFW")]

        for i in range(10):
            for backend_code, backend_name in backends_to_try:
                cap = cv2.VideoCapture(i, backend_code)
                if cap.isOpened():
                    if not any(d['index'] == i for d in details):
                        details.append({'name': f"Câmera ({i}, {backend_name})", 'index': i, 'backend': backend_code})
                    cap.release()
        
        if not details:
            details.append({'name': 'Padrão (0, MSMF)', 'index': 0, 'backend': cv2.CAP_MSMF})
            details.append({'name': 'Padrão (0, DSHOW)', 'index': 0, 'backend': cv2.CAP_DSHOW})
        
        self.camera_queue.put(details)

    def open_settings_window(self):
        settings_win = ctk.CTkToplevel(self)
        settings_win.title("Configurações")
        settings_win.geometry("450x250")
        settings_win.configure(fg_color="#2c2c2e")
        settings_win.resizable(False, False)
        settings_win.transient(self)
        settings_win.grab_set()

        camera_frame = ctk.CTkFrame(settings_win, fg_color="transparent")
        camera_frame.pack(pady=20, padx=20, fill="x")
        label_cam = ctk.CTkLabel(camera_frame, text="Selecionar Câmera:")
        label_cam.pack(pady=(0, 5), anchor="w")
        
        camera_menu = ctk.CTkOptionMenu(camera_frame, values=["Procurando câmeras..."])
        camera_menu.pack(fill="x")
        camera_menu.configure(state="disabled")

        def check_for_camera_results():
            try:
                self.available_camera_details = self.camera_queue.get_nowait()
                camera_names = [d['name'] for d in self.available_camera_details]
                
                print(f"Busca finalizada. Câmeras encontradas: {camera_names}")
                
                camera_menu.configure(values=camera_names, state="normal")
                
                current_name = next((d['name'] for d in self.available_camera_details if d['index'] == self.selected_camera_index and d['backend'] == self.selected_camera_backend), None)
                if current_name:
                    camera_menu.set(current_name)
                else:
                    camera_menu.set(camera_names[0])
                    camera_selected(camera_names[0])

            except queue.Empty:
                settings_win.after(200, check_for_camera_results)

        def camera_selected(choice: str):
            chosen_detail = next((d for d in self.available_camera_details if d['name'] == choice), None)
            if chosen_detail:
                self.selected_camera_index = chosen_detail['index']
                self.selected_camera_backend = chosen_detail['backend']
        
        camera_menu.configure(command=camera_selected)
        
        search_thread = threading.Thread(target=self.threaded_camera_finder, daemon=True)
        search_thread.start()
        
        check_for_camera_results()

    def stop_tracking(self):
        self.is_running = False
        if self.is_recording: self.stop_recording()
        if self.capture:
            self.capture.release()
            self.capture = None
        black_img = ctk.CTkImage(light_image=Image.new("RGB", (800, 450), "black"), size=(800, 450))
        self.camera_label.configure(image=black_img)
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.settings_button.configure(state="normal")
        self.log_button.configure(state="normal")
        self.add_to_log("Rastreio parado.")

    def update_frame(self):
        if self.is_running and self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, 1)
                self.detect_motion(frame)
                if self.is_recording:
                    self.video_writer.write(frame)
                    self.detection_countdown -= 1
                    cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
                    if self.detection_countdown <= 0:
                        self.stop_recording()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(800, 450))
                self.camera_label.configure(image=ctk_img)
        self.update_job = self.after(10, self.update_frame)
    
    def on_closing(self):
        self.add_to_log("Programa fechado.")
        print("Fechando aplicativo...")
        self.is_running = False
        if self.update_job:
            self.after_cancel(self.update_job)
            self.update_job = None
        if self.capture:
            self.capture.release()
        self.destroy()

    def detect_motion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if self.last_frame is None:
            self.last_frame = gray
            return
        frame_delta = cv2.absdiff(self.last_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = any(cv2.contourArea(c) > MOTION_SENSITIVITY_THRESHOLD for c in contours)
        if motion_detected:
            self.detection_countdown = FRAMES_TO_RECORD_AFTER_DETECTION
            if not self.is_recording:
                self.start_recording()
                self.add_to_log("Objeto Detectado.")
        self.last_frame = gray

    def start_recording(self):
        self.is_recording = True
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Meteoro_{timestamp}.mp4"
        filepath = os.path.join(self.output_folder, filename)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        w = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_writer = cv2.VideoWriter(filepath, fourcc, 30.0, (w, h))
        print(f"DETECÇÃO! Iniciando gravação em: {filepath}")

    def stop_recording(self):
        self.is_recording = False
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            print("Gravação salva.")

    def open_log_window(self):
        if self.log_window is None or not self.log_window.winfo_exists():
            self.log_window = ctk.CTkToplevel(self)
            self.log_window.title("Log de Atividade")
            self.log_window.geometry("600x400")
            self.log_window.configure(fg_color="#2c2c2e")
            self.log_window.transient(self)
            
            self.log_textbox = ctk.CTkTextbox(self.log_window, state="normal", width=580, height=380)
            self.log_textbox.pack(pady=10, padx=10)
            
            for entry in self.log_history:
                self.log_textbox.insert("end", entry)
            
            self.log_textbox.configure(state="disabled")
            self.log_textbox.see("end")
        
        self.log_window.lift()

    def add_to_log(self, message):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_history.append(log_entry)
        
        print(log_entry.strip())
        
        if self.log_window and self.log_window.winfo_exists() and self.log_textbox:
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", log_entry)
            self.log_textbox.configure(state="disabled")
            self.log_textbox.see("end")

if __name__ == "__main__":
    app = MeteorTrackerApp()
    app.mainloop()