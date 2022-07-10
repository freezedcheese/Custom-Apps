import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

#init
IN_TO_PIXELS = 100
IN_TO_THUMBNAIL = 40

GRID_PAD = 8
BUTTON_PAD = 5

DISPLAY_COLOR = "#ffffff"
DISPLAY_BUTTON_OUTER_PAD = 20

CANVAS_LINKS = 4
CANVAS_PAD_LINKS = 1.5
CANVAS_IPAD_LINKS = 1
CANVAS_WIDTH = (CANVAS_LINKS + CANVAS_PAD_LINKS - CANVAS_IPAD_LINKS) * 0.5 * IN_TO_PIXELS
CANVAS_HEIGHT = 250
CANVAS_MARKING_COLOR = "#000000"

TREE_WIDTH = 330

SPACE_TEXT_COLORS = ["#000000", "#cc2114", "#137a0d"]

menuChildrenProp = [{"name": "menuStructure", "style": "menuStructure.TFrame", "buttonStyle": "structureButton.TLabel", "weight": 1, "color": "#F0F0F0"},
                    {"name": "menuRigid", "style": "menuRigid.TFrame", "buttonStyle": "rigidButton.TLabel", "weight": 1, "color": "#DEDEDE"},
                    {"name": "menuHSShaft", "style": "menuHSShaft.TFrame", "buttonStyle": "hsShaftButton.TLabel", "weight": 2, "color": "#F0F0F0"},
                    {"name": "menuShaft", "style": "menuShaft.TFrame", "buttonStyle": "shaftButton.TLabel", "weight": 3, "color": "#DEDEDE"},
                    {"name": "menuCustom", "style": "menuCustom.TFrame", "buttonStyle": "customButton.TLabel", "weight": 1, "color": "#F0F0F0"}]

hardware = {"bar_link": #guide
                {"label": "Bar Link", "src": Image.open("images/bar_link.png"), "size": (0.5, 0.5)},
            "angle": #structure
                {"label": "Angle", "src": Image.open("images/angle.png"), "size": (1, 1)},
            "c_channel": 
                {"label": "C Channel", "src": Image.open("images/c_channel.png"), "size": (1, 0.5)},
            "u_channel": 
                {"label": "U Channel", "src": Image.open("images/u_channel.png"), "size": (1, 1)}, 
            "bearing_block": #rigid
                {"label": "Bearing Block", "src": Image.open("images/bearing_block.png"), "size": (1.4, 0.5)},
            "plate": 
                {"label": "Plate", "src": Image.open("images/plate.png"), "size": (0.062, 1.5)},
            "standoff": 
                {"label": "Standoff", "src": Image.open("images/standoff.png"), "size": (1, 0.25)},
            "nut_keps": 
                {"label": "Keps Nut", "src": Image.open("images/nut_keps.png"), "size": (0.141, 0.34)},
            "nut_nylock": 
                {"label": "Nylock Nut", "src": Image.open("images/nut_nylock.png"), "size": (0.19235124, 0.32)},
            "bearing": #shaft
                {"label": "Bearing", "src": Image.open("images/bearing.png"), "size": (0.25, 1.4)},
            "gear": 
                {"label": "Gear", "src": Image.open("images/gear.png"), "size": (0.375, 1.58)},
            "gear_hs_inserts": 
                {"label": "HS Gear with Inserts", "src": Image.open("images/gear_hs_inserts.png"), "size": (0.48425197, 1.58)},
            "shaft_collar": 
                {"label": "Shaft Collar", "src": Image.open("images/shaft_collar.png"), "size": (0.26, 0.43)},
            "shaft_collar_clamping": 
                {"label": "Clamping Shaft Collar", "src": Image.open("images/shaft_collar_clamping.png"), "size": (0.5, 0.62)},
            "spacer": 
                {"label": "Nylon Spacer", "src": Image.open("images/spacer.png"), "size": (0.5, 0.5)},
            "spacer_4.6mm": 
                {"label": "Small Black Spacer", "src": Image.open("images/spacer_4.6mm.png"), "size": (0.187, 0.32)},
            "spacer_8mm": 
                {"label": "Large Black Spacer", "src": Image.open("images/spacer_8mm.png"), "size": (0.328, 0.32)},
            "sprocket": 
                {"label": "Sprocket", "src": Image.open("images/sprocket.png"), "size": (0.625, 1.69)},
            "sprocket_hs_inserts": 
                {"label": "HS Sprocket with Inserts", "src": Image.open("images/sprocket_hs_inserts.png"), "size": (0.625, 1.69)},
            "washer": 
                {"label": "Washer", "src": Image.open("images/washer.png"), "size": (0.032, 0.38)},
            "bearing_hs": #hs shaft
                {"label": "HS Bearing", "src": Image.open("images/bearing_hs.png"), "size": (0.375, 1.4)},
            "gear_hs": 
                {"label": "HS Gear", "src": Image.open("images/gear_hs.png"), "size": (0.38425197, 1.58)},
            "shaft_collar_clamping_hs": 
                {"label": "HS Clamping Shaft Collar", "src": Image.open("images/shaft_collar_clamping_hs.png"), "size": (0.5, 0.79)},
            "spacer_hs": 
                {"label": "HS Spacer", "src": Image.open("images/spacer_hs.png"), "size": (0.5, 0.39)},
            "sprocket_hs": 
                {"label": "HS Sprocket", "src": Image.open("images/sprocket_hs.png"), "size": (0.525, 1.69)},
            "spacer_custom": #custom
                {"label": "Custom Spacer", "src": Image.open("images/spacer_custom.png"), "size": (0.5, 0.5)}}

