import tkinter as tk
from tkinter import ttk, messagebox
import pickle, os
from datetime import datetime

# === Employee Classes ===
class Employee:
    def __init__(self, eid, name, doj, end_date):
        self.eid, self.name = eid, name
        self.doj = doj
        self.end = end_date

    def calculate_salary(self): return 0

    def get_details(self):
        return (f"{self.eid} | {self.name} | {self.__class__.__name__} | "
                f"Joined: {self.doj} | Ends: {self.end} | ₹{self.calculate_salary():.2f}")

class FullTime(Employee):
    def __init__(self, eid, name, doj, end, salary):
        super().__init__(eid, name, doj, end)
        self.salary = float(salary)

    def calculate_salary(self): return self.salary

class PartTime(Employee):
    def __init__(self, eid, name, doj, end, hours, rate):
        super().__init__(eid, name, doj, end)
        self.h, self.r = float(hours), float(rate)

    def calculate_salary(self): return self.h * self.r

class Manager(Employee):
    def __init__(self, eid, name, doj, end, base, bonus):
        super().__init__(eid, name, doj, end)
        self.b, self.bo = float(base), float(bonus)

    def calculate_salary(self): return self.b + self.bo

# === Application ===
class EMSApp:
    def __init__(self, root):
        self.root, self.file = root, "employees.pkl"
        self.root.title("Employee Management System")
        self.emps = self.load()
        self.build_ui()

    def build_ui(self):
        f = tk.LabelFrame(self.root, text="Employee Info")
        f.grid(row=0, column=0, padx=10, pady=5)

        labels = ["ID", "Name", "Type", "DOJ (YYYY-MM-DD)", "End Date (YYYY-MM-DD)", "Extra1", "Extra2"]
        self.entries = {}
        for i, lbl in enumerate(labels):
            tk.Label(f, text=lbl).grid(row=i, column=0)
            ent = ttk.Combobox(f, values=["FullTime", "PartTime", "Manager"], state="readonly") if lbl == "Type" else tk.Entry(f)
            ent.grid(row=i, column=1)
            self.entries[lbl] = ent

        tk.Button(f, text="Add", command=self.add).grid(row=7, column=0)
        tk.Button(f, text="Remove", command=self.remove).grid(row=7, column=1)

        sf = tk.LabelFrame(self.root, text="Search / Display")
        sf.grid(row=1, column=0, padx=10, pady=5)
        self.search = tk.Entry(sf); self.search.grid(row=0, column=1)
        tk.Label(sf, text="Search ID/Name").grid(row=0, column=0)
        tk.Button(sf, text="Search", command=self.search_emp).grid(row=0, column=2)
        tk.Button(sf, text="Show All", command=self.show_all).grid(row=1, column=0)
        tk.Button(sf, text="Total Payroll", command=self.payroll).grid(row=1, column=1)

        # self.out = tk.Text(self.root, width=85, height=14)
        # self.out.grid(row=2, column=0, padx=10, pady=10)
        self.out = tk.Text(self.root, width=130, height=25, font=("Consolas", 12))
        self.out.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Add scrollbar
        scroll = tk.Scrollbar(self.root, command=self.out.yview)
        scroll.grid(row=2, column=1, sticky='ns', pady=10)
        self.out.config(yscrollcommand=scroll.set)


    def add(self):
        try:
            d = {k: v.get().strip() for k, v in self.entries.items()}
            if any(e.eid == d["ID"] for e in self.emps):
                return messagebox.showerror("Error", "ID already exists")

            # Validate dates
            doj = datetime.strptime(d["DOJ (YYYY-MM-DD)"], "%Y-%m-%d").date()
            end = datetime.strptime(d["End Date (YYYY-MM-DD)"], "%Y-%m-%d").date()

            t = d["Type"]
            if t == "FullTime":
                emp = FullTime(d["ID"], d["Name"], doj, end, float(d["Extra1"]))
            elif t == "PartTime":
                emp = PartTime(d["ID"], d["Name"], doj, end, float(d["Extra1"]), float(d["Extra2"]))
            elif t == "Manager":
                emp = Manager(d["ID"], d["Name"], doj, end, float(d["Extra1"]), float(d["Extra2"]))
            else:
                raise ValueError("Select a valid employee type.")

            self.emps.append(emp)
            self.save()
            self.clear()
            messagebox.showinfo("Success", "Employee added.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def remove(self):
        eid = self.entries["ID"].get().strip()
        for emp in self.emps:
            if emp.eid == eid:
                self.emps.remove(emp); self.save()
                return messagebox.showinfo("Removed", "Employee removed.")
        messagebox.showwarning("Not Found", "Employee not found.")

    def show_all(self):
        self.out.delete(1.0, tk.END)
        for emp in self.emps: self.out.insert(tk.END, emp.get_details() + "\n")

    def search_emp(self):
        k = self.search.get().strip().lower()
        self.out.delete(1.0, tk.END)
        found = False
        for e in self.emps:
            if k in e.eid.lower() or k in e.name.lower():
                self.out.insert(tk.END, e.get_details() + "\n")
                found = True
        if not found: self.out.insert(tk.END, "No match found.\n")

    def payroll(self):
        total = sum(e.calculate_salary() for e in self.emps)
        self.out.insert(tk.END, f"\nTotal Payroll: ₹{total:.2f}\n")

    def save(self): pickle.dump(self.emps, open(self.file, "wb"))
    def load(self): return pickle.load(open(self.file, "rb")) if os.path.exists(self.file) else []
    def clear(self): [v.delete(0, tk.END) if isinstance(v, tk.Entry) else v.set("") for v in self.entries.values()]

# === Run ===
if __name__ == "__main__":
    root = tk.Tk()
    EMSApp(root)
    root.mainloop()
