%% FMCW RADAR SIMULATION & VISUAL SCOPE
clear; clc; close all;

%% 1. SYSTEM PARAMETERS
c = 3e8;                    % Speed of light (m/s)
fc = 2.4e9;                 % 2.4 GHz
B = 100e6;                  % 100 MHz Bandwidth
Tsweep = 0.0064;            % 6.4 ms sweep time
N_samples = 512;            % ADC samples
Fs = N_samples / Tsweep;    % Sampling frequency
slope = B / Tsweep;         % Chirp rate

%% 2. DEFINE TARGETS: [Distance (m), Azimuth Angle (deg), Signal Strength]
targets = [
    25.0,  45.0,  1.0;   % Target 1: 25m at 45 degrees
    60.0, -30.0,  0.6;   % Target 2: 60m at -30 degrees
    ];

%% 3. DSP ENGINE (FFT Calculation)
t = linspace(0, Tsweep, N_samples);
tx_phase = 2*pi*(fc*t + 0.5*slope*(t.^2));
rx_signal = zeros(1, N_samples);

for i = 1:size(targets, 1)
    tau = (2 * targets(i,1)) / c;
    t_delay = t - tau;
    rx_phase = 2*pi*(fc*t_delay + 0.5*slope*(t_delay.^2));
    rx_signal = rx_signal + targets(i,3) * cos(rx_phase);
end

% Add Noise Floor & Down-convert
rx_signal = rx_signal + 0.08 * randn(1, N_samples);
if_signal = cos(tx_phase) .* rx_signal;

% FFT Range Profile
windowed_if = if_signal .* hamming(N_samples)';
fft_out = fft(windowed_if, N_samples);
fft_mag = abs(fft_out(1:N_samples/2));
fft_mag = fft_mag / max(fft_mag);

freq_axis = (0:(N_samples/2)-1) * (Fs / N_samples);
range_axis = (c * Tsweep * freq_axis) / (2 * B);

%% 4. PLOT 1: HIGH-CONTRAST DSP DIAGNOSTICS
figure('Name', 'FMCW Radar - DSP Signal Analysis', 'Color', [0.1 0.1 0.1]);

subplot(2,1,1);
plot(t * 1e3, if_signal, 'Color', [0 0.8 1], 'LineWidth', 1.2);
title('Raw Baseband Beat Signal (Voltage vs Time)', 'Color', 'w', 'FontSize', 12);
xlabel('Time (ms)', 'Color', 'w'); ylabel('Voltage (V)', 'Color', 'w');
set(gca, 'Color', [0.05 0.05 0.05], 'XColor', 'w', 'YColor', 'w');
grid on;

subplot(2,1,2);
plot(range_axis, 20*log10(fft_mag + 1e-6), 'Color', [0 1 0.4], 'LineWidth', 1.5);
title('FFT Range Profile (Target Peaks)', 'Color', 'w', 'FontSize', 12);
xlabel('Range (Meters)', 'Color', 'w'); ylabel('Magnitude (dB)', 'Color', 'w');
xlim([0, 100]); ylim([-40, 0]);
set(gca, 'Color', [0.05 0.05 0.05], 'XColor', 'w', 'YColor', 'w');
grid on;

%% 5. PLOT 2: VISUAL RADAR SCOPE
figure('Name', 'Tactical Radar Scope Output', 'Color', [0.05 0.05 0.05]);
polarplot(0, 0); hold on;

% Draw Range Rings
r_rings = [25, 50, 75, 100];
for r = r_rings
    th = linspace(0, 2*pi, 100);
    polarplot(th, r*ones(size(th)), ':', 'Color', [0 0.3 0.1]);
end

% Plot Detected Targets on Scope
for i = 1:size(targets, 1)
    az_rad = deg2rad(targets(i,2));
    r_dist = targets(i,1);
    polarplot(az_rad, r_dist, 'ro', 'MarkerSize', 10, 'LineWidth', 2, 'MarkerFaceColor', 'r');
    text(az_rad + 0.05, r_dist, sprintf(' Target: %.1fm', r_dist), 'Color', 'w', 'FontWeight', 'bold');
end

title('Simulated 2D Radar Target Map', 'Color', [0 1 0.4], 'FontSize', 14);
set(gca, 'Color', [0.02 0.02 0.02], 'ThetaColor', [0 0.8 0.3], 'RColor', [0 0.8 0.3]);
rlim([0 100]);