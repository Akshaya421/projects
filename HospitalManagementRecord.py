//Hospital ManageMent Record
# ----------------- IMPORTS -----------------
import tkinter as tk  # GUI components
from tkinter import messagebox, simpledialog  # Popups & dialogs for alerts and input
import os  # File system operations

# ----------------- FILE CONFIG -----------------
FILENAME = "patients.txt"  # Text file used to store patient records

# ----------------- FILE OPERATIONS -----------------

# Function to read patient records from the file
def read_patients():
    if not os.path.exists(FILENAME):  # If the file doesn't exist yet
        return []  # Return empty list
    with open(FILENAME, "r") as file:
        return [line.strip().split(",") for line in file.readlines()]  # Each line is split by commas into a list

# Function to write (overwrite) patient records into the file
def write_patients(patients):
    with open(FILENAME, "w") as file:  # Opens file in write mode (overwrites old content)
        for p in patients:
            file.write(",".join(p) + "\n")  # Join each patient record list with commas and write it to file

# ----------------- FUNCTIONALITY -----------------

# Function to add a new patient to file and update display
def add_patient():
    # Get the values from form inputs
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    phone = phone_entry.get().strip()
    gender = gender_var.get()
    illness = illness_entry.get().strip()
    bill_paid = bill_paid_var.get()
    consultant_fee = "300"  # Fixed consultant fee

    # Validate required fields
    if not name or not age or not phone or not illness:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    # Write new patient record to the file
    with open(FILENAME, "a") as file:  # Open in append mode to add new record
        file.write(f"{name},{age},{phone},{gender},{illness},{consultant_fee},{bill_paid}\n")

    messagebox.showinfo("Success", "Patient record added.")
    clear_fields()  # Clear the form fields after adding
    refresh_display()  # Update the listbox to show the new patient

# Refreshes the Listbox display with current patients
def refresh_display():
    patient_list.delete(0, tk.END)  # Clear all existing items
    for p in read_patients():
        patient_list.insert(tk.END, f"{p[0]} ({p[1]} yrs)")  # Add patient's name and age

# Displays full details of selected patient in popup
def show_selected():
    index = patient_list.curselection()
    if not index:
        return
    patient = read_patients()[index[0]]
    messagebox.showinfo("Patient Details",
        f"Name: {patient[0]}\nAge: {patient[1]}\nPhone: {patient[2]}\nGender: {patient[3]}"
        f"\nIllness: {patient[4]}\nConsultant Fee: ₹{patient[5]}\nBill Paid: {patient[6]}"
    )

# Searches patients by name
def search_patient():
    keyword = simpledialog.askstring("Search", "Enter patient name:")  # Prompt user
    if not keyword:
        return
    results = [p for p in read_patients() if keyword.lower() in p[0].lower()]  # Filter records by name match
    if results:
        # Format multiple results
        text = "\n\n".join([
            f"Name: {p[0]}\nAge: {p[1]}\nPhone: {p[2]}\nGender: {p[3]}"
            f"\nIllness: {p[4]}\nFee: ₹{p[5]}\nBill Paid: {p[6]}"
            for p in results
        ])
        messagebox.showinfo("Search Results", text)
    else:
        messagebox.showinfo("Search Results", "No patient found.")

# Deletes the selected patient from file
def delete_patient():
    index = patient_list.curselection()  # Get selected index
    if not index:
        messagebox.showwarning("Select Patient", "Please select a patient to delete.")
        return
    patients = read_patients()
    selected = patients[index[0]]
    # Confirm deletion
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected[0]}?")
    if confirm:
        del patients[index[0]]  # Remove selected patient
        write_patients(patients)  # Save updated list
        messagebox.showinfo("Deleted", f"Deleted patient: {selected[0]}")
        refresh_display()  # Refresh display

