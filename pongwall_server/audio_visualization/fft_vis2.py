import pyaudio
import numpy as np
import signal
import time
import aubio

SAMPLE_RATE = 44100
TIME_STEP = 1 / SAMPLE_RATE

BUFFER_SIZE = 2048

NEXT_FFT_TIME = time.monotonic() + 1


def _callback(in_data, frame_count, time_info, status):
    global NEXT_FFT_TIME
    if NEXT_FFT_TIME < time.monotonic():
        NEXT_FFT_TIME = NEXT_FFT_TIME + (1 / 20)

        audio_buffer = np.frombuffer(in_data, dtype=np.float32)

        print(chr(27) + "[2J")
        print("\033[H")
        fft = aubio.fft(BUFFER_SIZE)(audio_buffer)
        fb = aubio.filterbank(400, BUFFER_SIZE)
        fb.set_power(2)
        freqs = np.linspace(0, 20_000, 402)
        fb.set_triangle_bands(aubio.fvec(freqs), SAMPLE_RATE)

        output = np.around(fb(fft), 2)
        freqs = np.around(freqs[1:-1], 2)
        # print(np.column_stack((np.around(freqs[1:-1], 2), output)))

        for bin, amplitude in np.column_stack((freqs, output)):
            if amplitude > 1:
                print(f"{bin}: {amplitude}")

    return None, pyaudio.paContinue


def main():
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=BUFFER_SIZE,
        stream_callback=_callback,
    )

    signal.pause()


if __name__ == "__main__":
    main()
