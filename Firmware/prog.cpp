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