optioned = {"standoff", "spacer", "spacer_hs", "spacer_custom"}

lengthDict = {"1/16\"": 0.0625, "1/8\"": 0.125, "1/4\"": 0.25, "3/8\"": 0.375, "1/2\"": 0.5, "3/4\"": 0.75, "1\"": 1, "1-1/2\"": 1.5, "2\"": 2, "2-1/2\"": 2.5, "3\"": 3, "4\"": 4, "5\"": 5, "6\"": 6}

#classes
class PushButton(ttk.Button):
    def __init__(self, master, call, **kw):
        super().__init__(master=master,**kw)
        self.defaultStyle = self["style"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", lambda e: self.on_click(e, call))
        self.bind("<Shift-Button-1>", lambda e: self.on_shiftclick(e, call))
        self.bind("<ButtonRelease-1>", self.on_enter)
        
    def on_enter(self, e):
        ttk.Button.configure(self, style="hoverButton.TLabel")
    
    def on_leave(self, e):
        ttk.Button.configure(self, style=self.defaultStyle)
    
    def on_click(self, e, call):
        ttk.Button.configure(self, style="clickButton.TLabel")
        call(False)
    
    def on_shiftclick(self, e, call):
        ttk.Button.configure(self, style="clickButton.TLabel")
        call(True)

class ToggleButton(ttk.Button):
    toggleInstances = []
    
    def __init__(self, master, **kw):
        super().__init__(master=master,**kw)
        self.toggled = False
        self.clickFlag = True
        self.defaultStyle = self["style"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_unclick)
        ToggleButton.toggleInstances.append(self)
    
    def on_enter(self, e):
        ttk.Button.configure(self, style="hoverButton.TLabel")
    
    def on_leave(self, e):
        if self.toggled:
            ttk.Button.configure(self, style="clickButton.TLabel")
        else:
            ttk.Button.configure(self, style=self.defaultStyle)
    
    def on_click(self, e):
        if not self.clickFlag:
            self.clickFlag = True
            self.toggled = not self.toggled
            if self.toggled:
                ttk.Button.configure(self, style="clickButton.TLabel")
                for instance in ToggleButton.toggleInstances:
                    if instance != self:
                        instance.toggled = False
                        instance.event_generate("<Leave>")
            else:
                ttk.Button.configure(self, style=self.defaultStyle)
    
    def on_unclick(self, e):
        self.clickFlag = False

class RigidObject():
    rigidInstances = []
    adjustments =  {"angle": [0.75, -0.296, -0.296, 0.75],
                    "c_channel": [-0.25, -0.3, -0.25, 0.238], 
                    "u_channel": [-0.32874016, -0.31299213, -0.32874016, 0.75],
                    "bearing_block": [-0.125]}

    def __init__(self, iid, rotation, toggle, canvas):
        self.iid = iid
        self.rotation = rotation
        self.toggle = toggle
        self.canvas = canvas
        self.adjustment = RigidObject.adjustments[self.iid][0]
        RigidObject.rigidInstances.append(self)
    
    @classmethod
    def changeObject(cls, iid):
        for instance in RigidObject.rigidInstances:
            if instance.toggle.toggled:
                instance.iid = iid
                instance.updateRigidObject()

    def incRotation(self, inc):       
        self.rotation = (self.rotation + inc) % 4
        self.updateRigidObject()

    def updateRigidObject(self):
        if self.iid == "bearing_block":
            self.rotation = 1
            self.adjustment = RigidObject.adjustments["bearing_block"][0]
        else:
            self.adjustment = RigidObject.adjustments[self.iid][self.rotation]
        
        updateDisplay(self.canvas)
        updateSpace()


#functions
def updateSpins():
    unitSpin.selection_clear()
    standoffSpin.selection_clear()
    spacerHSSpin.selection_clear()
    spacerSpin.selection_clear()

def updateSpace():
    try:
        space = float(spaceEntry.get())
    except:
        return
    
    if unitSpin.get() == "holes":
        space = space / 2 - 0.5

    space += (lRigidObject.adjustment + rRigidObject.adjustment)

    for i in hardware:
        if i not in optioned:
            space -= hardware[i]["size"][0] * hardware[i]["asymCount"]
            space -= hardware[i]["size"][0] * hardware[i]["symCount"] * 2
        else:
            for option in hardware[i]["asymCount"]:
                if option in lengthDict:
                    space -= lengthDict[option] * hardware[i]["asymCount"][option]
                else:
                    space -= float(option) * hardware[i]["asymCount"][option]

            for option in hardware[i]["symCount"]:
                if option in lengthDict:
                    space -= lengthDict[option] * hardware[i]["symCount"][option] * 2
                else:
                    space -= float(option) * hardware[i]["symCount"][option] * 2
    
    if space > 0.032:
        spaceOutput.configure(text=f"{space:.8}", foreground=SPACE_TEXT_COLORS[0])
    elif space < 0:
        spaceOutput.configure(text=f"{space:.8}", foreground=SPACE_TEXT_COLORS[1])
    else:
        spaceOutput.configure(text=f"{space:.8}", foreground=SPACE_TEXT_COLORS[2])

    symSpace = space / 2

    if symSpace > 0.032:
        spaceSymOutput.configure(text=f"({symSpace:.8} symmetrical)", foreground=SPACE_TEXT_COLORS[0])
    elif symSpace / 2 < 0:
        spaceSymOutput.configure(text=f"({symSpace:.8} symmetrical)", foreground=SPACE_TEXT_COLORS[1])
    else:
        spaceSymOutput.configure(text=f"({symSpace:.8} symmetrical)", foreground=SPACE_TEXT_COLORS[2])

def addCount(iid, deduct, option=None):
    if iid == "spacer_custom":
        try:
            float(option)
        except:
            return

    if asymToggle.toggled:
        if not option:
            if not deduct:
                hardware[iid]["asymCount"] += 1
            elif hardware[iid]["asymCount"] > 0:
                hardware[iid]["asymCount"] -= 1
            updateTree(asymTree, iid, hardware[iid]["asymCount"])      
        else:
            if option not in hardware[iid]["asymCount"]:
                hardware[iid]["asymCount"][option] = 0
            if not deduct:
                hardware[iid]["asymCount"][option] += 1
            elif hardware[iid]["asymCount"][option] > 0:
                hardware[iid]["asymCount"][option] -= 1
            updateTree(asymTree, iid, hardware[iid]["asymCount"][option], option)        
    elif symToggle.toggled:
        if not option:
            if not deduct:
                hardware[iid]["symCount"] += 1
            elif hardware[iid]["symCount"] > 0:
                hardware[iid]["symCount"] -= 1
            updateTree(symTree, iid, hardware[iid]["symCount"])
        else:
            if option not in hardware[iid]["symCount"]:
                hardware[iid]["symCount"][option] = 0
            if not deduct:
                hardware[iid]["symCount"][option] += 1
            elif hardware[iid]["symCount"][option] > 0:
                hardware[iid]["symCount"][option] -= 1
            updateTree(symTree, iid, hardware[iid]["symCount"][option], option)

def updateTree(tree, iid, count, option=None):
    if tree == symTree:
        count *= 2
    
    if not option:
        if tree.exists(iid):
            if count == 0:
                tree.delete(iid)
            else:
                tree.item(iid, value=(hardware[iid]["label"], count))
        elif count != 0:
            tree.insert('', 'end', iid=iid, image=hardware[iid]["thumbnail"], value=(hardware[iid]["label"], count))
    else:
        parentID = iid
        iid = iid + "_" + option

        if not tree.exists(parentID):
            tree.insert('', 'end', iid=parentID, image=hardware[parentID]["thumbnail"], value=(hardware[parentID]["label"] + 's', ''))

        if tree.exists(iid):
            if count == 0:
                tree.delete(iid)
            else:
                tree.item(iid, value=(option, count))
        elif count != 0:
            tree.insert(parentID, 'end', iid=iid, value=(option, count))
        
        if not tree.get_children(parentID):
            tree.delete(parentID)

    updateSpace()

def delTree(*e):
    for iid in asymTree.selection():
        if asymTree.exists(iid):
            parentID = asymTree.parent(iid)

            if parentID == '':
                if asymTree.get_children(iid):
                    for option in hardware[iid]["asymCount"]:
                        hardware[iid]["asymCount"][option] = 0
                    asymTree.delete(iid)
                else:   
                    hardware[iid]["asymCount"] = 0
                    asymTree.delete(iid)
            else:
                hardware[parentID]["asymCount"][iid.split("_")[-1]] = 0
                asymTree.delete(iid)

                if not asymTree.get_children(parentID):
                    asymTree.delete(parentID)
    
    for iid in symTree.selection():
        if symTree.exists(iid):
            parentID = symTree.parent(iid)

            if parentID == '':
                if symTree.get_children(iid):
                    for option in hardware[iid]["symCount"]:
                        hardware[iid]["symCount"][option] = 0
                    symTree.delete(iid)
                else:   
                    hardware[iid]["symCount"] = 0
                    symTree.delete(iid)
            else:
                hardware[parentID]["symCount"][iid.split("_")[-1]] = 0
                symTree.delete(iid)

                if not symTree.get_children(parentID):
                    symTree.delete(parentID)
    
    updateSpace()

def updateDisplay(canvas):
    if canvas == lCanvas:
        drawImage = ImageTk.PhotoImage(hardware[lRigidObject.iid]["src"].resize((int(hardware[lRigidObject.iid]["size"][0] * IN_TO_PIXELS), int(hardware[lRigidObject.iid]["size"][1] * IN_TO_PIXELS))).rotate(lRigidObject.rotation * 90, expand=True))
        canvas.create_image((CANVAS_WIDTH - CANVAS_PAD_LINKS * 0.5 * IN_TO_PIXELS - hardware[lRigidObject.iid]["size"][int(lRigidObject.rotation%2)] * IN_TO_PIXELS, 0.75 * IN_TO_PIXELS), anchor="nw", image=drawImage)
        canvas.image=drawImage
    elif canvas == rCanvas:
        drawImage = ImageTk.PhotoImage(hardware[rRigidObject.iid]["src"].resize((int(hardware[rRigidObject.iid]["size"][0] * IN_TO_PIXELS), int(hardware[rRigidObject.iid]["size"][1] * IN_TO_PIXELS))).rotate(((rRigidObject.rotation + 2) % 4) * 90, expand=True))
        canvas.create_image((CANVAS_PAD_LINKS * 0.5 * IN_TO_PIXELS, 0.75 * IN_TO_PIXELS), anchor="nw", image=drawImage)
        canvas.image=drawImage

def updateAll(*e):
    updateSpins()
    updateSpace()

#app
root = tk.Tk()
root.title("VEX Spacing Calculator v1.0.1")
root.iconbitmap("favicon.ico")
root.state('zoomed')

root.bind("<FocusIn>", updateAll)
root.bind("<Button-1>", updateAll)
root.bind("<Key>", updateAll)
root.bind("<Delete>", delTree)

#visuals
ttk.Style().configure("display.TFrame", background=DISPLAY_COLOR)
ttk.Style().configure("outlist.Treeview", rowheight=75)

ttk.Style().configure("text.TLabel", background=DISPLAY_COLOR, font=("Calibri", 10), justify="center")
ttk.Style().configure("TSpinbox", font=("Calibri", 10), justify="center")

for child in menuChildrenProp:
    ttk.Style().configure(child["style"], background=child["color"])
    ttk.Style().configure(child["buttonStyle"], background=child["color"], padding=BUTTON_PAD, relief="raised")

ttk.Style().configure("hoverButton.TLabel", background="#dddddd", font=("Calibri", 10), anchor="center", padding=BUTTON_PAD, relief="sunken")
ttk.Style().configure("clickButton.TLabel", background="#bbbbbb", font=("Calibri", 10), anchor="center", padding=BUTTON_PAD, relief="sunken")

ttk.Style().configure("displayButton.TLabel", background=DISPLAY_COLOR, padding=BUTTON_PAD, relief="raised")

ttk.Style().configure("symButton.TLabel", background="#eeeeee", font=("Calibri", 10), anchor="center", padding=BUTTON_PAD, relief="raised")

toggleLImg = ImageTk.PhotoImage(Image.open("images/toggle_l.png").resize((int(0.5 * IN_TO_PIXELS), int(0.5 * IN_TO_PIXELS))))
toggleRImg = ImageTk.PhotoImage(Image.open("images/toggle_r.png").resize((int(0.5 * IN_TO_PIXELS), int(0.5 * IN_TO_PIXELS))))

rotateLImg = ImageTk.PhotoImage(Image.open("images/rotate_l.png").resize((int(0.5 * IN_TO_PIXELS), int(0.5 * IN_TO_PIXELS))))
rotateRImg = ImageTk.PhotoImage(Image.open("images/rotate_r.png").resize((int(0.5 * IN_TO_PIXELS), int(0.5 * IN_TO_PIXELS))))

for i in hardware:
    hardware[i]["image"] = ImageTk.PhotoImage(hardware[i]["src"].resize((int(hardware[i]["size"][0] * IN_TO_PIXELS), int(hardware[i]["size"][1] * IN_TO_PIXELS))))
    hardware[i]["thumbnail"] = ImageTk.PhotoImage(hardware[i]["src"].resize((int(hardware[i]["size"][0] * IN_TO_THUMBNAIL), int(hardware[i]["size"][1] * IN_TO_THUMBNAIL))))

#hardware setup
for i in hardware:
    hardware[i]["asymCount"] = 0
    hardware[i]["symCount"] = 0

for i in optioned:
    hardware[i]["asymCount"] = {}
    hardware[i]["symCount"] = {}

#root children
display = ttk.Frame(root, style="display.TFrame")
display.grid(column=0, row=0, sticky="nsew")

output = ttk.Frame(root)
output.grid(column=1, row=0, sticky="nsew")

menu = ttk.Frame(root, style="menu.TFrame")
menu.grid(column=0, row=1, sticky="nsew", columnspan=2)

root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=0)
root.rowconfigure(0, weight=3)
root.rowconfigure(1, weight=0)


