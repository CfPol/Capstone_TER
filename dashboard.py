import os
import sys
import customtkinter
import tkinter
from tkinter import messagebox, filedialog
from PIL import Image, ExifTags
import cv2
import numpy as np
from tkinterdnd2 import DND_FILES, TkinterDnD  # requires: pip install tkinterdnd2
import main  # This module should define process_sections(img)

# Global variable to hold processed results.
processed_results = None

# Colors
MAROON = "#800000"
GOLD = "#FFD700"
WHITE = "#FFFFFF"

# Helper function to get absolute path to a resource.
def resource_path(relative_path):
    """
    Get absolute path to resource, works for development and for PyInstaller.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def fix_orientation(pil_img):
    try:
        exif = pil_img._getexif()
        if exif is None:
            return pil_img

        # Find the orientation tag
        for tag, value in ExifTags.TAGS.items():
            if value == 'Orientation':
                orientation_tag = tag
                break

        orientation = exif.get(orientation_tag, None)
        if orientation == 3:
            pil_img = pil_img.rotate(180, expand=True)
        elif orientation == 6:
            pil_img = pil_img.rotate(270, expand=True)
        elif orientation == 8:
            pil_img = pil_img.rotate(90, expand=True)
    except Exception as e:
        print("Error fixing orientation:", e)
    return pil_img

# Load icon safely using absolute paths.
def load_icon(path, size):
    try:
        abs_path = resource_path(path)
        return customtkinter.CTkImage(Image.open(abs_path), size=size)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def open_dashboard(app):
    global processed_results
    app.destroy()

    # Create the dashboard window using TkinterDnD.Tk for drag-and-drop support.
    dashboard = TkinterDnD.Tk()
    dashboard.title("CNSC TER | Dashboard")
    dashboard.configure(bg=MAROON)
    dashboard.after(10, lambda: dashboard.state("zoomed"))

    # Sidebar
    sidebar = customtkinter.CTkFrame(master=dashboard, width=260, fg_color=MAROON, corner_radius=0)
    sidebar.pack(side="left", fill="y")

    # CNSC Logo using resource_path.
    try:
        sidebar_logo = customtkinter.CTkImage(
            light_image=Image.open(resource_path("assets/cnsc.jpg")),
            dark_image=Image.open(resource_path("assets/cnsc.jpg")),
            size=(60, 60)
        )
    except Exception as e:
        print(f"Error loading cnsc.jpg: {e}")
        sidebar_logo = None

    logo = customtkinter.CTkLabel(master=sidebar, image=sidebar_logo, text="", bg_color=MAROON)
    logo.pack(pady=(30, 20))

    # Button Icons
    icons = {
        "Home": load_icon("assets/home.png", (20, 20)),
        "Scan": load_icon("assets/scan.png", (20, 20)),
        "Print": load_icon("assets/print.png", (20, 20)),
        "Results": load_icon("assets/result.png", (20, 20)),
        "Logout": load_icon("assets/logout.png", (20, 20)),
    }

    # Content Area: Create a frame for content.
    content_frame = customtkinter.CTkFrame(master=dashboard, fg_color=WHITE, corner_radius=12)
    content_frame.place(relx=0.23, rely=0.13, relwidth=0.74, relheight=0.8)

    # Default content for non-scan pages.
    default_label = customtkinter.CTkLabel(
        master=content_frame,
        text="Home Page",
        font=('Montserrat', 24, 'bold'),
        text_color=MAROON
    )
    default_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # Function to open file dialog and process image.
    def select_image():
        global processed_results
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            try:
                pil_img = Image.open(file_path)
                pil_img = fix_orientation(pil_img)
                
                # Optionally, resize the image if needed.
                cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                resized = cv2.resize(cv_img, (800, 1000))
                
                # Call the main function to process the image.
                processed_results = main.process_sections(resized)
                # Update the content area with a success message.
                for widget in content_frame.winfo_children():
                    widget.destroy()
                result_label = customtkinter.CTkLabel(
                    master=content_frame,
                    text="Image processed successfully! Go to the Results page to view output.",
                    font=('Montserrat', 20),
                    text_color=MAROON
                )
                result_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load/process image: {e}")

    # Function to switch content.
    def show_content(name):
        # Clear current content in content_frame.
        for widget in content_frame.winfo_children():
            widget.destroy()
        if name == "Scan":
            # Show a "Select Image" button.
            select_btn = customtkinter.CTkButton(
                master=content_frame,
                text="Select Image",
                font=('Montserrat', 20),
                fg_color=MAROON,
                text_color=WHITE,
                hover_color="#660000",
                command=select_image
            )
            select_btn.pack(expand=True, fill="both", padx=20, pady=20)
        elif name == "Results":
            global processed_results
            if processed_results is not None:
                # Define your section titles and questions
                section_titles = {
                    "Section 1": "Commitment",
                    "Section 2": "Knowledge of Subject",
                    "Section 3": "Teaching for Independent Learning",
                    "Section 4": "Management of Learning"
                }
                section_questions = {
                    "Section 1": {
                        1: "demonstrate sensitivity to students' ability to attend and absorb content information",
                        2: "exhibit readiness and enthusiasm for professional development",
                        3: "display consistency in teaching methodology",
                        4: "adapt teaching to meet student needs",
                        5: "engage students with diverse learning styles"
                    },
                    "Section 2": {
                        1: "present subject matter with clarity",
                        2: "use relevant examples and explanations",
                        3: "integrate current research into teaching",
                        4: "demonstrate mastery of core content",
                        5: "address questions effectively"
                    },
                    "Section 3": {
                        1: "encourage independent inquiry",
                        2: "provide effective feedback",
                        3: "support collaborative learning",
                        4: "promote critical thinking",
                        5: "use technology to enhance learning"
                    },
                    "Section 4": {
                        1: "organize classroom effectively",
                        2: "manage time efficiently",
                        3: "set clear learning objectives",
                        4: "maintain a positive classroom climate",
                        5: "evaluate student progress fairly"
                    }
                }
                
                # Build a display string for the results.
                display_text = ""
                for sec, data in processed_results.items():
                    title = section_titles.get(sec, sec)
                    display_text += f"{title}:\n"
                    # Assume your process_sections function stores row scores in data['row_scores']
                    row_scores = data.get("row_scores", {})
                    for row in sorted(row_scores.keys()):
                        question_text = section_questions.get(sec, {}).get(row, f"Row {row}")
                        display_text += f"{row}. {question_text}: {row_scores[row]}\n"
                    display_text += f"Total Score: {data.get('total_score', 'N/A')}\n\n"
                
                results_textbox = customtkinter.CTkTextbox(
                    master=content_frame,
                    font=('Montserrat', 24),
                    text_color="#000000",
                    fg_color=WHITE,
                    bg_color=WHITE
                )
                results_textbox.pack(expand=True, fill="both", padx=20, pady=20)
                results_textbox.insert("0.0", display_text)
            else:
                no_result_label = customtkinter.CTkLabel(
                    master=content_frame,
                    text="No results available.\nPlease scan an image first.",
                    font=('Montserrat', 20),
                    text_color=MAROON
                )
                no_result_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        else:
            content_label = customtkinter.CTkLabel(
                master=content_frame,
                text=f"{name} Page is still under development",
                font=('Montserrat', 24, 'bold'),
                text_color=MAROON
            )
            content_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # Navigation Buttons
    nav_items = ["Home", "Scan", "Print", "Results"]
    for item in nav_items:
        btn = customtkinter.CTkButton(
            master=sidebar,
            text=item,
            image=icons[item],
            compound="left",
            width=160,
            font=('Montserrat', 14),
            fg_color=WHITE,
            text_color=MAROON,
            hover_color="#f0e68c",
            command=lambda name=item: show_content(name)
        )
        btn.pack(pady=10, padx=20, anchor="center")

    # Logout confirmation and Logout Button
    def confirm_logout():
        response = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
        if response:
            dashboard.destroy()

    logout_btn = customtkinter.CTkButton(
        master=sidebar,
        text="Logout",
        image=icons["Logout"],
        compound="left",
        width=160,
        font=('Montserrat', 14),
        fg_color=WHITE,
        text_color=MAROON,
        hover_color="#f0e68c",
        command=confirm_logout
    )
    logout_btn.pack(pady=30, padx=20, side="bottom", anchor="center")

    # Topbar
    topbar = customtkinter.CTkFrame(master=dashboard, height=60, fg_color=WHITE, corner_radius=0)
    topbar.pack(side="top", fill="x")

    top_title = customtkinter.CTkLabel(
        master=topbar,
        text="Welcome to CNSC TER Dashboard",
        font=('Montserrat', 18, 'bold'),
        text_color=MAROON
    )
    top_title.place(relx=0.02, rely=0.5, anchor=tkinter.W)

    dashboard.mainloop()

# To launch the dashboard, call open_dashboard() with your current app instance.
if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Login")  # Dummy login window for testing.
    open_dashboard(root)
