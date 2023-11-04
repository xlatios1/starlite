from tools.encryption import Encryption

import tkinter as tk
from tkinter import messagebox

def set_encrypted_account(encryption: Encryption, username:str=None, password:str=None):  
    if username and password: 
        encryption.encrypt_and_save_data(f"{username.strip()}, {password.strip()}")
    else:
        def set_account():
            if not entry_username.get().strip(): 
                messagebox.showerror("Invalid Input", "Username field is empty.")
            elif not entry_password.get().strip(): 
                messagebox.showerror("Invalid Input", "Password field is empty.")
            else:
                encryption.encrypt_and_save_data(
                    f"{entry_username.get()}, {entry_password.get()}" 
                )
                account_window.destroy()

        account_window = tk.Tk()
        account_window.title("Login")
        
        label_username = tk.Label(account_window, text="Pls enter your NTU Account")
        label_username = tk.Label(account_window, text="Username:")
        label_password = tk.Label(account_window, text="Password:")
        entry_username = tk.Entry(account_window, width=20)
        entry_password = tk.Entry(account_window, width=20, show="*")  # Hide password characters
        set_account_btn = tk.Button(account_window, text="set account", command=set_account)
        
        label_username.grid(row=0, sticky="w")
        entry_username.grid(row=0, padx=60, pady=5, sticky="w")
        label_password.grid(row=1, sticky="w")
        entry_password.grid(row=1, padx=60, pady=5, sticky="w")
        set_account_btn.grid(row=2, sticky="w", padx=115)
        account_window.geometry('200x90')
        account_window.mainloop()
        
        
        
        # # A new account
        # def set_new_account():
        #     def set_account():
        #         if not entry_username.get().strip(): 
        #             messagebox.showerror("Invalid Input", "Username field is empty.")
        #         elif not entry_password.get().strip(): 
        #             messagebox.showerror("Invalid Input", "Password field is empty.")
        #         else:
        #             encryption.set_key(key_entry.get())
        #             if encryption.check_if_exists(): encryption.remove_saved_datas()
        #             encryption.encrypt_and_save_data(
        #                 f"{entry_username.get()}, {entry_password.get()}" 
        #             )
        #             root.destroy()
            
        #     if key_entry.get().strip():
        #         account_window = tk.Toplevel(root)
        #         account_window.title("Set account")

        #         label_username = tk.Label(account_window, text="Username:")
        #         label_password = tk.Label(account_window, text="Password:")
        #         entry_username = tk.Entry(account_window, width=20)
        #         entry_password = tk.Entry(account_window, width=20, show="*")  # Hide password characters
        #         # remember_me_cfm = tk.Checkbutton(account_window, text='Save key?', variable=remember_me_var)
        #         set_account_btn = tk.Button(account_window, text="set account", command=set_account)
                
        #         label_username.grid(row=0, sticky="w")
        #         entry_username.grid(row=0, padx=60, pady=5, sticky="w")
        #         label_password.grid(row=1, sticky="w")
        #         entry_password.grid(row=1, padx=60, pady=5, sticky="w")
        #         # remember_me_cfm.grid(row=2, sticky="w", padx=55)
        #         set_account_btn.grid(row=2, sticky="w", padx=115)
        #         # account_window.geometry('200x115')
        #         account_window.geometry('200x90')
        #     else:
        #         messagebox.showerror("Invalid Input", "Key field is empty.")
                
        # def get_account():
        #     if key_entry.get().strip():
        #         if encryption.check_if_exists():
        #             encryption.set_key(key_entry.get())
        #             root.destroy()
        #         else:
        #             messagebox.showerror("Oops!", "Account is not found, please set one.")
        #     else:
        #         messagebox.showerror("Invalid Input", "Key field is empty.")
            
        # root = tk.Tk()
        # root.title("Get/Set key")
        # # remember_me_var = tk.IntVar()
        
        # label = tk.Label(root, text="Input Key:")
        # key_entry = tk.Entry(root, show="*",width=12)  # Use "*" to hide the password
        # key_entry.focus_set
        # # remember_me = tk.Checkbutton(root, text='Save key?', variable=remember_me_var)
        # get_account_button = tk.Button(root, text="Get Account", command=get_account)
        # set_account_button = tk.Button(root, text="Set Key", command=set_new_account)

        # label.grid(row=0,sticky='w')
        # key_entry.grid(row=0,sticky='w',padx=65,pady=5)
        # # remember_me.grid(row=2, sticky='w', padx=60, pady=5)
        # get_account_button.grid(row=2, sticky='w', padx=5)
        # set_account_button.grid(row=2, sticky='w', padx=90, pady=5)
        # # root.geometry('150x100')
        # root.geometry('150x70')
        
        # root.mainloop()