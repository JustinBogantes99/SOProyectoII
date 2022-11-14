import tkinter as tk
 
import tksheet
 
top = tk.Tk()
 
sheet = tksheet.Sheet(top)
 
sheet.grid()
 
sheet.insert_column(values=["AAA", "BCCC", "CEEE"])
 
sheet.set_sheet_data([[f"{ri+cj}" for cj in range(4)] for ri in range(20)])
 
# table enable choices listed below:
 
sheet.enable_bindings(("single_select",
 
                      "row_select",
 
                      "column_width_resize",
 
                      "arrowkeys",
 
                      "right_click_popup_menu"))
 
top.mainloop()