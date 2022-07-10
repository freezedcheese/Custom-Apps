import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import math
import time

#setup constants
PX_PER_IN = 3

DISPLAY_COLOR = "#ffffff"
CONTROLS_COLOR = "#f0f0f0"

PATH_COLOR = "#000000"

ENTRY_WIDTH = 7
BUTTON_WIDTH = 30

#setup global objects
drivetrain = None
path = None
controller = None

drivetrainProcess = None
controllerProcess = None

#define classes
#represents a 3 dimensional vector
class Vector3D():
    def __init__(self, x = 0, y = 0, angle = 0):
        self.x = x
        self.y = y
        self.angle = angle
    
    def getMagnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

#represents a physical drivetrain, but virtually
class VirtualDrivetrain():
    def __init__(self, trackRadius, motorVelCap, canvas, imgPath):
        self.trackRadius = trackRadius

        self.motorVelCap = motorVelCap

        self.v_a = 0
        self.v_b = 0
        self.v_c = 0
        self.v_d = 0

        self.pose = Vector3D()

        self.localVelocity = Vector3D()
        self.globalVelocity = Vector3D()

        self.imgPath = imgPath
        self.img = Image.open(self.imgPath).resize((18 * PX_PER_IN, 18 * PX_PER_IN))
        self.tkImg = ImageTk.PhotoImage(self.img)

        self.canvas = canvas
        self.canvas_item = self.canvas.create_image((0,0), image=self.tkImg)

        self.lastUpdateTimestamp = time.perf_counter()
    
    #wrapper to set individual motor velocities - respects motor saturation
    def setMotorVels(self, v_a, v_b, v_c, v_d):
        self.v_a = v_a if abs(v_a) < self.motorVelCap else self.motorVelCap * v_a / abs(v_a)
        self.v_b = v_b if abs(v_b) < self.motorVelCap else self.motorVelCap * v_b / abs(v_b)
        self.v_c = v_c if abs(v_c) < self.motorVelCap else self.motorVelCap * v_c / abs(v_c)
        self.v_d = v_d if abs(v_d) < self.motorVelCap else self.motorVelCap * v_d / abs(v_d)

        for i in range(4):
            if (v_a, v_b, v_c, v_d)[i] != (self.v_a, self.v_b, self.v_c, self.v_d)[i]:
                print("MOTOR VELOCITY SATURATED")

    #calculates local/global velocity based on individual motor velocities
    def power(self):
        v_ac = (self.v_a + self.v_c) / 2
        v_bd = (self.v_b + self.v_d) / 2

        r_ac = ((2 * self.trackRadius * self.v_a) / (self.v_a - self.v_c)) - self.trackRadius if self.v_a - self.v_c != 0 else None
        r_bd = ((2 * self.trackRadius * self.v_b) / (self.v_b - self.v_d)) - self.trackRadius if self.v_b - self.v_d != 0 else None

        if r_ac != None and r_bd != None:
            r_icc = math.sqrt(r_ac ** 2 + r_bd ** 2)
        elif r_ac != None:
            r_icc = r_ac
        elif r_bd != None:
            r_icc = r_bd
        else:
            r_icc = None

        v_lx, v_ly = rotate(v_bd, v_ac, math.pi / 4)

        theta_icc = None

        if r_icc == None:
            omega = 0
        elif r_icc == 0:
            omega = (self.v_a + self.v_b) / (2 * self.trackRadius)
        else:
            if r_ac == None:
                theta_icc = 0
            elif r_bd == 0 or r_bd == None:
                theta_icc = math.pi / 2
            else:
                theta_icc = math.atan(r_ac / r_bd)

                if (theta_icc > 0 and r_ac < 0) or (theta_icc < 0 and r_bd < 0):
                    theta_icc += math.pi

            omega = (v_ac * math.sin(theta_icc) + v_bd * math.cos(theta_icc)) / r_icc

        self.localVelocity = Vector3D(v_lx, v_ly, omega)

        self.globalVelocity.x, self.globalVelocity.y = rotate(self.localVelocity.x, self.localVelocity.y, self.pose.angle)
        self.globalVelocity.angle = self.localVelocity.angle

    #move drivetrain
    def move(self, displacement):
        self.pose.x += displacement.x
        self.pose.y += displacement.y
        self.pose.angle += displacement.angle

    #draw drivetrain to Canvas
    def draw(self):
        self.canvas.update()
        canvasX, canvasY = getCanvasCoords(self.canvas, self.pose.x, self.pose.y)

        self.canvas.coords(self.canvas_item, canvasX, canvasY)

        self.tkImg = ImageTk.PhotoImage(self.img.rotate(math.degrees(self.pose.angle), expand=True))
        self.canvas.itemconfig(self.canvas_item, image=self.tkImg)
    
    #updates to calculate movement based on time
    def update(self):
        currentTimestamp = time.perf_counter()
        deltaT = currentTimestamp - self.lastUpdateTimestamp
        self.lastUpdateTimestamp = currentTimestamp

        self.power()

        deltaX = self.globalVelocity.x * deltaT
        deltaY = self.globalVelocity.y * deltaT
        deltaTheta = self.globalVelocity.angle * deltaT

        self.move(Vector3D(deltaX, deltaY, deltaTheta))
        self.draw()

        root.after(10, self.update)

