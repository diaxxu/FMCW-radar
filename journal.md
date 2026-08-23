# 28/07/2026 
# *time spent: 5.86h*
hello welcome im starting this project for ISPY ysws im not sure what im gonna do so i will research something im passioned about. SO i found three amazing project 
- the first one is a radar that scan the ground from a plane giving you a 2d map of this place (very usefull for spying haha) 
- the second project is microphone that can hear from long distance (meh)
-  the third one is a drone that act like a cell tower and steal all ur creditials 


alright we have some interesting project but the radar literally stole the show im sorry but building a functional radar is so much cooler than all of those so i went with the radar project  

But i dont know anything about radars and such so i went on a research journey first of all i watched some vids explaining how an overall radar work 
![alt text](pics/image.png)
but i needed to get really deep this is just surface level knowledge it won't show you how exactly a radar work or how to build it 
so i followed a serie specialising in fmcw radars that kind that go on cars and mounted on uav 
cuz there are two kind of radar a pulse radar (conventional used on jets and early warning system) its consuming heavy and pretty old technology in this project i will use a fmcw radar the difference between them is that when the fmcw radar send a pulse its continuous small pulse instead of one big pulse every 10s 
![alt text](pics/image-1.png)
this serie is really good and full of good information that i will definetly need when building this radar ahah 


also this one is really good ![alt text](pics/image-2.png) if any one is doing the same exact project i recommend that he watch those two series !! 

so after learning i decided to plan my project cuz i love planning to get as profesionnal as possibble: 

- first thing is that i should start by doing the schematics of the radar pcb i will have two pcb instead of one big pcb 
- then i will route and make the pcb 
- then make the gimbal in CAD (fusion360)
- then make the software that will run inside 
- then if i have more time i will simulate my radar in mathlab 


