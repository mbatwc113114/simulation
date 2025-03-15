import customtkinter as ctk

def open_window(parent_window):
    child = ctk.CTkToplevel()
    child.title("Child Window")
    child.geometry("400x300")

    def back_to_parent():
        child.destroy()
        parent_window.deiconify()  # Show parent window again

    btn_back = ctk.CTkButton(child, text="Back to Parent", command=back_to_parent)
    btn_back.pack(pady=20)
