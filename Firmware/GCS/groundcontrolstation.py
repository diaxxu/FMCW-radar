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