#issues path following commands to the drivetrain
class DrivetrainController():
    def __init__(self, drivetrain, path, lookahead, Kp, motorAccelCap):
        self.drivetrain = drivetrain

        self.path = path
        self.lastWaypointIndex = 0

        self.lookahead = lookahead

        self.motorVelCap = drivetrain.motorVelCap
        self.motorAccelCap = motorAccelCap

        self.Kp = Kp

        self.localVelocity = Vector3D()
        self.globalVelocity = Vector3D()

        self.lastMotorVelUpdateTimestamp = time.perf_counter()
    
    #generates individual motor velocities given a global velocity - respects motor velocity and acceleration limits
    def getMotorVels(self):
        self.localVelocity.x, self.localVelocity.y = rotate(self.globalVelocity.x, self.globalVelocity.y, -self.drivetrain.pose.angle)

        self.localVelocity.angle = self.globalVelocity.angle

        v_bd, v_ac = rotate(self.localVelocity.x, self.localVelocity.y, -math.pi / 4)

        rotPower = self.localVelocity.angle * self.drivetrain.trackRadius

        v_a, v_c = v_ac + rotPower, v_ac - rotPower
        v_b, v_d = v_bd + rotPower, v_bd - rotPower

        currentTimestamp = time.perf_counter()
        deltaT = currentTimestamp - self.lastMotorVelUpdateTimestamp
        self.lastMotorVelUpdateTimestamp = currentTimestamp

        motorDeltaVelCap = self.motorAccelCap * deltaT

        v_aDelta = v_a - self.drivetrain.v_a
        v_bDelta = v_b - self.drivetrain.v_b
        v_cDelta = v_c - self.drivetrain.v_c
        v_dDelta = v_d - self.drivetrain.v_d

        highestMotorDeltaVel = max(abs(v_aDelta), abs(v_bDelta), abs(v_cDelta), abs(v_dDelta))

        v_aDelta *= motorDeltaVelCap / highestMotorDeltaVel
        v_bDelta *= motorDeltaVelCap / highestMotorDeltaVel
        v_cDelta *= motorDeltaVelCap / highestMotorDeltaVel
        v_dDelta *= motorDeltaVelCap / highestMotorDeltaVel

        v_a = self.drivetrain.v_a + v_aDelta
        v_b = self.drivetrain.v_b + v_bDelta
        v_c = self.drivetrain.v_c + v_cDelta
        v_d = self.drivetrain.v_d + v_dDelta

        highestMotorVel = max(abs(v_a), abs(v_b), abs(v_c), abs(v_d))

        if highestMotorVel > self.motorVelCap:
            v_a *= self.motorVelCap / highestMotorVel
            v_b *= self.motorVelCap / highestMotorVel
            v_c *= self.motorVelCap / highestMotorVel
            v_d *= self.motorVelCap / highestMotorVel

        return v_a, v_b, v_c, v_d

    #sets global velocity to aim towards a target point - magnitude is proportional to distance
    def aim(self, target):
        displacement = sumVector3D((target, scaleVector3D(self.drivetrain.pose, -1)))

        if displacement.angle > math.pi:
            displacement.angle -= 2 * math.pi

        normalizedCorrection = scaleVector3D(displacement, 1 / displacement.getMagnitude())

        distanceToTarget = displacement.getMagnitude()

        self.globalVelocity = scaleVector3D(normalizedCorrection, distanceToTarget * self.Kp)
    
    #gets next target point on path
    def getNextTarget(self):
        for i in range(self.lastWaypointIndex, len(self.path.waypoints)):
            waypoint = self.path.waypoints[i]

            displacement = sumVector3D((waypoint, scaleVector3D(self.drivetrain.pose, -1)))

            if displacement.getMagnitude() > self.lookahead:
                break

        self.lastWaypointIndex = i
        
        return waypoint

    #updates and sets individual motor velocities to follow path
    def update(self):
        self.aim(self.getNextTarget())

        v_a, v_b, v_c, v_d = self.getMotorVels()
        self.drivetrain.setMotorVels(v_a, v_b, v_c, v_d)

        root.after(10, self.update)