# Updates the selected patient by prompting for new details
def update_patient():
    index = patient_list.curselection()
    if not index:
        messagebox.showwarning("Select Patient", "Select a patient to update.")
        return
    patients = read_patients()
    selected = patients[index[0]]

    # Prompt for updated values with existing ones pre-filled
    new_name = simpledialog.askstring("Update", "New Name:", initialvalue=selected[0])
    new_age = simpledialog.askstring("Update", "New Age:", initialvalue=selected[1])
    new_phone = simpledialog.askstring("Update", "New Phone:", initialvalue=selected[2])
    new_gender = simpledialog.askstring("Update", "Gender:", initialvalue=selected[3])
    new_illness = simpledialog.askstring("Update", "Illness:", initialvalue=selected[4])
    new_bill_paid = simpledialog.askstring("Update", "Bill Paid (Yes/No):", initialvalue=selected[6])

    # Validate input
    if not new_name or not new_age or not new_phone or not new_gender or not new_illness or not new_bill_paid:
        messagebox.showerror("Invalid Input", "All fields must be filled.")
        return

    # Update record
    patients[index[0]] = [new_name, new_age, new_phone, new_gender, new_illness, "300", new_bill_paid]
    write_patients(patients)
    messagebox.showinfo("Updated", "Patient record updated successfully.")
    refresh_display()

# Clears the input form fields
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    illness_entry.delete(0, tk.END)
    gender_var.set("Male")  # Reset to default
    bill_paid_var.set("No")  # Reset to default

# ----------------- GUI SETUP -----------------

root = tk.Tk()  # Create the main window
root.title("Hospital Management System")  # Title of the window
root.geometry("500x720")  # Size of the window
root.config(bg="#e6f2ff")  # Set background color to light blue

# Font and color styling
label_font = ("Arial", 12)
entry_bg = "#ffffff"  # White entry boxes
button_bg = "#4CAF50"  # Green button background
button_fg = "white"  # White text on buttons

# Main heading
tk.Label(root, text="Patient Details", font=("Arial", 16, "bold"), bg="#e6f2ff", fg="#333").pack(pady=10)

# Form Fields
for label in ["Name", "Age", "Phone Number", "Illness"]:
    tk.Label(root, text=label, font=label_font, bg="#e6f2ff").pack()  # Create label
    entry = tk.Entry(root, bg=entry_bg)  # Create entry input field
    entry.pack()
    # Save entry widgets to global variables
    if label == "Name":
        name_entry = entry
    elif label == "Age":
        age_entry = entry
    elif label == "Phone Number":
        phone_entry = entry
    elif label == "Illness":
        illness_entry = entry

# Gender selection (radio buttons)
tk.Label(root, text="Gender", font=label_font, bg="#e6f2ff").pack()
gender_var = tk.StringVar(value="Male")  # Default gender
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male", bg="#e6f2ff").pack(anchor="w")
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female", bg="#e6f2ff").pack(anchor="w")

# Bill Paid selection (radio buttons)
tk.Label(root, text="Bill Paid", font=label_font, bg="#e6f2ff").pack()
bill_paid_var = tk.StringVar(value="No")  # Default bill status
tk.Radiobutton(root, text="Yes", variable=bill_paid_var, value="Yes", bg="#e6f2ff").pack(anchor="w")
tk.Radiobutton(root, text="No", variable=bill_paid_var, value="No", bg="#e6f2ff").pack(anchor="w")

# Button to add patient
tk.Button(root, text="Add Patient", command=add_patient, bg=button_bg, fg=button_fg).pack(pady=5)

# Patient list heading
tk.Label(root, text="Patient Records", font=("Arial", 14), bg="#e6f2ff", fg="#333").pack(pady=10)

# Listbox to display patient names and ages
patient_list = tk.Listbox(root, width=50)
patient_list.pack(pady=5)

# Buttons for operations: Show, Search, Update, Delete
buttons = [
    ("Show Details", show_selected),
    ("Search Patient", search_patient),
    ("Update Patient", update_patient),
    ("Delete Patient", delete_patient)
]
for text, command in buttons:
    tk.Button(root, text=text, command=command, bg="#2196F3", fg="white").pack(pady=3)

# Load patients into listbox on app start
refresh_display()

# Run the GUI loop (wait for user interaction)
root.mainloop()