#display children
spaceEntryFrame = ttk.Frame(display, style="display.TFrame")
spaceEntryFrame.grid(column=1, row=3, sticky="n", pady=(0.25 * IN_TO_PIXELS - 10) * 2)

spaceOutputFrame = ttk.Frame(display, style="display.TFrame")
spaceOutputFrame.grid(column=1, row=3, sticky="s")

lDisplayFrame = ttk.Frame(display, style="display.TFrame")
lDisplayFrame.grid(column=0, row=3)

rDisplayFrame = ttk.Frame(display, style="display.TFrame")
rDisplayFrame.grid(column=2, row=3)

for i in range(3):
    display.columnconfigure(i, weight=1)
for i in range(6):
    display.rowconfigure(i, weight=1)

#spaceEntry children
spaceEntry = ttk.Entry(spaceEntryFrame, width=12, font=("Calibri", 20), justify="center")
spaceEntry.insert('end', "2")
spaceEntry.pack()

unitSpin = ttk.Spinbox(spaceEntryFrame, state="readonly", wrap=True, values=("holes", "inches (center to center)"), justify="center", width=30)
unitSpin.set("holes")
unitSpin.pack(padx=GRID_PAD, pady=GRID_PAD)

#spaceLOutput children
spaceOutput = ttk.Label(spaceOutputFrame, style="text.TLabel", font=("Calibri", 20), justify="center")
spaceOutput.pack()