#represents a path for the robot to follow
class Path():
    def __init__(self, canvas, steps):
        self.start = Vector3D()
        self.end = Vector3D()
        self.startTan = Vector3D()
        self.endTan = Vector3D()

        self.steps = steps

        self.waypoints = []

        self.canvas = canvas
        self.pointSizeIn = 0.2
    
    #generates list of pose waypoints
    def generate(self, lockAngle = None):
        for i in range(1, self.steps + 1):
            t = i / self.steps

            h3 = sumVector3D((scaleVector3D(self.start, 2), scaleVector3D(self.end, -2), self.startTan, self.endTan))
            h2 = sumVector3D((scaleVector3D(self.start, -3), scaleVector3D(self.end, 3), scaleVector3D(self.startTan, -2), scaleVector3D(self.endTan, -1)))
            h1 = self.startTan
            h0 = self.start

            waypoint = Vector3D()
            waypoint = sumVector3D((scaleVector3D(h3, t**3), scaleVector3D(h2, t**2), scaleVector3D(h1, t), h0))

            if lockAngle != None:
                waypoint.angle = lockAngle
            else:
                waypointPoseDeriv = sumVector3D((scaleVector3D(h3, 3*(t**2)), scaleVector3D(h2, 2*t), h1))
                
                if waypointPoseDeriv.x == 0:
                    if waypointPoseDeriv.y < 0:
                        waypoint.angle = math.pi
                    else:
                        waypoint.angle = 0
                else:
                    waypoint.angle = math.atan(waypointPoseDeriv.y / waypointPoseDeriv.x)

                    if (waypoint.angle > 0 and waypointPoseDeriv.y < 0) or (waypoint.angle < 0 and waypointPoseDeriv.x < 0):
                        waypoint.angle += math.pi
                    
                    waypoint.angle -= math.pi / 2
            
            self.waypoints.append(waypoint)
    
    #draws waypoints on Canvas
    def draw(self):
        for waypoint in self.waypoints:
            self.canvas.update()
            canvasX, canvasY = getCanvasCoords(self.canvas, waypoint.x, waypoint.y)

            self.canvas.create_oval((canvasX - self.pointSizeIn * PX_PER_IN / 2, canvasY - self.pointSizeIn * PX_PER_IN / 2, canvasX + self.pointSizeIn * PX_PER_IN / 2, canvasY + self.pointSizeIn * PX_PER_IN / 2), fill=PATH_COLOR)

