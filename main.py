import tkinter as tk
from tkinter import ttk
import socket
import threading
import uuid

class NetworkScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Scanner")
        
        self.root.geometry("800x600")  
        self.root.resizable(False, False)  
        
        self.ip_choice = tk.StringVar()
        
        self.choice_label = ttk.Label(root, text="Select IP type:")
        self.choice_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.public_ip_radio = ttk.Radiobutton(root, text="Public IP", variable=self.ip_choice, value="public")
        self.public_ip_radio.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        self.local_ip_radio = ttk.Radiobutton(root, text="Local IP", variable=self.ip_choice, value="local")
        self.local_ip_radio.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        self.host_label = ttk.Label(root, text="Target Host:")
        self.host_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.host_entry = ttk.Entry(root, width=30)
        self.host_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        self.scan_button = ttk.Button(root, text="Scan", command=self.start_scan)
        self.scan_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        
        self.results_text = tk.Text(root, width=100, height=30, state='disabled')
        self.results_text.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
        
        self.found_devices = []  # List to store information about found devices
    
    def start_scan(self):
        ip_type = self.ip_choice.get()
        host = self.host_entry.get()
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)  
        self.results_text.insert(tk.END, f"Scanning host {host}...\n")
        self.results_text.config(state='disabled')
        if ip_type == "public":
            self.results_text.insert(tk.END, f"Please Select Local IP ......")
            pass
        elif ip_type == "local":
            threading.Thread(target=self.scan_local_network).start()
    
    def scan_local_network(self):
        local_ip = socket.gethostbyname(socket.gethostname())
        network_prefix = '.'.join(local_ip.split('.')[:-1]) + '.'
        
        self.results_text.config(state='normal')
        self.results_text.insert(tk.END, f"Scanning local network...\n")
        
        for i in range(1, 255):
            ip = network_prefix + str(i)
            if self.is_valid_ip(ip):  # Check if IP address is valid
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
                    self.found_devices.append((ip, hostname, mac))
                    self.display_device(ip, hostname, mac)
                except socket.herror:
                    pass
        
        self.results_text.config(state='disabled')
    
    def is_valid_ip(self, ip):
        # Check if the IP address is valid
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    
    def display_device(self, ip, hostname, mac):
        self.results_text.config(state='normal')
        self.results_text.insert(tk.END, f"IP: {ip}, Hostname: {hostname}, MAC Address: {mac}\n")
        self.results_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = NetworkScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
