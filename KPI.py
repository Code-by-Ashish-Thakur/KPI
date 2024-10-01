import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv")])
    
    if file_path:
        selected_file_label.config(text=file_path)
        submit_button.config(state=tk.NORMAL)

def process_csv(file_path, output_path):
    try:
        df = pd.read_csv(file_path)

        sum_values = df[['Total Voice Traffic', 'Total Data Traffic', 'SDCCH Drop Call Rate', 
                         'Drop Call Rate', 'RX Quality', 'RX Quality DL', 
                         'RX Quality UL', 'Handover Success Rate']].sum()

        short_count = df['Short name'].count()

        result = pd.DataFrame({
            'Column Name': ['Count of Short Names'] + [f'Sum of {col}' for col in sum_values.index],
            'Value': [short_count] + list(sum_values.values)
        })

        result.to_excel(output_path, index=False)

        messagebox.showinfo("Success", f"Output generated successfully:\n{output_path}")
        print(result)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit():
    file_path = selected_file_label.cget("text")
    if file_path:
        output_path = filedialog.asksaveasfilename(
            title="Save Output File",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")])
        
        if output_path:  # Check if the user selected a valid output path
            process_csv(file_path, output_path)

root = tk.Tk()
root.title("CSV File Processor")
root.geometry("400x200")  

open_file_button = tk.Button(root, text="Open CSV File", command=open_file_dialog)
open_file_button.pack(pady=10)

selected_file_label = tk.Label(root, text="No file selected")
selected_file_label.pack(pady=10)

submit_button = tk.Button(root, text="Submit", command=submit, state=tk.DISABLED)
submit_button.pack(pady=10)

root.mainloop()
