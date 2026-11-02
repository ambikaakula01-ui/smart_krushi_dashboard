import serial
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

# ================= SERIAL CONFIG =================
PORT = "COM13"   # Change according to your PC
BAUD = 9600

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)
except:
    messagebox.showerror("Error", "Master Arduino not connected")
    exit()

# ================= SEND COMMAND =================
def send_cmd(cmd):
    ser.write((cmd + "\n").encode())
    log.insert(tk.END, f"Sent: {cmd}\n")
    log.see(tk.END)

# ================= UPDATE SENSOR DISPLAY =================
def update_display(data):
    try:
        parts = data.split(",")
        node = parts[0]

        temp = parts[1].split(":")[1]
        hum  = parts[2].split(":")[1]
        s1   = parts[3].split(":")[1]
        s2   = parts[4].split(":")[1]

        if node == "N1":
            n1_temp.set(temp + " °C")
            n1_hum.set(hum + " %")
            n1_s1.set(s1)
            n1_s2.set(s2)
        elif node == "N2":
            n2_temp.set(temp + " °C")
            n2_hum.set(hum + " %")
            n2_s1.set(s1)
            n2_s2.set(s2)

    except:
        pass

# ================= SERIAL READ THREAD =================
def read_serial():
    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                log.insert(tk.END, f"Received: {line}\n")
                log.see(tk.END)
                update_display(line)
        except:
            break

# ================= AUTO SENSOR REQUEST =================
def auto_request():
    while True:
        send_cmd("N1GET")
        time.sleep(2)
        send_cmd("N1GET")
        time.sleep(5)

# ================= UI =================
root = tk.Tk()
root.title("Smart Krushi Dashboard")
root.geometry("900x600")
root.configure(bg="#f0f4f7")
root.resizable(False, False)

# ================= HEADER =================
header_frame = tk.frame(root, bg="#1e90ff", pady=15)
header_frame.pack(fill="x")

tk.Label(header_frame, text="SMART KRUSHI", font=("Helvetica", 20, "bold"),
         bg="#1e90ff", fg="white").pack()
tk.Label(header_frames, text="LoRa Smart Agriculture Monitoring & Control",
         font=("Arial", 12), bg="#1e90ff", fg="white").pack()
tk.Label(header_frame, text="Sri Vasavi Engineering College, Tadepalligudem",
         font=("Arial", 10, "italic"), bg="#1e90ff", fg="white").pack()
tk.Label(header_frame, text="Monitor temperature, humidity, soil moisture & control relays",
         font=("Arial", 10), bg="#1e90ff", fg="white").pack(pady=(5,0))

# ================= MAIN CONTENT FRAME =================
main_frame = tk.Frame(root, bg="#f0f4f7")
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

# ================= NODE 1 FRAME =================
frame1 = tk.LabelFrame(main_frame, text="NODE 1", font=("Arial", 12, "bold"),
                       bg="#e6f2ff", fg="#000080", padx=10, pady=10)
frame1.grid(row=0, column=0, sticky="nsew", padx=5)

n1_temp = tk.StringVar(value="--")
n1_hum  = tk.StringVar(value="--")
n1_s1   = tk.StringVar(value="--")
n1_s2   = tk.StringVar(value="--")

tk.Label(frame1, text="Temperature:", bg="#e6f2ff").grid(row=0, column=0, sticky="w")
tk.Label(frame1, textvariable=n1_temp, bg="#e6f2ff").grid(row=0, column=1)
tk.Label(frame1, text="Humidity:", bg="#e6f2ff").grid(row=1, column=0, sticky="w")
tk.Label(frame1, textvariable=n1_hum, bg="#e6f2ff").grid(row=1, column=1)
tk.Label(frame1, text="Soil 1:", bg="#e6f2ff").grid(row=2, column=0, sticky="w")
tk.Label(frame1, textvariable=n1_s1, bg="#e6f2ff").grid(row=2, column=1)
tk.Label(frame1, text="Soil 2:", bg="#e6f2ff").grid(row=3, column=0, sticky="w")
tk.Label(frame1, textvariable=n1_s2, bg="#e6f2ff").grid(row=3, column=1)