spaceSymOutput = ttk.Label(spaceOutputFrame, style="text.TLabel", justify="center")
spaceSymOutput.pack()

ttk.Label(spaceOutputFrame, text="inches remaining", style="text.TLabel").pack()

#lDisplay children
lCanvas = tk.Canvas(lDisplayFrame, background=DISPLAY_COLOR, highlightthickness=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
lCanvas.pack()

lToggle = ToggleButton(lDisplayFrame, image=toggleLImg, style="displayButton.TLabel")
lToggle.pack(side="left")

lRigidObject = RigidObject("c_channel", 0, lToggle, lCanvas)

lRotate = PushButton(lDisplayFrame, call=lambda mode: lRigidObject.incRotation(1), image=rotateLImg, style="displayButton.TLabel")
lRotate.pack(side="left", padx=DISPLAY_BUTTON_OUTER_PAD)

#rDisplay children
rCanvas = tk.Canvas(rDisplayFrame, background=DISPLAY_COLOR, highlightthickness=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
rCanvas.pack()

rToggle = ToggleButton(rDisplayFrame, image=toggleRImg, style="displayButton.TLabel")
rToggle.pack(side="right")

rRigidObject = RigidObject("c_channel", 2, rToggle, rCanvas)

rRotate = PushButton(rDisplayFrame, call=lambda mode: rRigidObject.incRotation(-1), image=rotateRImg, style="displayButton.TLabel")
rRotate.pack(side="right", padx=DISPLAY_BUTTON_OUTER_PAD)

#populate canvases
for i in range(CANVAS_LINKS):
    lCanvas.create_image((0.5 * IN_TO_PIXELS * i, 0), anchor="nw", image=hardware["bar_link"]["image"])
    rCanvas.create_image((CANVAS_WIDTH - 0.5 * IN_TO_PIXELS * i, 0), anchor="ne", image=hardware["bar_link"]["image"])

lMark = {"x": (CANVAS_LINKS - CANVAS_IPAD_LINKS - 0.5) * 0.5 * IN_TO_PIXELS, "y": 0.25 * IN_TO_PIXELS, "r": 0.03125 * IN_TO_PIXELS}
rMark = {"x": (CANVAS_PAD_LINKS + 0.5) * 0.5 * IN_TO_PIXELS, "y": 0.25 * IN_TO_PIXELS, "r": 0.03125 * IN_TO_PIXELS}

lCanvas.create_oval(lMark["x"]-lMark["r"], lMark["y"]-lMark["r"], lMark["x"]+lMark["r"], lMark["y"]+lMark["r"], fill=CANVAS_MARKING_COLOR)
lCanvas.create_line(lMark["x"], lMark["y"], CANVAS_WIDTH, lMark["y"], fill=CANVAS_MARKING_COLOR)

rCanvas.create_oval(rMark["x"]-rMark["r"], rMark["y"]-rMark["r"], rMark["x"]+rMark["r"], rMark["y"]+rMark["r"], fill=CANVAS_MARKING_COLOR)
rCanvas.create_line(rMark["x"], rMark["y"], 0, rMark["y"], fill=CANVAS_MARKING_COLOR)

updateDisplay(lCanvas)
updateDisplay(rCanvas)

updateSpace()

#output children
asym = ttk.Frame(output)
asym.grid(column=0, row=0, sticky="nsew")

sym = ttk.Frame(output)
sym.grid(column=0, row=1, sticky="nsew")

output.columnconfigure(0, weight=1)
output.rowconfigure(0, weight=1)
output.rowconfigure(1, weight=1)

#asym children
asymToggle = ToggleButton(asym, text="Asymmetrical Spacers", style="symButton.TLabel")
asymToggle.pack(fill="x")

asymScroll = ttk.Scrollbar(asym)

asymTree = ttk.Treeview(asym, columns=("label", "count"), yscrollcommand=asymScroll.set, style="outlist.Treeview")
asymTree.pack(side="left")

asymTree.heading("label", text="Type")
asymTree.heading("count", text="Count")
asymTree.column("#0", width=int(TREE_WIDTH * 0.25), anchor="center")
asymTree.column("label", width=int(TREE_WIDTH * 0.6))
asymTree.column("count", width=int(TREE_WIDTH * 0.15), anchor="center")

asymScroll.configure(command=asymTree.yview)
asymScroll.pack(side="right", fill="y")

#sym children
symToggle = ToggleButton(sym, text="Symmetrical Spacers", style="symButton.TLabel")
symToggle.pack(fill="x")

symScroll = ttk.Scrollbar(sym)

symTree = ttk.Treeview(sym, columns=("label", "count"), yscrollcommand=symScroll.set, style="outlist.Treeview")
symTree.pack(side="left")

symTree.heading("label", text="Type")
symTree.heading("count", text="Count")
symTree.column("#0", width=int(TREE_WIDTH * 0.25), anchor="center")
symTree.column("label", width=int(TREE_WIDTH * 0.6))
symTree.column("count", width=int(TREE_WIDTH * 0.15), anchor="center")

symScroll.configure(command=symTree.yview)
symScroll.pack(side="right", fill="y")


#menu children
menuChildren = {}

for i in range(len(menuChildrenProp)):
    menuChildren[menuChildrenProp[i]["name"]] = ttk.Frame(menu, style=menuChildrenProp[i]["style"], padding=5)
    menuChildren[menuChildrenProp[i]["name"]].grid(column=i, row=0, sticky="nsew")
    menu.columnconfigure(i, weight=menuChildrenProp[i]["weight"])

menu.rowconfigure(0, weight=1)

#menuStructure children
PushButton(menuChildren["menuStructure"], call=lambda mode:RigidObject.changeObject("angle"), image=hardware["angle"]["image"], style="structureButton.TLabel").grid(column=0, row=0, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuStructure"], call=lambda mode:RigidObject.changeObject("c_channel"), image=hardware["c_channel"]["image"], style="structureButton.TLabel").grid(column=0, row=1, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuStructure"], call=lambda mode:RigidObject.changeObject("u_channel"), image=hardware["u_channel"]["image"], style="structureButton.TLabel").grid(column=1, row=0, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuStructure"], call=lambda mode:RigidObject.changeObject("bearing_block"), image=hardware["bearing_block"]["image"], style="structureButton.TLabel").grid(column=1, row=1, padx=GRID_PAD, pady=GRID_PAD)

for i in range(2):
    menuChildren["menuStructure"].columnconfigure(i, weight=1)
for i in range(3):
    menuChildren["menuStructure"].rowconfigure(i, weight=1)

#menuRigid children
standoffFrame = ttk.Frame(menuChildren["menuRigid"], style="menuRigid.TFrame")
standoffFrame.grid(column=1, row=1, columnspan=2)

PushButton(menuChildren["menuRigid"], call=lambda mode:addCount("plate", mode), image=hardware["plate"]["image"], style="rigidButton.TLabel").grid(column=0, row=0, rowspan=4, padx=GRID_PAD, pady=GRID_PAD)
PushButton(standoffFrame,             call=lambda mode:addCount("standoff", mode, standoffSpin.get()), image=hardware["standoff"]["image"], style="rigidButton.TLabel").pack(padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuRigid"], call=lambda mode:addCount("nut_keps", mode), image=hardware["nut_keps"]["image"], style="rigidButton.TLabel").grid(column=1, row=2, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuRigid"], call=lambda mode:addCount("nut_nylock", mode), image=hardware["nut_nylock"]["image"], style="rigidButton.TLabel").grid(column=2, row=2, padx=GRID_PAD, pady=GRID_PAD)
standoffSpin = ttk.Spinbox(standoffFrame, state="readonly", wrap=True, values=("1/4\"", "1/2\"", "3/4\"", "1\"", "1-1/2\"", "2\"", "2-1/2\"", "3\"", "4\"", "5\"", "6\""), justify="center", width=15)
standoffSpin.set("1\"")
standoffSpin.pack(padx=GRID_PAD, pady=GRID_PAD)

for i in range(3):
    menuChildren["menuRigid"].columnconfigure(i, weight=1)
for i in range(4):
    menuChildren["menuRigid"].rowconfigure(i, weight=1)

#menuHSShaft children
PushButton(menuChildren["menuHSShaft"], call=lambda mode:addCount("bearing_hs", mode), image=hardware["bearing_hs"]["image"], style="hsShaftButton.TLabel").grid(column=0, row=0, rowspan=3, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuHSShaft"], call=lambda mode:addCount("gear_hs", mode), image=hardware["gear_hs"]["image"], style="hsShaftButton.TLabel").grid(column=1, row=0, rowspan=3, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuHSShaft"], call=lambda mode:addCount("sprocket_hs", mode), image=hardware["sprocket_hs"]["image"], style="hsShaftButton.TLabel").grid(column=2, row=0, rowspan=3, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuHSShaft"], call=lambda mode:addCount("shaft_collar_clamping_hs", mode), image=hardware["shaft_collar_clamping_hs"]["image"], style="hsShaftButton.TLabel").grid(column=3, row=0, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuHSShaft"], call=lambda mode:addCount("spacer_hs", mode, spacerHSSpin.get()), image=hardware["spacer_hs"]["image"], style="hsShaftButton.TLabel").grid(column=3, row=1, padx=GRID_PAD, pady=GRID_PAD)
spacerHSSpin = ttk.Spinbox(menuChildren["menuHSShaft"], state="readonly", wrap=True, values=("1/16\"", "1/8\"", "1/4\"", "1/2\""), justify="center", width=8)
spacerHSSpin.set("1/2\"")
spacerHSSpin.grid(column=3, row=2, padx=GRID_PAD, pady=GRID_PAD)

