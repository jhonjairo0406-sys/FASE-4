import tkinter as tk
from tkinter import messagebox, ttk


# ==========================================
# CLASS: Usuario (Login Requirements)
# ==========================================
class Usuario:
    def __init__(self, usuario: str = "programacion", password: str = "programacion"):
        self._usuario = usuario
        self._password = password

    def validar(self, usuario_ingresado: str, password_ingresada: str) -> bool:
        return (
            self._usuario == usuario_ingresado
            and self._password == password_ingresada
        )


# ==========================================
# CLASS: ComputadorMantenimiento (Exercise 4)
# ==========================================
class ComputadorMantenimiento:
    def __init__(self, codigo: str, valor_hora: float):
        self._codigo = codigo
        self._hora_entrada = None
        self._valor_hora = valor_hora
        self._hora_salida = None

    def registrar_entrada(self, hora: float):
        self._hora_entrada = hora

    def registrar_salida(self, hora: float):
        self._hora_salida = hora

    def calcular_valor(self, hora_salida: float) -> float:
        if self._hora_entrada is None:
            raise ValueError("Entry time has not been recorded.")
        
        tiempo_transcurrido = hora_salida - self._hora_entrada
        if tiempo_transcurrido < 0:
            raise ValueError("Exit time cannot be earlier than entry time.")
        
        return tiempo_transcurrido * self._valor_hora

    def obtener_codigo(self) -> str:
        return self._codigo