# Node 1 Relays
tk.Button(frame1, text="R1 ON", width=10, bg="#006600", fg="white",
          command=lambda: send_cmd("N1R1ON")).grid(row=4, column=0, pady=5)
tk.Button(frame1, text="R1 OFF", width=10, bg="#cc0000", fg="white",
          command=lambda: send_cmd("N1R1OFF")).grid(row=4, column=1, pady=5)
tk.Button(frame1, text="R2 ON", width=10, bg="#006600", fg="white",
          command=lambda: send_cmd("N1R2ON")).grid(row=5, column=0, pady=5)
tk.Button(frame1, text="R2 OFF", width=10, bg="#cc0000", fg="white",
          command=lambda: send_cmd("N1R2OFF")).grid(row=5, column=1, pady=5)

# ================= NODE 2 FRAME =================
frame2 = tk.LabelFrame(main_frame, text="NODE 2", font=("Arial", 12, "bold"),
                       bg="#fff0e6", fg="#cc6600", padx=10, pady=10)
frame2.grid(row=0, column=1, sticky="nsew", padx=5)

n2_temp = tk.StringVar(value="--")
n2_hum  = tk.StringVar(value="--")
n2_s1   = tk.StringVar(value="--")
n2_s2   = tk.StringVar(value="--")

tk.Label(frame2, text="Temperature:", bg="#fff0e6").grid(row=0, column=0, sticky="w")
tk.Label(frame2, textvariable=n2_temp, bg="#fff0e6").grid(row=0, column=1)
tk.Label(frame2, text="Humidity:", bg="#fff0e6").grid(row=1, column=0, sticky="w")
tk.Label(frame2, textvariable=n2_hum, bg="#fff0e6").grid(row=1, column=1)
tk.Label(frame2, text="Soil 1:", bg="#fff0e6").grid(row=2, column=0, sticky="w")
tk.Label(frame2, textvariable=n2_s1, bg="#fff0e6").grid(row=2, column=1)
tk.Label(frame2, text="Soil 2:", bg="#fff0e6").grid(row=3, column=0, sticky="w")
tk.Label(frame2, textvariable=n2_s2, bg="#fff0e6").grid(row=3, column=1)

# Node 2 Relays
tk.Button(frame2, text="R1 ON", width=10, bg="#006600", fg="white",
          command=lambda: send_cmd("N2R1ON")).grid(row=4, column=0, pady=5)
tk.Button(frame2, text="R1 OFF", width=10, bg="#cc0000", fg="white",
          command=lambda: send_cmd("N2R1OFF")).grid(row=4, column=1, pady=5)
tk.Button(frame2, text="R2 ON", width=10, bg="#006600", fg="white",
          command=lambda: send_cmd("N2R2ON")).grid(row=5, column=0, pady=5)
tk.Button(frame2, text="R2 OFF", width=10, bg="#cc0000", fg="white",
          command=lambda: send_cmd("N2R2OFF")).grid(row=5, column=1, pady=5)

# ================= LOG FRAME =================
log_frame = tk.LabelFrame(root, text="System Log", font=("Arial", 12, "bold"),
                          bg="#f9f9f9", fg="#000000", padx=5, pady=5)
log_frame.pack(padx=10, pady=10, fill="both", expand=True)

log = scrolledtext.ScrolledText(log_frame, width=110, height=8, bg="#f0f0f0", fg="#000000")
log.pack(padx=5, pady=5, fill="both", expand=True)
log.insert(tk.END, "Dashboard Ready...\n")

# ================= EXIT =================
def on_close():
    ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# ================= THREADS =================
threading.Thread(target=read_seriall, daemon=True).start()
threading.Thread(target=auto_request, daemon=True).start()

root.mainloop()