so for today we did research and learn new things but im too tired to continue see yall tomorow 
(if i don't slack off)

# 29/07/2026 
# *time spent: 7.51h*
heyyy im backk , lets get right into it 
so i said that im going to start by doing the schematic of the radar but i lied a bit since i need to put a scope cuz that will define our whole project like the range the power etc 
so to stay legal so i don't land in any jail ^^ we will limit our radar to 100mw this give us approximately a range of 100m and on tall buildings 500m all depend on the RCS (radar cross section) 
also its going to use a pcb patch antenna with 3d printed convex horn lined with aluminuim to straightify and give more range ^^

so opening my fav pcb software EasyEda so we need component but i don't know what component i need i had to go research with the bit of help from geminy and datasheets 

starting by the S-Band VCO Block its main job is to generates the high-frequency $2.4\text{ GHz}$ RF signal by converting the incoming $V_{\text{TUNE}}$ voltage ramp into a sweeping microwave frequency output ![alt text](pics/image-3.png)

passing into the next block the WILKINSON this circuit splits the incoming RF signal (RF_TX_OUT) equally between the transmit antenna (RF_TO_ANT) and the receiver's local oscillator (RF_LO_MIXER).
![alt text](pics/image-4.png)

This circuit multiplies the incoming target echo (RF_RX_AMP) with the reference sweep signal (RF_LO_MIXER) using a Schottky diode ring array. By down-converting the high-frequency $2.4\text{ GHz}$ signals, it extracts the low-frequency beat signal (IF_OUT_RAW) needed for range calculations.
![alt text](pics/image-5.png)


this is the ldo it steps down an incoming $+5\text{V}$ rail to a ultraclean $3.3\text{V}$ output dedicated to powering sensitive RF components like the VCO
![alt text](pics/image-6.png)

this lna block amplify weak microwave echo signals received from the antenna (RF_RX_IN) before feeding them to the mixer
![alt text](pics/image-7.png)

And finally the connector i installed 2 sma connector to connect to pcb patch antennas one for receiving and one for transmitting the 5 pin header is to connect to the next pcb we are going to do its the next thing since now the schematics of this pcb is finished 
![alt text](pics/image-8.png)


# Schematic of the second PCB 

the second board is a Baseband Signal Processing Board so my first pcb handle generating and receiving $2.4\text{ GHz}$ HF (high frequency)
the second board takes the low-frequency down-converted beat signal from the mixer and processes it so any microcontroller can read it.

so starting by the first block in our schematic : 

### *PA/VGC*

it stand for Programmable Gain Amplifier / Variable Gain Control
this op amp stage use a trim potentiometer in its feedback loop to dynamically adjust signal gain for strong or weak echo returns
![alt text](pics/image-9.png)

this next block is an Dual-Stage Power Supply Block
takes DC input via connector and regulates it down to a stable $+5\text{V}$ rail using the $\text{AMS1117-5.0}$. A secondary low-noise regulator ($\text{AP2112K-3.3}$) steps that $+5\text{V}$ down to a ultra-clean $3.3\text{V}$ rail

![alt text](pics/image-10.png)

okay so this is the Virtual Ground Generator Block it splits the $3.3\text{V}$ rail using a precision voltage divider ($R_1, R_2$) filtered by $C_3$ to create a stable $1.65\text{V}$ reference. An op-amp ($U_{1.1}$) configured as a unity-gain buffer isolates this mid-rail voltage (V_MID) so downstream AC signals can swing symmetrically without clipping on a single-supply system.

![alt text](pics/image-11.png)

Active IF Bandpass Filter Block, this circuit receives the raw beat signal (IF_OUT_RAW) from the mixer, outputting a cleaned AC beat signal (IF_BANDPASS) centered around $V_{\text{MID}}$.
![alt text](pics/image-13.png)

with the unused Op-Amp Voltage Follower Buffer its the sub unit of the mcp6002 that we used earlier i wired it as a unity-gain buffer tied to the virtual ground (V_MID) this way it prevents floating inputs from oscillating, consuming excess current, or coupling noise into the active stage

![alt text](pics/image-12.png)


Finally the headers it serve as an Inter-Board & MCU Interface Headers

- Header $H_1$ connects directly to the RF front-end board to send $+5\text{V}$ power/ground, receive the raw beat signal (IF_OUT_RAW), and route the tuning ramp (V_TUNE).
- Header $H_2$ breaks out the fully amplified/filtered analog signal (IF_ADC_IN) and $V_{\text{MID}}$ reference voltage to connect directly to the microcontroller's ADC pin.

![alt text](pics/image-14.png)

with this last block we finished the schematisation phase of the two main PCB's
![alt text](pics/image-15.png)
![alt text](pics/image-16.png)

the next phase is routing but im going to do it tomorow cuz im so tireeeeeeed now goodbye

# 30/07/2026 
# *time spent: 5.37h*
hi again today we are going to route our board after we schematisated them so lets get started 
![alt text](pics/image-17.png)
so lets arrange our component and add screw hole and route them peacefully 
![alt text](pics/image-18.png)
alright this look good i will now just route and put a ground region
![alt text](pics/image-19.png)
voila this look good 



going into the next pcb routing 
![alt text](pics/image-20.png)
arranged and looking good so far 

![alt text](pics/image-21.png)

same thing  added ground and routed 
![alt text](pics/image-22.png)

so uh this complete our phase of routing so now we did shema and routing see yall in the next one 
# 01/08/2026 
# *time spent: 4.41h*
alright i have some badnew about the latest phase we did after watching some vid on high frequency routing we did every mistake that he said a beguinner would do ![alt text](pics/image-23.png)
 so i see that in my first pcb its good but the second one need re design so that what i did with taking consideration of all what i learned from that playlist that mean no via on high freq lines and Avoid routing over split ground planes so here is the result 

![alt text](pics/image-24.png) 
also i changed it shape lol so that it counter pose directly on the first pcb 

a 3d view :

![alt text](pics/image-25.png)

with this the phase 2 is finished we should now be able to hop on cad and start designing the gimbal for the radar but i will let it for tomorow bye bye ! 


# 04/08/2026 
# *time spent: 7.6h*
hi again long time no see lets hop on cad and start designing yay ! 
so i started by importing the pcbs we made  and then i aligned the holes and fixed them with screw and nuts 

![alt text](pics/image-27.png)

then i made a platform where they both sit 

![alt text](pics/image-28.png)

and then i made the pcb patch antenna 

![alt text](pics/image-29.png)

then the convex horn lined with aluminuim foil to give more range 

![alt text](pics/image-30.png) 

after that i added a platform that hold both of the receiver and the transmitter 

![alt text](pics/image-31.png)


then come the gimbal it can do 360 degree rotation and 90 deg up and 90 deg down 

![alt text](pics/image-32.png)

added the rod that will rotate the whole assembly 
![alt text](pics/image-33.png)



![alt text](pics/image-35.png)
 
the thing that will hold all the weight and it feature two bearing its made out of aluminuim for structural stiffness

![alt text](pics/image-34.png)


added the belt that will drive the rod to turn its powered by a 360 servo motor 
![alt text](pics/image-36.png)

then added the whole assembly 


![alt text](pics/image-37.png)

finally the radom 

![alt text](pics/image-38.png)

im so tired i will go to sleep i can't ohh my legs 


# 07/08/2026 
# *time spent: 7h*

bruh i gotta stop doing long session they destroy my legs and my back anyway welcome back i took a long pause so recap we finished phase 3 which is cad 
so next phase is programming since this is going to run on an esp 32 so lets get started !! 

since im a bit bad in coding geminy will help me a bit 
so how this will work is that the esp32 internal DAC will generate a smooth $0\text{v}$ to $3.3\text{v}$ sawthoot wave so this ramp sweeps thr $2.4\text{ GHz}$ VCO across a $100\text{ MHz}$ bandwidth every $6.4\text{ ms}$.
also the esp 32 will samples the Echo Signal it will reads the filtered analog beat signal (IF_ADC_IN) from the baseband board through the ADC pin and Calculates Target Range and also Tracks Azimuth & Streams Data

so with this in mind i started coding 

```cpp
#include <Arduino.h>
#include <driver/dac.h>
#include <driver/adc.h>
#include <arduinoFFT.h>

#define DAC_RAMP_PIN    DAC_CHANNEL_1  
#define ADC_IF_PIN      34             
#define SERVO_PAN_PIN   18             

#define SAMPLES         512            
#define SAMPLING_FREQ   40000          
#define BANDWIDTH_HZ    100000000.0    
#define SWEEP_TIME_SEC  0.0064         
#define SPEED_OF_LIGHT  299792458.0    

TaskHandle_t DSP_Task_Handle;
TaskHandle_t Motor_Task_Handle;

volatile float g_target_distance = 0.0;
volatile float g_peak_frequency = 0.0;
volatile int   g_current_angle = 0;
SemaphoreHandle_t xMutex;

double vReal[SAMPLES];
double vImag[SAMPLES];

ArduinoFFT<double> FFT = ArduinoFFT<double>(vReal, vImag, SAMPLES, SAMPLING_FREQ);

void DSP_Task(void * pvParameters) {
dac_output_enable(DAC_RAMP_PIN);
  
for(;;) {
for (int step = 0; step < 256; step++) {
dac_output_voltage(DAC_RAMP_PIN, step);
delayMicroseconds(25);
    }
    
unsigned long step_time = 1000000 / SAMPLING_FREQ;
unsigned long next_sample = micros();
    
for (int i = 0; i < SAMPLES; i++) {
vReal[i] = (double)analogRead(ADC_IF_PIN);
vImag[i] = 0.0;
      
while (micros() < next_sample) {
}
      next_sample += step_time;
    }

FFT.windowing(FFTWindow::Hamming, FFTDirection::Forward);
FFT.compute(FFTDirection::Forward);
FFT.complexToMagnitude();

double peak_freq = FFT.majorPeak();

float calculated_range = (SPEED_OF_LIGHT * SWEEP_TIME_SEC * peak_freq) / (2.0 * BANDWIDTH_HZ);

if (xSemaphoreTake(xMutex, portMAX_DELAY) == pdTRUE) {
g_peak_frequency = (float)peak_freq;
     g_target_distance = calculated_range;
xSemaphoreGive(xMutex);
    }
 vTaskDelay(1 / portTICK_PERIOD_MS); 
  }
}

void Motor_Task(void * pvParameters) {
int angle = 0;
  int direction = 1;

for(;;) {
    angle += direction;
    if (angle >= 360) {
      angle = 0;
    }

    if (xSemaphoreTake(xMutex, portMAX_DELAY) == pdTRUE) {
      g_current_angle = angle;
      
      Serial.printf("{\"angle\": %d, \"dist_m\": %.2f, \"beat_hz\": %.1f}\n", 
                    g_current_angle, g_target_distance, g_peak_frequency);
                    
      xSemaphoreGive(xMutex);
    }

    vTaskDelay(20 / portTICK_PERIOD_MS); 
  }
}

void setup() {
  Serial.begin(115200);
  
  analogReadResolution(12); 
  pinMode(ADC_IF_PIN, INPUT);

  xMutex = xSemaphoreCreateMutex();

  xTaskCreatePinnedToCore(
    DSP_Task,
  "DSP_Engine",
10000,
    NULL,
    2,
   &DSP_Task_Handle,
    0
  );

  xTaskCreatePinnedToCore(
    Motor_Task,
  "Motor_Engine",
  4000,
    1,
 &Motor_Task_Handle,
    1
  );
}

void loop() {
  vTaskDelete(NULL);
}
```

this is all for today see yall another day ! 

# 15/08/2026 
# *time spent: 4.9h*
hi a little recap so last time we finished phase 4 which was uh coding the program that will run inside the esp32 now we are going to code the Ground Control Station to make cool radar scope and features 

alr since i don't have the radar with me now we will use real simulation to test the ground station first we will use python to build the app don't worry guys ill make sure to make it green like spying and movie ish just let me cook ahahah
![alt text](pics/image-39.png) 

what do you guys think wait i will add some functionalities 
i added one where you scan a sector instead of 360 scan also added a target tracking but it doesn seem to work lol 
![alt text](pics/image-40.png)

![alt text](pics/image-41.png)
i added a hard lock so let me explain the radar slew back the last knew position of the target then start scanning back for it so when it catch again it doesnt go past it like standart 360 radar it keep a hard lock on it 
![alt text](pics/image-42.png)

also added a slider for filtering noise so a target appear only once instead of multiple thats it for today 

```
import sys
import json
import math
import serial
import serial.tools.list_ports
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QPushButton, QSlider)
from PyQt6.QtCore import QTimer, Qt
import pyqtgraph as pg

class HardwareRadarGCS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FMCW Radar GCS - Live Hardware")
        self.resize(900, 900)

        self.setStyleSheet("""
            QMainWindow { background-color: #0a0a0a; }
            QWidget { background-color: #0a0a0a; color: #00ff66; font-family: 'Consolas', monospace; font-size: 12px; }
            QLabel { color: #00ff66; font-weight: bold; }
            QPushButton { 
                background-color: #141414; 
                color: #00ff66; 
                border: 1px solid #00441b; 
                padding: 6px 14px; 
                border-radius: 2px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #00441b; color: #ffffff; }
            QPushButton:checked { background-color: #00ff66; color: #000000; border: 1px solid #00ff66; }
            QSlider::groove:horizontal { height: 4px; background: #141414; }
            QSlider::handle:horizontal { background: #00ff66; width: 12px; margin: -4px 0; border-radius: 2px; }
        """)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Telemetry & Status
        self.status_label = QLabel("STATUS: DISCONNECTED | AWAITING SERIAL DATA...")
        main_layout.addWidget(self.status_label)

        # Radar Scope
        self.win = pg.GraphicsLayoutWidget()
        main_layout.addWidget(self.win)
        
        self.plot = self.win.addPlot()
        self.plot.setAspectLocked(True)
        self.plot.showGrid(x=False, y=False)
        self.plot.setXRange(-100, 100)
        self.plot.setYRange(-100, 100)
        self.plot.hideAxis('bottom')
        self.plot.hideAxis('left')

        for r in [25, 50, 75, 100]:
            theta = np.linspace(0, 2 * np.pi, 200)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            self.plot.plot(x, y, pen=pg.mkPen(color=(0, 60, 25), width=1, style=Qt.PenStyle.DashLine))

        self.plot.plot([-100, 100], [0, 0], pen=pg.mkPen(color=(0, 40, 15), width=1))
        self.plot.plot([0, 0], [-100, 100], pen=pg.mkPen(color=(0, 40, 15), width=1))

        self.sweep_line = self.plot.plot([0, 0], [0, 100], pen=pg.mkPen(color=(0, 255, 102), width=2))
        self.targets = pg.ScatterPlotItem(size=8, pen=pg.mkPen(None), brush=pg.mkBrush(0, 255, 102, 240))
        self.plot.addItem(self.targets)
        
        self.lock_box = pg.ScatterPlotItem(size=18, symbol='cross', pen=pg.mkPen(color=(255, 50, 50), width=1.5), brush=pg.mkBrush(None))
        self.plot.addItem(self.lock_box)

        # Tactical Controls
        bottom_bar = QHBoxLayout()
        main_layout.addLayout(bottom_bar)

        self.btn_tx = QPushButton("TX / STBY")
        self.btn_tx.setCheckable(True)
        self.btn_tx.setChecked(True)
        self.btn_tx.clicked.connect(self.cmd_toggle_tx)
        bottom_bar.addWidget(self.btn_tx)

        self.btn_tws = QPushButton("TWS (360 SCAN)")
        self.btn_tws.setCheckable(True)
        self.btn_tws.setChecked(True)
        self.btn_tws.clicked.connect(self.cmd_mode_tws)
        bottom_bar.addWidget(self.btn_tws)

        self.btn_sector = QPushButton("SET SECTOR")
        self.btn_sector.clicked.connect(self.cmd_sector_click)
        bottom_bar.addWidget(self.btn_sector)

        self.btn_stt = QPushButton("STT (HARD LOCK)")
        self.btn_stt.setCheckable(True)
        self.btn_stt.clicked.connect(self.cmd_mode_stt)
        bottom_bar.addWidget(self.btn_stt)

        bottom_bar.addWidget(QLabel("  GCS CLUTTER FILTER:"))
        self.slider_filter = QSlider(Qt.Orientation.Horizontal)
        self.slider_filter.setRange(0, 20)  # Filter out targets within X meters
        self.slider_filter.setValue(2)
        self.slider_filter.setFixedWidth(100)
        bottom_bar.addWidget(self.slider_filter)

        # Hardware Comms & State
        self.serial_port = None
        self.target_points = []
        self.current_azimuth = 0.0
        self.sector_clicks = 0
        self.sector_bounds = [0, 360]

        self.init_serial()

        # Update loop runs fast to catch all serial buffer data
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_hardware)
        self.timer.start(10)

    def init_serial(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if any(id_str in p.description for id_str in ["USB", "UART", "CH340"]):
                try:
                    self.serial_port = serial.Serial(p.device, 115200, timeout=0.01)
                    return
                except Exception:
                    pass

    def send_cmd(self, command_dict):
        """Sends JSON command to the hardware MCU."""
        if self.serial_port and self.serial_port.is_open:
            msg = json.dumps(command_dict) + '\n'
            self.serial_port.write(msg.encode('utf-8'))

    # --- COMMAND SENDERS ---
    def cmd_toggle_tx(self):
        state = "TX_ON" if self.btn_tx.isChecked() else "STBY"
        self.send_cmd({"cmd": "EMCON", "state": state})
        if state == "STBY":
            self.sweep_line.setData([0, 0], [0, 0])

    def cmd_mode_tws(self):
        self.btn_tws.setChecked(True)
        self.btn_stt.setChecked(False)
        self.btn_sector.setText("SET SECTOR")
        self.sector_clicks = 0
        self.send_cmd({"cmd": "MODE", "type": "TWS"})

    def cmd_sector_click(self):
        if self.sector_clicks == 0:
            self.sector_bounds[0] = self.current_azimuth
            self.sector_clicks = 1
            self.btn_sector.setText(f"SEC A: {int(self.current_azimuth)}° (CLICK AGAIN)")
        elif self.sector_clicks == 1:
            self.sector_bounds[1] = self.current_azimuth
            self.sector_clicks = 0
            self.btn_sector.setText(f"SEC: {int(self.sector_bounds[0])}° - {int(self.sector_bounds[1])}°")
            self.btn_tws.setChecked(False)
            self.btn_stt.setChecked(False)
            self.send_cmd({
                "cmd": "MODE", 
                "type": "SECTOR", 
                "min": self.sector_bounds[0], 
                "max": self.sector_bounds[1]
            })

    def cmd_mode_stt(self):
        self.btn_stt.setChecked(True)
        self.btn_tws.setChecked(False)
        self.btn_sector.setText("SET SECTOR")
        self.sector_clicks = 0
        
        # Send STT command with the azimuth of the last detected target
        target_az = self.current_azimuth
        if self.target_points:
            pt = self.target_points[-1]
            az = math.degrees(math.atan2(pt['x'], pt['y']))
            target_az = az if az >= 0 else az + 360

        self.send_cmd({"cmd": "MODE", "type": "STT", "target_az": target_az})

    # --- HARDWARE LISTENER ---
    def read_hardware(self):
        if not self.serial_port or not self.serial_port.is_open:
            return

        try:
            # Read all available lines in buffer to prevent serial lag
            while self.serial_port.in_waiting:
                line = self.serial_port.readline().decode('utf-8').strip()
                if not line.startswith("{"): continue

                data = json.loads(line)
                self.current_azimuth = data.get("angle", self.current_azimuth)
                dist_m = data.get("dist_m", 0.0)
                locked = data.get("locked", False)  # Hardware confirms if it holds STT lock

                # Update Sweep Line Position
                rad = math.radians(self.current_azimuth)
                if self.btn_tx.isChecked():
                    self.sweep_line.setData([0, 100 * math.sin(rad)], [0, 100 * math.cos(rad)])

                # Plot valid targets (applying local STC clutter filter)
                if dist_m > self.slider_filter.value():
                    tx = dist_m * math.sin(rad)
                    ty = dist_m * math.cos(rad)
                    self.target_points.append({'x': tx, 'y': ty, 'dist': dist_m, 'life': 1.0, 'locked': locked})

        except Exception as e:
            pass

        self.process_visuals()

    def process_visuals(self):
        pos = []
        closest_target = None
        min_d = 999.0
        updated_points = []
        is_locked = False

        # Decay targets over time
        for pt in self.target_points:
            pt['life'] -= 0.015
            if pt['life'] > 0:
                pos.append({'pos': (pt['x'], pt['y'])})
                updated_points.append(pt)
                
                if pt.get('locked', False):
                    is_locked = True
                    closest_target = pt
                elif pt['dist'] < min_d and not is_locked:
                    min_d = pt['dist']
                    closest_target = pt

        self.target_points = updated_points
        self.targets.setData(pos)

        # Update Top Telemetry UI
        if is_locked and closest_target:
            self.lock_box.setData([{'pos': (closest_target['x'], closest_target['y'])}])
            self.status_label.setText(f"STT: LOCKED | AZ: {self.current_azimuth:03.0f}° | RANGE: {closest_target['dist']:.1f}m")
        else:
            self.lock_box.setData([])
            mode_text = "STANDBY" if not self.btn_tx.isChecked() else "SCANNING"
            self.status_label.setText(f"MODE: {mode_text} | AZ: {self.current_azimuth:03.0f}° | TRACKS: {len(pos)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gcs = HardwareRadarGCS()
    gcs.show()
    sys.exit(app.exec())

```

# 18/08/2026 
# *time spent: 5.22h*

hi again recap time yay : so

- phase 1 was schema : done 
- phase 2 was routing : done
- phase 3 was cad : done 
- phase 4 was programming : done 
- phase 5 was ground control station : done 
- phase 6 is simulation of the radar in Mathlabs : currently working on it 


so lets get into it without wasting any time: first of all what is matlab definition from google MATLAB (short for Matrix Laboratory) is a proprietary high-level programming language and numeric computing environment developed by MathWorks, designed primarily for engineers and scientists. 

ok so what i will do is because i don't have the hardware with me i will put the code that we generated earlier that will run on the esp32 i will put it inside a simulator in mathlab and if the code don't work it will mean that even if i had the esp32 with all the hardware it won't work so lets test it 
![alt text](pics/image-43.png)

SUCCESS !!! let me explain the top graph is the raw AC voltage coming out of the MCP6002 op-amp stage. It looks like chaotic noise because it contains two different frequency sine waves mixed together !!! 

the bottom graph is what the ESP32 calculates after running the FFT
you can see a 2 spike in the bottom graph those are targets 

let me make this better to see 


![alt text](pics/image-44.png)

alright much better so now we confirmed that the math is working greattt 
here is what happened in depth script took the exact radar specifications ($2.4\text{ GHz}$, $100\text{ MHz}$ bandwidth, $6.4\text{ ms}$ sweep time) and calculated how much time delay a radio wave would experience bouncing off an object at 25 meters and 60 meters.

It mathematically generated the transmit chirp wave, delayed it, bounced it back, and multiplied them together (mixing) just like how the real life hardware would do 
it also ran a real mathematical Fast Fourier Transform (FFT) the exact same mathematical algorithm you are coding into the ESP32.

ou shii ![alt text](pics/image-45.png) since im using matlab free version i only have 20 hours per month :scared_skull: 

# 22/08/2026 
# *time spent: 2h*

so i made a github repo filled it withall necessary file and such wrote the readme.md also organised the repo as correctly as possible added image to polish and renders 
also i spend over 2h on journalling on this project ![alt text](pics/image67.png)
i hope you like my project <3