# ==========================================
# GUI APPLICATION (Tkinter - English)
# ==========================================
class MaintenanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maintenance Tech Support System")
        self.geometry("520x580")
        self.resizable(False, False)

        # Instance of user validator & internal list for computers
        self.user_system = Usuario()
        self.computers_list = []

        # Show Login Screen first
        self.show_login_screen()

    # --------------------------------------
    # LOGIN SCREEN
    # --------------------------------------
    def show_login_screen(self):
        self.clear_window()

        frame = ttk.Frame(self, padding="30")
        frame.pack(expand=True, fill="both")

        ttk.Label(
            frame, 
            text="SYSTEM LOGIN", 
            font=("Helvetica", 16, "bold")
        ).pack(pady=15)

        ttk.Label(frame, text="Username:").pack(anchor="w", pady=(10, 2))
        self.entry_username = ttk.Entry(frame, width=30)
        self.entry_username.pack(pady=2)

        ttk.Label(frame, text="Password:").pack(anchor="w", pady=(10, 2))
        self.entry_password = ttk.Entry(frame, show="*", width=30)
        self.entry_password.pack(pady=2)

        btn_login = ttk.Button(
            frame, 
            text="Login", 
            command=self.handle_login
        )
        btn_login.pack(pady=20)

    def handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if self.user_system.validar(username, password):
            messagebox.showinfo("Success", "Access granted. Welcome!")
            self.show_main_screen()
        else:
            messagebox.showerror(
                "Access Denied", 
                "Invalid username or password. Please try again."
            )

    # --------------------------------------
    # MAIN APPLICATION SCREEN
    # --------------------------------------
    def show_main_screen(self):
        self.clear_window()

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        ttk.Label(
            main_frame, 
            text="Computer Maintenance Control", 
            font=("Helvetica", 14, "bold")
        ).pack(pady=(0, 15))

        # --- Register Section ---
        register_frame = ttk.LabelFrame(
            main_frame, 
            text=" Register New Computer ", 
            padding="10"
        )
        register_frame.pack(fill="x", pady=5)

        ttk.Label(register_frame, text="Code / Serial:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.entry_code = ttk.Entry(register_frame, width=15)
        self.entry_code.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(register_frame, text="Entry Hour (0-24):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.entry_entry_hour = ttk.Entry(register_frame, width=15)
        self.entry_entry_hour.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(register_frame, text="Rate per Hour ($):").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.entry_rate = ttk.Entry(register_frame, width=15)
        self.entry_rate.grid(row=2, column=1, padx=5, pady=5)

        btn_add = ttk.Button(
            register_frame, 
            text="Register Computer", 
            command=self.add_computer
        )
        btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Process Exit Section ---
        exit_frame = ttk.LabelFrame(
            main_frame, 
            text=" Process Computer Checkout ", 
            padding="10"
        )
        exit_frame.pack(fill="x", pady=10)

        ttk.Label(exit_frame, text="Select Computer:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.combo_computers = ttk.Combobox(
            exit_frame, 
            state="readonly", 
            width=20
        )
        self.combo_computers.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(exit_frame, text="Exit Hour (0-24):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.entry_exit_hour = ttk.Entry(exit_frame, width=15)
        self.entry_exit_hour.grid(row=1, column=1, padx=5, pady=5)

        btn_calculate = ttk.Button(
            exit_frame, 
            text="Calculate & Checkout", 
            command=self.process_checkout
        )
        btn_calculate.grid(row=2, column=0, columnspan=2, pady=10)

        # Logout button
        btn_logout = ttk.Button(
            main_frame, 
            text="Logout", 
            command=self.show_login_screen
        )
        btn_logout.pack(anchor="e", pady=5)

    # --------------------------------------
    # LOGIC HELPER METHODS
    # --------------------------------------
    def add_computer(self):
        code = self.entry_code.get().strip()
        entry_str = self.entry_entry_hour.get().strip()
        rate_str = self.entry_rate.get().strip()

        if not code or not entry_str or not rate_str:
            messagebox.showwarning("Warning", "All registration fields are required.")
            return

        try:
            entry_hour = float(entry_str)
            rate = float(rate_str)

            if entry_hour < 0 or entry_hour > 24:
                raise ValueError("Entry hour must be between 0 and 24.")
            if rate <= 0:
                raise ValueError("Rate per hour must be greater than zero.")

            # Create object instance
            comp = ComputadorMantenimiento(code, rate)
            comp.registrar_entrada(entry_hour)

            # Store in list
            self.computers_list.append(comp)

            # Update combobox options
            self.update_combobox()

            # Clear inputs
            self.entry_code.delete(0, tk.END)
            self.entry_entry_hour.delete(0, tk.END)
            self.entry_rate.delete(0, tk.END)

            messagebox.showinfo(
                "Success", 
                f"Computer '{code}' successfully registered."
            )

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def process_checkout(self):
        selected_index = self.combo_computers.current()
        exit_str = self.entry_exit_hour.get().strip()

        if selected_index == -1:
            messagebox.showwarning("Warning", "Please select a computer from the list.")
            return

        if not exit_str:
            messagebox.showwarning("Warning", "Please enter the exit hour.")
            return

        try:
            exit_hour = float(exit_str)
            if exit_hour < 0 or exit_hour > 24:
                raise ValueError("Exit hour must be between 0 and 24.")

            selected_comp = self.computers_list[selected_index]

            # Calculate total maintenance cost
            total_cost = selected_comp.calcular_valor(exit_hour)
            selected_comp.registrar_salida(exit_hour)

            messagebox.showinfo(
                "Checkout Summary",
                f"Computer Code: {selected_comp.obtener_codigo()}\n"
                f"Entry Hour: {selected_comp._hora_entrada:.2f} h\n"
                f"Exit Hour: {exit_hour:.2f} h\n"
                f"Total Diagnosis Cost: ${total_cost:.2f}"
            )

            # Remove processed computer from the active list
            self.computers_list.pop(selected_index)
            self.update_combobox()
            self.entry_exit_hour.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_combobox(self):
        codes = [comp.obtener_codigo() for comp in self.computers_list]
        self.combo_computers["values"] = codes
        if codes:
            self.combo_computers.current(0)
        else:
            self.combo_computers.set("")

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


# ==========================================
# MAIN EXECUTION POINT
# ==========================================
if __name__ == "__main__":
    app = MaintenanceApp()
    app.mainloop()
    