#functions
#rotates a 2 dimensional vector by theta radians
def rotate(i, j, theta):
    x = i * math.cos(theta) - j * math.sin(theta)
    y = i * math.sin(theta) + j * math.cos(theta)

    return x, y

#multiplies a vector by a scalar
def scaleVector3D(vector, scalar):
    return Vector3D(vector.x * scalar, vector.y * scalar, vector.angle * scalar)

#adds vectors in a list
def sumVector3D(vectors):
    x = 0
    y = 0
    angle = 0

    for vector in vectors:
        x += vector.x
        y += vector.y
        angle += vector.angle
    
    return Vector3D(x, y, angle)

#converts custom inch coordinate system to Canvas coordinates
def getCanvasCoords(canvas, x, y):
    canvasX, canvasY = x * PX_PER_IN + canvas.winfo_width() / 2, -y * PX_PER_IN + canvas.winfo_height() / 2

    return canvasX, canvasY

#gets parameters from user and constructs new simulation by replacing global class instances
def constructSimulation(canvas, drivetrainImage):
    global drivetrain
    global path
    global controller

    global drivetrainProcess
    global controllerProcess
    
    if drivetrainProcess:
        root.after_cancel(drivetrainProcess)
    if controllerProcess:
        root.after_cancel(controllerProcess)

    try:
        pathStartX = float(pathStartXEntry.get())
        pathStartY = float(pathStartYEntry.get())
        pathStartTanX = float(pathStartTanXEntry.get())
        pathStartTanY = float(pathStartTanYEntry.get())
        pathEndX = float(pathEndXEntry.get())
        pathEndY = float(pathEndYEntry.get())
        pathEndTanX = float(pathEndTanXEntry.get())
        pathEndTanY = float(pathEndTanYEntry.get())
        pathAngleLock = float(pathAngleLockEntry.get()) if pathAngleLockEntry.get() != "" else None
        pathSteps = int(pathStepsEntry.get())
        drivetrainX = float(drivetrainXEntry.get())
        drivetrainY = float(drivetrainYEntry.get())
        drivetrainTheta = float(drivetrainThetaEntry.get())
        drivetrainRadius = float(drivetrainRadiusEntry.get())
        drivetrainMotorCap = float(drivetrainMotorCapEntry.get())
        controllerLookahead = float(controllerLookaheadEntry.get())
        controllerKp = float(controllerKpEntry.get())
        controllerMotorAccelCap = float(controllerMotorAccelCapEntry.get())
    except:
        return

    canvas.delete("all")

    drivetrain = VirtualDrivetrain(drivetrainRadius, drivetrainMotorCap, canvas, drivetrainImage)
    drivetrain.pose = Vector3D(drivetrainX, drivetrainY, drivetrainTheta)

    path = Path(canvas, pathSteps)

    path.start = Vector3D(pathStartX, pathStartY)
    path.end = Vector3D(pathEndX, pathEndY)
    path.startTan = Vector3D(pathStartTanX, pathStartTanY)
    path.endTan = Vector3D(pathEndTanX, pathEndTanY)

    path.generate(pathAngleLock)
    path.draw()

    controller = DrivetrainController(drivetrain, path, controllerLookahead, controllerKp, controllerMotorAccelCap)
        
    drivetrain.lastUpdateTimestamp = time.perf_counter()
    controller.lastUpdateTimestamp = time.perf_counter()

    drivetrainProcess = root.after(0, drivetrain.update)
    controllerProcess = root.after(0, controller.update)

#application setup
root = tk.Tk()
root.title("Pathing Simulator v0.1")
root.iconbitmap("favicon.ico")
root.state('zoomed')