for i in range(4):
    menuChildren["menuHSShaft"].columnconfigure(i, weight=1)
for i in range(3):
    menuChildren["menuHSShaft"].rowconfigure(i, weight=1)

#menuShaft children
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("bearing", mode), image=hardware["bearing"]["image"], style="shaftButton.TLabel").grid(column=0, row=0, rowspan=3, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("gear", mode), image=hardware["gear"]["image"], style="shaftButton.TLabel").grid(column=1, row=0, rowspan=3, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("gear_hs_inserts", mode), image=hardware["gear_hs_inserts"]["image"], style="shaftButton.TLabel").grid(column=2, row=0, rowspan=3, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("sprocket", mode), image=hardware["sprocket"]["image"], style="shaftButton.TLabel").grid(column=3, row=0, rowspan=3, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("sprocket_hs_inserts", mode), image=hardware["sprocket_hs_inserts"]["image"], style="shaftButton.TLabel").grid(column=4, row=0, rowspan=3, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("shaft_collar_clamping", mode), image=hardware["shaft_collar_clamping"]["image"], style="shaftButton.TLabel").grid(column=5, row=0, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("spacer", mode, spacerSpin.get()), image=hardware["spacer"]["image"], style="shaftButton.TLabel").grid(column=5, row=1, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("shaft_collar", mode), image=hardware["shaft_collar"]["image"], style="shaftButton.TLabel").grid(column=6, row=0, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("spacer_8mm", mode), image=hardware["spacer_8mm"]["image"], style="shaftButton.TLabel").grid(column=6, row=1, rowspan=2, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("washer", mode), image=hardware["washer"]["image"], style="shaftButton.TLabel").grid(column=7, row=0, padx=GRID_PAD, pady=GRID_PAD)
PushButton(menuChildren["menuShaft"], call=lambda mode:addCount("spacer_4.6mm", mode), image=hardware["spacer_4.6mm"]["image"], style="shaftButton.TLabel").grid(column=7, row=1, rowspan=2, padx=GRID_PAD, pady=GRID_PAD)
spacerSpin = ttk.Spinbox(menuChildren["menuShaft"], state="readonly", wrap=True, values=("1/8\"", "1/4\"", "3/8\"", "1/2\""), justify="center", width=8)
spacerSpin.set("1/2\"")
spacerSpin.grid(column=5, row=2, padx=GRID_PAD, pady=GRID_PAD)

for i in range(8):
    menuChildren["menuShaft"].columnconfigure(i, weight=1)
for i in range(3):
    menuChildren["menuShaft"].rowconfigure(i, weight=1)

#menuCustom children
customFrame = ttk.Frame(menuChildren["menuCustom"], style="menuCustom.TFrame")
customFrame.grid(column=0, row=0)

PushButton(customFrame, call=lambda mode:addCount("spacer_custom", mode, customEntry.get()), image=hardware["spacer_custom"]["image"], style="customButton.TLabel").pack(padx=GRID_PAD, pady=GRID_PAD)
customEntry = ttk.Entry(customFrame, width=10, justify="center")
customEntry.pack(padx=GRID_PAD, pady=GRID_PAD)

menuChildren["menuCustom"].columnconfigure(0, weight=1)
menuChildren["menuCustom"].rowconfigure(0, weight=1)

#main loop
root.mainloop()
