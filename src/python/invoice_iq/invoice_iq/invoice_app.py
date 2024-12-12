import typer
import os

from loguru import logger

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview

from PyPDF2 import PdfReader

from invoice_iq.config import TEMP_FILE_PATH, MODEL_TWO_PATH, MODEL_ONE_PATH
from invoice_iq.modeling import InvoiceDetector

app = typer.Typer()

class PDFUploaderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Invoice IQ")
        self.root.geometry("600x400")

        self._pdf_content = ""

        self.label = tk.Label(root, text="Upload a PDF File", font=("Arial", 14))
        self.label.pack(pady=20)

        self.upload_button = tk.Button(
            root, text="Upload PDF", command=self.upload_pdf, font=("Arial", 12)
        )
        self.upload_button.pack(pady=10)

        self.read_button = tk.Button(
            root, text="Read PDF", command=self.read_pdf, font=("Arial", 12), state=tk.DISABLED
        )
        self.read_button.pack(pady=10)

        self.output_button = tk.Button(
            root, text="Recognized Invoice", command=self.model_output, font=("Arial", 12), state=tk.DISABLED
        )
        self.output_button.pack(pady=10)

    def upload_pdf(self):
        # Open file dialog to select a PDF file
        file_path = filedialog.askopenfilename(
            title="Select a PDF File", filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.pdf_path = file_path
            messagebox.showinfo("File Selected", f"File selected: {file_path}")
            self.read_button.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("No File", "No file was selected!")

    def read_pdf(self):
        if hasattr(self, "pdf_path"):
            if os.path.exists(TEMP_FILE_PATH):
                self._pdf_content = ""
                os.remove(TEMP_FILE_PATH)
            logger.info("Old temp file removed")
            try:
                reader = PdfReader(self.pdf_path)
                for page in reader.pages:
                    self._pdf_content += page.extract_text()
                messagebox.showinfo("Success", "PDF content successfully read!")
                self._save_temp_file()
                self.output_button.config(state=tk.NORMAL)
            except Exception as e:
                logger.error(e)
                messagebox.showerror("Error", f"Failed to read PDF: {str(e)}")
        else:
            messagebox.showwarning("No File", "Please upload a file first.")

    def _save_temp_file(self):
        """
        Save the content of the PDF uploaded by the user to a temp text file.
        """
        with open(TEMP_FILE_PATH, "w") as f:
            f.seek(0)
            f.write(self._pdf_content)
            logger.info("PDF content stored in temp file")

    def create_table_output(self, table_data):
        """
        Create a table output of the detected invoice parameters.
        """
        entities = ["INVOICE_NO","DATE_OF_ISSUE","SELLER","BUYER","Net_worth","Gross_worth","order_id","IBAN"]
        table_window = tk.Toplevel(self.root)
        table_window.title("Recognized Invoice")
        table_window.geometry("500x300")
        tree = Treeview(root, columns=("Entities", "Values"), show="headings", height=len(entities))

        # Configure the columns
        tree.heading("Entities", text="Entities")
        tree.heading("Values", text="Values")
        tree.column("Entities", width=150, anchor="center")
        tree.column("Values", width=150, anchor="center")
        
        entities_dict =dict()    
        for data in table_data:
            entities_dict.update({data.label_:data.text})
            
        # Populate the table
        for entity in entities:
            value = entities_dict.get(entity, "NA")  # Get value or default to "NA"
            tree.insert("", tk.END, values=(entity, value))

        # Pack the Treeview
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def model_output(self):
        """
        Get the model output of the invoice file parameters.
        """
        logger.info(f"Model path : {MODEL_ONE_PATH}")
        invoice_inst = InvoiceDetector(MODEL_ONE_PATH)
        ai_output = invoice_inst.predict()

        # Ensure ai_output is a list of tuples or lists to display in the table
        self.create_table_output(ai_output)
        logger.success("Output table created")
        messagebox.showinfo("Processing Result", "Invoice parameters displayed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFUploaderApp(root)
    root.mainloop()