ttk.Style().configure("controls.TFrame", background=CONTROLS_COLOR)
ttk.Style().configure("text.TLabel", background=CONTROLS_COLOR, font=("Calibri", 10), justify="center")

#root children
display = tk.Canvas(root, background=DISPLAY_COLOR)
display.grid(column=0, row=0, sticky="nsew")

controls = ttk.Frame(root, style="controls.TFrame", relief="raised", borderwidth=20)
controls.grid(column=1, row=0, sticky="nsew")

root.columnconfigure(0, weight=3, uniform="root")
root.columnconfigure(1, weight=1, uniform="root")
root.rowconfigure(0, weight=1)

#controls children
#path entries
pathLabel = ttk.Label(controls, text="Path Controls", style="text.TLabel")
pathLabel.grid(column=0, row=1, columnspan=4)

pathStartXLabel = ttk.Label(controls, text="Start X: ", style="text.TLabel")
pathStartXLabel.grid(column=0, row=2, sticky="e")

pathStartXEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathStartXEntry.grid(column=1, row=2, sticky="w")

pathStartYLabel = ttk.Label(controls, text="Start Y: ", style="text.TLabel")
pathStartYLabel.grid(column=2, row=2, sticky="e")

pathStartYEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathStartYEntry.grid(column=3, row=2, sticky="w")

pathStartTanXLabel = ttk.Label(controls, text="Start Tan. X: ", style="text.TLabel")
pathStartTanXLabel.grid(column=0, row=3, sticky="e")

pathStartTanXEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathStartTanXEntry.grid(column=1, row=3, sticky="w")

pathStartTanYLabel = ttk.Label(controls, text="Start Tan. Y: ", style="text.TLabel")
pathStartTanYLabel.grid(column=2, row=3, sticky="e")

pathStartTanYEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathStartTanYEntry.grid(column=3, row=3, sticky="w")

pathEndXLabel = ttk.Label(controls, text="End X: ", style="text.TLabel")
pathEndXLabel.grid(column=0, row=4, sticky="e")

pathEndXEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathEndXEntry.grid(column=1, row=4, sticky="w")

pathEndYLabel = ttk.Label(controls, text="End Y: ", style="text.TLabel")
pathEndYLabel.grid(column=2, row=4, sticky="e")

pathEndYEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathEndYEntry.grid(column=3, row=4, sticky="w")

pathEndTanXLabel = ttk.Label(controls, text="End Tan. X: ", style="text.TLabel")
pathEndTanXLabel.grid(column=0, row=5, sticky="e")

pathEndTanXEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathEndTanXEntry.grid(column=1, row=5, sticky="w")

pathEndTanYLabel = ttk.Label(controls, text="End Tan. Y: ", style="text.TLabel")
pathEndTanYLabel.grid(column=2, row=5, sticky="e")

pathEndTanYEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathEndTanYEntry.grid(column=3, row=5, sticky="w")

pathAngleLockLabel = ttk.Label(controls, text="Angle Lock: ", style="text.TLabel")
pathAngleLockLabel.grid(column=0, row=6, sticky="e")

pathAngleLockEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathAngleLockEntry.grid(column=1, row=6, sticky="w")

pathStepsLabel = ttk.Label(controls, text="Steps: ", style="text.TLabel")
pathStepsLabel.grid(column=2, row=6, sticky="e")

pathStepsEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
pathStepsEntry.grid(column=3, row=6, sticky="w")

#drivetrain entries
drivetrainLabel = ttk.Label(controls, text="Drivetrain Setup", style="text.TLabel")
drivetrainLabel.grid(column=0, row=7, columnspan=4)

drivetrainXLabel = ttk.Label(controls, text="X: ", style="text.TLabel")
drivetrainXLabel.grid(column=0, row=8, sticky="e")

drivetrainXEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
drivetrainXEntry.grid(column=1, row=8, sticky="w")

