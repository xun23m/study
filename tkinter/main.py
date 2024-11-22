import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog, Scale, HORIZONTAL, Entry, Menu
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self, master):
        self.image = None
        self.processed_image = None
        self.selection = None
        self.master = master
        self.type_way = None
        self.master.title("图像处理实验")

        self.master.geometry("1280x800")

        # self.master.bind("<Configure>", self.on_resize)

        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # 添加文件菜单
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="打开图像", command=self.open_image)
        self.file_menu.add_command(label="退出", command=self.master.quit)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)

        # 添加图像处理菜单
        self.process_menu = Menu(self.menu_bar, tearoff=0)
        self.process_menu.add_command(label="边缘检测", command=lambda: self.edge_detection())
        self.process_menu.add_command(label="直线检测", command=lambda: self.line_detection())
        self.process_menu.add_command(label="圆检测", command=lambda: self.circle_detection())
        self.menu_bar.add_cascade(label="图像处理", menu=self.process_menu)


        # UI Elements
        self.label = Label(master, text="选择图像进行处理")
        self.label.place(x=10, y=10)

        self.canvas = Label(master)
        self.canvas.place(x=500, y=40)

        self.canvas_origon = Label(master)
        self.canvas_origon.place(x=10, y=40)

        # 边缘检测参数
        self.edge_low_scale = Scale(master, from_=1, to=300, orient=HORIZONTAL,  command=self.on_threshold_change,
                                    length=100, label="低阈值")
        self.edge_low_scale.set(150)
        self.edge_high_scale = Scale(master, from_=1, to=300, orient=HORIZONTAL, command=self.on_threshold_change,
                                    length=100,label= "高阈值")
        self.edge_high_scale.set(150)

        # 直线检测参数
        self.line_minLineLength_scale = Scale(master, from_=1, to=300, orient=HORIZONTAL,
                                              command=self.on_threshold_change,label= "最小线段长度")
        self.line_maxLineGap_scale = Scale(master, from_=1, to=300, orient=HORIZONTAL,
                                              command=self.on_threshold_change, label= "最大线段间隔")
        self.line_threshold_scale = Scale(master, from_=1, to=300, orient=HORIZONTAL,
                                              command=self.on_threshold_change, label= "阈值")
        self.rho_entry = Entry(master, width=5)
        self.rho_entry.insert(0, "1")
        #圆检测参数
        self.circle_minDist_scale = Scale(master, from_=1, to=300, orient=HORIZONTAL,
                                              command=self.on_threshold_change, label= "最小圆心距")
        self.circle_minDist_scale.set(5)
        self.circle_param2_scale = Scale(master, from_=1, to=300, orient=HORIZONTAL,
                                              command=self.on_threshold_change, label= "积累器阈值")
        self.circle_param2_scale.set(50)
        self.circle_minRadius_scale = Scale(master, from_=1, to=300, orient=HORIZONTAL,
                                              command=self.on_threshold_change, label= "最小半径")
        self.circle_maxRadius_scale = Scale(master, from_=1, to=300, orient=HORIZONTAL,
                                              command=self.on_threshold_change, label= "最大半径")
        self.circle_maxRadius_scale.set(300)

    def hide_all_widgets(self):
        # 隐藏所有控件
        self.edge_low_scale.place_forget()
        self.edge_high_scale.place_forget()
        self.line_minLineLength_scale.place_forget()
        self.line_maxLineGap_scale.place_forget()
        self.line_threshold_scale.place_forget()
        self.rho_entry.place_forget()
        self.circle_minDist_scale.place_forget()
        self.circle_param2_scale.place_forget()
        self.circle_minRadius_scale.place_forget()
        self.circle_maxRadius_scale.place_forget()

    def select_operation(self, operation):
        self.type_way = operation
    def on_threshold_change(self, value):
        if self.type_way == "edge_detection":
            self.edge_detection()
        elif self.type_way == "line_detection":
            self.line_detection()
        elif self.type_way == "circle_detection":
            self.circle_detection()
        else:
            print("未选择")
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)

            x, y = self.image.shape[:2]
            while x > 640 or y > 480:
                self.image = cv2.resize(self.image, (x//2, y//2))
                x, y = self.image.shape[:2]
            self.canvas.place(x=x+50, y=40)
            self.display_origon_image(self.image)

    def display_origon_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.canvas_origon.configure(image=img)
        self.canvas_origon.image = img

    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.canvas.configure(image=img)
        self.canvas.image = img
    def edge_detection(self):
        if self.image is None:
            return

        if self.selection != "edge_detection":
            self.hide_all_widgets()
            self.edge_low_scale.place(x=10, y=590)
            self.edge_high_scale.place(x=150, y=590)
            self.selection = "edge_detection"
        self.select_operation("edge_detection")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        low_threshold = self.edge_low_scale.get()
        high_threshold = self.edge_high_scale.get()

        edges = cv2.Canny(blurred, low_threshold, high_threshold)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self.display_image(edges_colored)

    def line_detection(self):
        if self.image is None:
            return
        if self.selection != "line_detection":
            self.hide_all_widgets()
            self.edge_low_scale.place(x=10, y=590)
            self.edge_high_scale.place(x=150, y=590)
            self.line_minLineLength_scale.place(x=250, y=590)
            self.line_maxLineGap_scale.place(x=350, y=590)
            self.line_threshold_scale.place(x=450, y=590)
            self.rho_entry.place(x=10, y=670)
            self.selection = "line_detection"
        self.select_operation("line_detection")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        low_threshold = self.edge_low_scale.get()
        high_threshold = self.edge_high_scale.get()
        rho = float(self.rho_entry.get())
        line_threshold = self.line_threshold_scale.get()
        minLineLength = self.line_minLineLength_scale.get()
        maxLineGap = self.line_maxLineGap_scale.get()
        edges = cv2.Canny(gray, low_threshold, high_threshold)
        lines = cv2.HoughLinesP(edges, rho, np.pi / 180, threshold=line_threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)
        line_img = self.image.copy()

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        self.display_image(line_img)

    def circle_detection(self):
        if self.image is None:
            return
        if self.selection != "circle_detection":
            self.hide_all_widgets()
            self.edge_high_scale.place(x=10, y=590)
            self.circle_minDist_scale.place(x=150, y=590)
            self.circle_param2_scale.place(x=250, y=590)
            self.circle_minRadius_scale.place(x=350, y=590)
            self.circle_maxRadius_scale.place(x=450, y=590)
            self.selection = "circle_detection"
        self.select_operation("circle_detection")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.medianBlur(gray, 5)
        low_threshold = self.edge_low_scale.get()
        high_threshold = self.edge_high_scale.get()
        minDist = self.circle_minDist_scale.get()
        param2 = self.circle_param2_scale.get()
        minRadius = self.circle_minRadius_scale.get()
        maxRadius = self.circle_maxRadius_scale.get()

        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=minDist,
            param1=high_threshold, param2=param2, minRadius=minRadius, maxRadius=maxRadius
        )

        circle_img = self.image.copy()

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(circle_img, (x, y), r, (0, 255, 0), 4)

        self.display_image(circle_img)

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()

