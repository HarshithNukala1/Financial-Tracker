import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Transaction:
    def __init__(self, transaction_type, amount, description):
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description


class ExpensesIncomesTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Tracker")

        # Initialize variables
        self.transaction_var = tk.StringVar()
        self.total_incomes = tk.DoubleVar()
        self.total_expenses = tk.DoubleVar()
        self.total_balance = tk.DoubleVar()
        self.description = tk.StringVar()

        # Create the UI
        self.create_ui()

    def create_ui(self):
        # Create and pack the title label
        titleLabel = ttk.Label(self.root, text="FINANCIAL TRACKER",
                               font=("Arial", 16, "bold"), foreground="#003136")
        titleLabel.pack(pady=10)

        # Create and pack radio buttons for transaction type
        transactionRadioFrame = ttk.Frame(self.root)
        transactionRadioFrame.pack(pady=10)
        expenseRadio = ttk.Radiobutton(transactionRadioFrame, text="Expense",
                                       variable=self.transaction_var, value="Expense")

        incomeRadio = ttk.Radiobutton(transactionRadioFrame, text="Income",
                                      variable=self.transaction_var, value="Income")

        expenseRadio.grid(row=0, column=0, padx=10)
        incomeRadio.grid(row=0, column=1, padx=10)

        # Create and pack the frame for amount and description
        entryFrame = ttk.Frame(self.root)
        entryFrame.pack(pady=10)

        # Create amount label and entry
        amountLabel = ttk.Label(entryFrame, text="Amount: ", font=("Arial", 12),
                                foreground="#34495e")

        amountLabel.grid(row=0, column=0, padx=5)

        self.amountEntry = ttk.Entry(entryFrame, font=("Arial", 12))
        self.amountEntry.grid(row=0, column=1)

        # Create description label and entry
        descriptionLabel = ttk.Label(entryFrame, text="Description: ",
                                     font=("Arial", 12), foreground="#34495e")

        descriptionLabel.grid(row=0, column=2, padx=5)

        self.descriptionEntry = ttk.Entry(entryFrame, font=("Arial", 12))
        self.descriptionEntry.grid(row=0, column=3)

        # Create and pack the "Add Transaction" button
        addButton = tk.Button(self.root, text="Add Transaction", bg="#b0c3be",
                              fg="black", font=("Arial", 12, "bold"), width="22",
                              command=self.add_transaction)

        addButton.pack(pady=10)

        # Create and pack the frame for the lists of expenses and incomes
        listFrame = ttk.Frame(self.root)
        listFrame.pack()

        # Create Treeview with Scrollbar for expenses and incomes
        self.expenses_incomes_list = ttk.Treeview(listFrame,
                                                  columns=("Type", "Amount", "Description"), show="headings", height=5)

        self.expenses_incomes_list.heading("Type", text="Type")
        self.expenses_incomes_list.heading("Amount", text="Amount")
        self.expenses_incomes_list.heading("Description", text="Description")
        self.expenses_incomes_list.pack(side="right", padx=(0, 20), fill=tk.Y)

        # Scrollbar for expenses and incomes Treeview
        scrollbar = ttk.Scrollbar(listFrame, orient="vertical",
                                  command=self.expenses_incomes_list.yview)

        scrollbar.pack(side="left", padx=(20, 0), fill="y")
        self.expenses_incomes_list.config(yscrollcommand=scrollbar.set)

        # Create and pack the frame for displaying totals
        totalsFrame = ttk.Frame(self.root)
        totalsFrame.pack(pady=10)

        total_expenses_label = ttk.Label(totalsFrame, text="Total Expenses: ",
                                         font=("Arial", 12, "bold"), foreground="#003136")

        total_expenses_label.grid(row=0, column=0, padx=0)

        self.total_expenses_display = ttk.Label(totalsFrame,
                                                textvariable=self.total_expenses, font=("Arial", 12, "bold"),
                                                foreground="#003136")

        self.total_expenses_display.grid(row=0, column=1, padx=(0, 20))

        total_incomes_label = ttk.Label(totalsFrame, text="Total Incomes: ",
                                        font=("Arial", 12, "bold"), foreground="#003136")

        total_incomes_label.grid(row=0, column=2, padx=0)

        self.total_incomes_display = ttk.Label(totalsFrame,
                                               textvariable=self.total_incomes, font=("Arial", 12, "bold"),
                                               foreground="#003136")

        self.total_incomes_display.grid(row=0, column=3, padx=(0, 20))

        total_balance_label = ttk.Label(totalsFrame, text="Balance: ",
                                        font=("Arial", 12, "bold"), foreground="#003136")

        total_balance_label.grid(row=0, column=4, padx=0)

        self.total_balance_display = ttk.Label(totalsFrame,
                                               textvariable=self.total_balance, font=("Arial", 12, "bold"),
                                               foreground="#003136")

        self.total_balance_display.grid(row=0, column=5, padx=(0, 20))

    def add_transaction(self):
        # Get transaction type, amount, and description from the UI
        transaction_type = self.transaction_var.get()
        amount_entry_text = self.amountEntry.get()
        description_entry_text = self.descriptionEntry.get()

        try:
            amount = float(amount_entry_text)
        except ValueError:
            self.show_error_message("Invalid amount. Please enter a numeric value.")
            return

        if not amount_entry_text or amount <= 0:
            self.show_error_message("Amount cannot be empty or non-positive")
            return

        if not transaction_type:
            self.show_error_message("Please select a transaction type")
            return

        # Create a Transaction object and update UI
        transaction = Transaction(transaction_type, amount_entry_text,
                                  description_entry_text)

        self.expenses_incomes_list.insert("", "end", values=(transaction_type,
                                                             amount_entry_text, description_entry_text))

        if transaction_type == "Expense":
            self.total_expenses.set(self.total_expenses.get() + amount)

        else:
            self.total_incomes.set(self.total_incomes.get() + amount)

        self.total_balance.set(self.total_incomes.get() - self.total_expenses.get())

        # Clear entries
        self.amountEntry.delete(0, "end")
        self.descriptionEntry.delete(0, "end")

    def show_error_message(self, message):
        tk.messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpensesIncomesTracker(root)
    root.mainloop()