drivetrainYLabel = ttk.Label(controls, text="Y: ", style="text.TLabel")
drivetrainYLabel.grid(column=2, row=8, sticky="e")

drivetrainYEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
drivetrainYEntry.grid(column=3, row=8, sticky="w")

drivetrainThetaLabel = ttk.Label(controls, text="Θ: ", style="text.TLabel")
drivetrainThetaLabel.grid(column=0, row=9, sticky="e")

drivetrainThetaEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
drivetrainThetaEntry.grid(column=1, row=9, sticky="w")

drivetrainRadiusLabel = ttk.Label(controls, text="Track Radius: ", style="text.TLabel")
drivetrainRadiusLabel.grid(column=0, row=10, sticky="e")

drivetrainRadiusEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
drivetrainRadiusEntry.grid(column=1, row=10, sticky="w")

drivetrainMotorCapLabel = ttk.Label(controls, text="Motor Vel Cap: ", style="text.TLabel")
drivetrainMotorCapLabel.grid(column=2, row=10, sticky="e")

drivetrainMotorCapEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
drivetrainMotorCapEntry.grid(column=3, row=10, sticky="w")

#controller entries
controllerLabel = ttk.Label(controls, text="Controller Setup", style="text.TLabel")
controllerLabel.grid(column=0, row=11, columnspan=4)

controllerLookaheadLabel = ttk.Label(controls, text="Lookahead: ", style="text.TLabel")
controllerLookaheadLabel.grid(column=0, row=12, sticky="e")

controllerLookaheadEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
controllerLookaheadEntry.grid(column=1, row=12, sticky="w")

controllerKpLabel = ttk.Label(controls, text="Kp: ", style="text.TLabel")
controllerKpLabel.grid(column=2, row=12, sticky="e")

controllerKpEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
controllerKpEntry.grid(column=3, row=12, sticky="w")

controllerMotorAccelCapLabel = ttk.Label(controls, text="Motor Accel Cap: ", style="text.TLabel")
controllerMotorAccelCapLabel.grid(column=0, row=13, sticky="e")

controllerMotorAccelCapEntry = ttk.Entry(controls, width=ENTRY_WIDTH)
controllerMotorAccelCapEntry.grid(column=1, row=13, sticky="w")

#construct button to call constructSimulation()
constructButton = ttk.Button(controls, command=lambda: constructSimulation(display, "images/x_drive.png"), text="Construct Simulation!", width=BUTTON_WIDTH)
constructButton.grid(column=0, row=15, columnspan=4)

#configure grid
controls.columnconfigure(0, weight=4, uniform="controls")
controls.columnconfigure(1, weight=3, uniform="controls")
controls.columnconfigure(2, weight=4, uniform="controls")
controls.columnconfigure(3, weight=3, uniform="controls")

controls.rowconfigure(0, weight=1, uniform="controls")
for col in range(1, 20):
    controls.rowconfigure(col, weight=2, uniform="controls")

#set default entry values
pathStartXEntry.insert(0, "0")
pathStartYEntry.insert(0, "0")
pathStartTanXEntry.insert(0, "0")
pathStartTanYEntry.insert(0, "120")
pathEndXEntry.insert(0, "72")
pathEndYEntry.insert(0, "72")
pathEndTanXEntry.insert(0, "0")
pathEndTanYEntry.insert(0, "120")
pathAngleLockEntry.insert(0, "")
pathStepsEntry.insert(0, "100")
drivetrainXEntry.insert(0, "0")
drivetrainYEntry.insert(0, "0")
drivetrainThetaEntry.insert(0, "0")
drivetrainRadiusEntry.insert(0, "9.51")
drivetrainMotorCapEntry.insert(0, "30")
controllerLookaheadEntry.insert(0, "12")
controllerKpEntry.insert(0, "1.5")
controllerMotorAccelCapEntry.insert(0, "20")

#construct simulation for first time
constructSimulation(display, "images/x_drive.png")

#main loop
root.mainloop()