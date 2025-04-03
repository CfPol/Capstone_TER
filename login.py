import tkinter
import customtkinter
from PIL import Image
from dashboard import open_dashboard  # 👈 Import from the other file

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("600x440")
app.title('CNSC TER')

MAROON = "#800000"
GOLD = "#FFD700"
WHITE = "#FFFFFF"

app.configure(bg=MAROON)

# Improved Login Frame UI
frame = customtkinter.CTkFrame(master=app, width=360, height=420, corner_radius=20, fg_color=WHITE)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# CNSC logo
small_logo = customtkinter.CTkImage(
    light_image=Image.open("./assets/cnsc.jpg"),
    dark_image=Image.open("./assets/cnsc.jpg"),
    size=(60, 60)
)
logo_label = customtkinter.CTkLabel(master=frame, image=small_logo, text="")
logo_label.place(x=150, y=20)

# Login Title
l2 = customtkinter.CTkLabel(master=frame, text="LOGIN", font=('Segoe UI', 24, 'bold'), text_color=MAROON)
l2.place(relx=0.5, y=90, anchor=tkinter.CENTER)

# Username Entry
entry1 = customtkinter.CTkEntry(master=frame, width=260, height=40, placeholder_text='Username', font=('Montserrat', 13))
entry1.place(relx=0.5, y=150, anchor=tkinter.CENTER)

# Password Entry
entry2 = customtkinter.CTkEntry(master=frame, width=260, height=40, placeholder_text='Password', show="*", font=('Montserrat', 13))
entry2.place(relx=0.5, y=200, anchor=tkinter.CENTER)

# Forget Password
l3 = customtkinter.CTkLabel(master=frame, text="Forgot password?", font=('Montserrat', 12), text_color="gray")
l3.place(relx=0.85, y=235, anchor=tkinter.E)

# Login Button
button1 = customtkinter.CTkButton(master=frame, width=260, height=40, text="Login", command=lambda: open_dashboard(app),
                                  font=('Montserrat', 14), corner_radius=8,
                                  fg_color=MAROON, hover_color="#660000", text_color=WHITE)
button1.place(relx=0.5, y=290, anchor=tkinter.CENTER)

app.mainloop()
