from tkinter import *

class Map(Canvas):

    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.config(**kwargs)
        self.pack(side=LEFT)

       # self.textbox = None

        self.size = 22
        self.objects = self.make_map()

        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.motion)
        self.bind("<ButtonRelease>", self.release)

        # State holders to decide when to fill pixel or not
        self.button_pressed = False
        self.button_released = True
        self.paint = True


    def motion(self, event):
        # Exception handling to remove errors from 
        # when the mouse is outside of the scope
        try:
            pxl = self.get_pixel(event)
            self.fill_pxl(pxl)
        except:
            pass

    def release(self, event):
        try:
            pxl = self.get_pixel(event)
            self.button_pressed = False
            self.button_released = True
        except:
            pass        

    def click(self, event):
        # Sets the button pressed as true or false, depending on
        # the state the pixel is in.
        try:
            pxl = self.get_pixel(event)
            self.button_pressed = True
            self.button_released = False

            if self.objects[pxl]:
                self.paint = False
            else:
                self.paint = True

            self.fill_pxl(pxl)
        except:
            pass


    def fill_pxl(self, pxl):
        # Checks if pixel should be black or white. The current state of
        # the pixel is found as a value in self.objects, where the pixel
        # is the key. Fill = 1, Unfill = 0
        if self.paint:
            self.itemconfig(pxl, fill="black")
            self.objects[pxl] = 1
        else:
            self.itemconfig(pxl, fill="white")
            self.objects[pxl] = 0


    def get_pixel(self, event):
        # Gets the pixel that the cursor is overlappning, given the
        # coordinates from the event callback.
        x = event.x
        y = event.y
        pxl = self.find_overlapping(x, y, x, y)[0]
        return pxl
            

    def make_map(self):
        y = 110
        objects = {}

        for col in range(16):
            x = 15
            row = self.create_text(x,(y+(self.size/2)), text=col+1)
            row_x = 25
            for row in range(16):
                self.create_text((row_x + (self.size/2)),470, text=row+1)
                pxl_ID = self.create_rectangle(row_x, y, row_x+self.size, y+self.size,
                                             outline="black", fill="white")
                objects[pxl_ID] = 0
                row_x += self.size
            y += self.size

        return objects

    def clear(self):
        for pxl in self.objects.keys():
            self.itemconfig(pxl, fill="white")
            self.objects[pxl] = 0

        self.textbox.clear()
        
    def callback(self):
        code = CodeCreator(self.objects)

class StyledButton(Button):

    def __init__(self, master, callback_object, **kwargs):
        super().__init__(master)
        self.config(text="Convert", bg="gray", fg="black", font="Courier 15",
                    relief=RIDGE, command=callback_object.callback, bd=2)
        self.config(**kwargs)
        self.pack(pady=10)
        self.bind("<Enter>", lambda x: self.hover(True))
        self.bind("<Leave>", lambda x: self.hover(False))

    def hover(self, action):
        if action:
            self.config(bg="white")
        else:
            self.config(bg="gray")


class CodeBox(Text):

    def __init__(self, master, map):
        super().__init__(master)
        # Saves a reference of the map object, to
        # achive get be able to convert the mapping system to 
        # binaries and then to final code
        self.map = map
        self.config(font="Courier 10", width=50, height=20, relief=RIDGE, bd=2)
        self.pack(side=TOP)

    
    def callback(self):
        self.output_code = CodeCreator(self.map.objects)
        self.insert_code()


    def insert_code(self):
        self.delete("1.0", END)

        for row in self.output_code:
            self.insert(END, row)
            self.insert(END, "\n")


    def clear(self):
        self.output_code.clear()
        self.insert_code()


class CodeCreator:

    def __init__(self, pixel_map):
        
        self.binaries = self.convert_map_to_binarie(pixel_map)
        self.write_code()

    def write_code(self):
        self.output_code = []
        first_line = "function void draw(int location) {"
        second_line = "\tlet memAddr = 16384 + location;"
        self.output_code.extend((first_line, second_line))

        for index, data in enumerate(self.binaries):
            code = "\tdo Memory.poke(memAddr + {}, {});".format(index*32, data)
            self.output_code.append(code)

        self.output_code.extend(("\treturn;", "}"))

    def clear(self):
        self.binaries = [0 for i in range(16)]
        self.write_code()


    def convert_map_to_binarie(self, pixel_map):
        all_registers = [reg for reg in pixel_map.items()]

        rows = []
        step = 0

        for i in range(16):
            slice_end = step + 16
            rows.append(all_registers[step:slice_end])
            step += 16

        binaries = []

        for row in rows:
            binarie = ""
            for pxl in row:
                binarie += str(pxl[1])
            binaries.append(binarie)

        converted_instruction = [int(bin, 2) for bin in binaries]

        return converted_instruction

    def __iter__(self):
        return self

    def __next__(self):
        if self.output_code:
            code = self.output_code[0]
            self.output_code.pop(0)
            return code
        else:
            raise StopIteration

    def __repr__(self):
        return self.binaries

class MiddleFrame(Frame):

    def __init__(self, master, map, textbox, **kwargs):
        super().__init__(master)
        self.config(width=200, height=600)
        self.config(**kwargs)
        self.pack(side=LEFT)

        map.textbox = textbox

        self.subroutine_label = Label(self, font="Courier 12", 
                                    text="Subroutine")
        self.subroutine_label.pack()

        self.subroutines = ["function", "method"]
        self.var = StringVar(self)
        self.var.set(self.subroutines[0])
        self.subroutine = OptionMenu(self, self.var, *self.subroutines)
        self.subroutine.pack(pady=10)


        self.name_label = Label(self, font="Courier 12", text="Name")
        self.name_label.pack()
        self.name = Entry(self, font="Courier 10", width=20)
        self.name.pack()
        self.name_label2 = Label(self, font="Courier 12", text=">>")
        self.name_label2.pack(pady=5)


        # This button is in the middle frame but needs the textbox to
        # created first, to be able to reference it.
        self.convert_button = StyledButton(self, textbox)



        self.clear_button = StyledButton(self, map, text="Clear",
                                        command=map.clear)
        self.clear_button.pack()


        



if __name__ == "__main__":

    root = Tk()
    root.geometry("1000x600")

    map = Map(root, height=600, width=400)

    # Right frame and its content

    right_frame = Frame(root, width=450, height=600)
    right_frame.pack(side=RIGHT, padx=40)

    textbox = CodeBox(right_frame, map)

    copy_button = StyledButton(right_frame, textbox, text="COPY")
    copy_button.pack(side=BOTTOM)

    middle_frame = MiddleFrame(root, map, textbox)


    root.mainloop()