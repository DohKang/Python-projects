import tkinter as tk
import math
import tkinter.messagebox as msgbox


GGRAY="#a8a897"
WHITE = "#FFFFFF"
ORANGE = "#f0c51a"

TOP_D_LABEL_FONT = ("Arial", 12)
D_LABEL_FONT = ("Arial", 17)
BTN_FONT = ("Arial", 12, "bold")
SPECIAL_BTN_FONT = ("Arial", 12, "bold", "italic")
INTRO_FONT = ("Arial", 7)
OPERATOR_FONT = ("Arial", 12)

class Calculator():
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("350x450+700+350")
        self.window.resizable(False, True)
        self.window.title("DK_Calculator")
        self.entire_frame = self.create_entire_frame()
        self.display_frame = self.create_display_frame()
        self.total_expression = ""
        self.current_expression = ""
        self.total_label, self.current_label = self.create_display_label()
        self.button_frame = self.create_button_frame()
        self.digits = {
            7:(2,2), 8:(2,3), 9:(2,4),
            4:(3,2), 5:(3,3), 6:(3,4),
            1:(4,2), 2:(4,3), 3:(4,4),
            0:(5,3), ".":(5,2)
        }
        self.digit_buttons = self.create_digit_buttons()
        #special buttons

        self.clear_button = self.create_C_button()
        self.pie_button = self.create_pie_button()
        self.power_button = self.create_power_button()
        self.sqrt_button = self.create_sqrt_button()
        self.oprths_button = self.create_oprths_button()
        self.cprths_buttton = self.create_cprths_button()
        self.button = self.create_enter_button()
        self.operations = {"/": "/", "*": "*", "-": "-", "+": "+"}
        self.operations = self.create_operation_button()
        #intro button
        self.intro_button = self.create_into_button()
        for x in range(1, 6):
            self.button_frame.rowconfigure(x, weight=1)
            self.button_frame.columnconfigure(x, weight=1)

        self.menu = tk.Menu(self.window)
        self.first_menu = self.create_first_menu()
        self.window.config(menu=self.menu)
        self.binding_keys()


    # FRAME WORK
    def create_entire_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame


    def create_display_frame(self):
        d_frame = tk.Frame(self.entire_frame, height=250)
        d_frame.pack(expand=True, fill="both")
        return d_frame

    def create_button_frame(self):
        btn_frame = tk.Frame(self.entire_frame, height= 200, bg=WHITE)
        btn_frame.pack(expand=True, fill="both")
        return btn_frame

    #Total_expressionm, current_expression Label
    def create_display_label(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor = tk.E, bg=GGRAY, font=TOP_D_LABEL_FONT, height= 2, padx = 10)
        total_label.pack(expand=True, fill="both")

        current_label = tk.Label(self.display_frame, text=self.current_expression, anchor = tk.E, bg= ORANGE, font=D_LABEL_FONT, height= 2, padx= 10)
        current_label.pack(expand= True, fill="both", ipady=20)

        return total_label, current_label
    

    #Create all buttons 

    def create_digit_buttons(self):
        for digit, grid_location in self.digits.items():
            button = tk.Button(self.button_frame, text=str(digit),font= BTN_FONT, width=5, height=2, command=lambda x=digit: self.add_to_calculation(x))
            button.grid(row=grid_location[0], column=grid_location[1], sticky=tk.NSEW, padx=3, pady=3 )

    def create_C_button(self):
        button = tk.Button(self.button_frame, text="CLEAR", font= BTN_FONT, width=5, height=2, command=self.clear)
        button.grid(row=1, column=1, columnspan=2, sticky=tk.NSEW, padx=3, pady=3 )
    
    def create_pie_button(self):
        button = tk.Button(self.button_frame, text="π", font= SPECIAL_BTN_FONT, width=5, height=2, command= self.pie)
        button.grid(row=2, column=1, sticky=tk.NSEW, padx=3, pady=3 )
    
    def create_power_button(self):
        button = tk.Button(self.button_frame, text="x²", font= SPECIAL_BTN_FONT, width=5, height=2, command= self.power)
        button.grid(row=3, column=1, sticky=tk.NSEW, padx=3, pady=3 )
    
    def create_sqrt_button(self):
        button = tk.Button(self.button_frame, text="√ ", font= SPECIAL_BTN_FONT, width=5, height=2, command= self.root)
        button.grid(row=4, column=1, sticky=tk.NSEW, padx=3, pady=3 )

    def create_oprths_button(self):
        button = tk.Button(self.button_frame, text="(", font= BTN_FONT, width=5, height=2, command=self.open_bracket)
        button.grid(row=1, column=3, sticky=tk.NSEW, padx=3, pady=3 )

    def create_cprths_button(self):
        button = tk.Button(self.button_frame, text=")",font= BTN_FONT,  width=5, height=2, command=self.close_bracket)
        button.grid(row=1, column=4, sticky=tk.NSEW, padx=3, pady=3 )

    def create_enter_button(self):
        button = tk.Button(self.button_frame, text="Enter", font= BTN_FONT, width=5, height=2, command=self.evaluate)
        button.grid(row=5, column=4, columnspan=2 ,sticky=tk.NSEW, padx=3, pady=3 )
    
    def create_operation_button(self):
        i = 1
        for operator, symbol in self.operations.items():
            button = tk.Button(self.button_frame, text=symbol, font=OPERATOR_FONT, width=5, height =2, command=lambda x=operator: self.operated(x))
            button.grid(row=i, column=5, sticky=tk.NSEW, padx=3, pady=3 )
            i += 1

    def create_into_button(self):
        button = tk.Button(self.button_frame, text="Hi", font=BTN_FONT, width=5, height=2, command=self.intro)
        button.grid(row=5, column=1, sticky=tk.NSEW, padx=3, pady=3)


    #define functions FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


    def add_to_calculation(self, value):
        self.current_expression += str(value)
        self.update_current_label()

    def operated (self, operator):
        self.current_expression += operator
        self.update_current_label()
    
    def power(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_current_label()
    
    def root(self):
        self.current_expression = str(eval(f"{self.current_expression} **0.5"))
        self.update_current_label()

    def pie(self):
        self.current_expression = str(eval(f"{self.current_expression}*{math.pi}"))
        self.update_current_label()
    
    def open_bracket(self):
        self.current_expression += "("
        self.update_current_label()
    
    def close_bracket(self):
        self.current_expression += ")"
        self.update_current_label()

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_current_label()
        self.update_total_label()

    #updates
    def update_total_label(self):
        self.total_label.config(text=self.total_expression)

    def update_current_label(self):
        self.current_label.config(text=self.current_expression[:20])

    #define evaluation
    def evaluate(self):
        self.total_expression += self.current_expression + " = "
        self.update_total_label()
        try:
            self.current_expression=str(eval(self.current_expression))
        except Exception as err:
            self.current_expression = "Error"
            msgbox.showwarning("Warning", message="Can't calculate")
        finally:
            self.update_current_label()

    #intro

    def intro(self):
        msgbox.showinfo("INFO", "DK_Calculator is the first GUI project from DK. Thank you for your support. 12/30/22")

    #menu
    def show_version(self):
        msgbox.showinfo("info", "DK_Calculator_version 0.001")

    def askyesorno(self):
        response = msgbox.askyesno(title="warning" ,message="Do you really want to quit the program?")
        if response == 1:
            self.window.quit()
        else:
            return 
    def create_first_menu(self):
        menu_file = tk.Menu(self.menu, tearoff=0)
        menu_file.add_command(label="version", command=self.show_version)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.askyesorno)
        self.menu.add_cascade(label="info", menu=menu_file)

    #key binding
    def binding_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event,digit=key: self.add_to_calculation(digit))

        self.window.bind("/", lambda event, operator="/": self.operated(operator))
        self.window.bind("*", lambda event, operator="*": self.operated(operator))
        self.window.bind("+", lambda event, operator="+": self.operated(operator))
        self.window.bind("-", lambda event, operator="-": self.operated(operator))
        self.window.bind("C".lower(), lambda event: self.clear())

    #looping
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    DKC = Calculator()
    DKC.run()


