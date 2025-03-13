import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import logging
import sys

from main import PostaAPIClient, ExcelProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

class PostaTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Balikovna Tracking Status Checker")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')  # Light gray background
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Modern looking theme
        
        # Configure custom styles
        self.style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('Custom.TButton', font=('Helvetica', 10), padding=10)
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Status.TLabel', font=('Helvetica', 10))
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Balikovna Tracking Status Checker", 
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Excel File:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=80)
        self.file_entry.grid(row=0, column=1, padx=10)
        browse_btn = ttk.Button(
            file_frame, 
            text="Browse", 
            command=self.browse_file, 
            style='Custom.TButton'
        )
        browse_btn.grid(row=0, column=2)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding="10")
        progress_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=200
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(5, 10))
        
        self.status_label = ttk.Label(
            progress_frame, 
            text="Ready to process", 
            style='Status.TLabel'
        )
        self.status_label.grid(row=1, column=0)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.main_frame, text="Processing Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview with custom style
        self.style.configure("Treeview", font=('Helvetica', 10))
        self.style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        self.tree = ttk.Treeview(
            results_frame, 
            columns=('tracking', 'status', 'date', 'action'), 
            show='headings',
            height=15
        )
        
        # Configure column widths and headings
        self.tree.column('tracking', width=150)
        self.tree.column('status', width=250)
        self.tree.column('date', width=150)
        self.tree.column('action', width=300)
        
        self.tree.heading('tracking', text='Tracking Number')
        self.tree.heading('status', text='Status')
        self.tree.heading('date', text='Last Update')
        self.tree.heading('action', text='Action Required')
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Control buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.start_button = ttk.Button(
            button_frame, 
            text="Start Processing", 
            command=self.start_processing,
            style='Custom.TButton'
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.cancel_button = ttk.Button(
            button_frame, 
            text="Cancel", 
            command=self.cancel_processing,
            state=tk.DISABLED,
            style='Custom.TButton'
        )
        self.cancel_button.grid(row=0, column=1, padx=5)
        
        # Status bar
        self.status_bar = ttk.Label(
            self.main_frame, 
            text="Ready", 
            relief=tk.SUNKEN, 
            style='Status.TLabel'
        )
        self.status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Processing state
        self.processing = False
        self.success_count = 0
        self.error_count = 0

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if filename:
            self.file_path.set(filename)

    def update_progress(self, current, total, message=""):
        progress = (current / total) * 100
        self.progress_var.set(progress)
        status_text = f"Processing: {current}/{total} ({progress:.1f}%) - {message}"
        self.status_label.config(text=status_text)
        self.root.update_idletasks()

    def start_processing(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select an Excel file first")
            return
            
        self.processing = True
        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.tree.delete(*self.tree.get_children())
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_file)
        thread.daemon = True
        thread.start()

    def cancel_processing(self):
        self.processing = False
        self.status_label.config(text="Processing cancelled")
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)

    def process_file(self):
        try:
            excel_processor = ExcelProcessor(self.file_path.get())
            api_client = PostaAPIClient()
            
            df = excel_processor.read_tracking_numbers()
            total_records = len(df)
            
            df['Stav'] = None
            df['Last Update'] = None
            df['Action Required'] = None
            
            for idx, row in df.iterrows():
                if not self.processing:
                    break
                    
                tracking_number = row['Tracking Number']
                self.update_progress(idx + 1, total_records, f"Processing {tracking_number}")
                
                try:
                    result = api_client.get_parcel_status(tracking_number)
                    
                    if result and not result.get('error'):
                        status = result['status']
                        date = result['date']
                        action = ""
                        
                        if status == "Receipt of data about consignment before posting.":
                            action = "The parcel has not been handed over for transport"
                            
                        df.at[idx, 'Stav'] = status
                        df.at[idx, 'Last Update'] = date
                        df.at[idx, 'Action Required'] = action
                        
                        self.tree.insert('', 'end', values=(tracking_number, status, date, action))
                        self.success_count += 1
                    else:
                        error_msg = result.get('error') if result else 'No result'
                        df.at[idx, 'Action Required'] = "Failed to get status"
                        self.tree.insert('', 'end', values=(tracking_number, "Error", "", error_msg))
                        self.error_count += 1
                        
                except Exception as e:
                    logger.error(f"Error processing {tracking_number}: {str(e)}")
                    self.error_count += 1
                    
                # Save progress every 10 records
                if (idx + 1) % 10 == 0:
                    excel_processor.write_results(df, None)
            
            # Final save
            if self.processing:
                excel_processor.write_results(df, None)
                messagebox.showinfo("Complete", 
                    f"Processing complete!\nSuccessful updates: {self.success_count}\nFailed updates: {self.error_count}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
            logger.error(f"Processing failed: {str(e)}")
        
        finally:
            self.processing = False
            self.start_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
            self.status_label.config(text="Ready")

def main():
    root = tk.Tk()
    app = PostaTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 