#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrapper with helper function to run vad to analyze frames."""

import audioop
import asyncio
from pathlib import Path
from typing import List, Tuple
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

from seavad.silero import SileroVADAnalyzer


class SeaVAD:
    def __init__(
        self,
        model_file_path: str,
        sample_rate: int,
        sample_width: int,
        vad_on_needed: int = 5,
        vad_off_needed: int = 20,
        logger: logging.Logger = logger
    ):
        """
        Initialize the SeaVAD class with the given parameters.

        Args:
            sample_rate (int): The sample rate of the audio.
            vad_on_needed (int): Number of consecutive VAD detected frames to switch on state.
            vad_off_needed (int): Number of consecutive no VAD detected frames to switch to off state.
            logger (logging.Logger): Logger instance for logging information and errors.
        """
        self.sample_rate = sample_rate
        self.sample_width = sample_width
        assert Path(model_file_path).exists(), f"VAD model file {model_file_path} does not exist"
        self.vad = SileroVADAnalyzer(model_file_path=model_file_path, sample_rate=sample_rate)
        self.vad_detected = asyncio.Event()
        self.vad_buffer = b''
        self.vad_bytes_per_chunk = self.vad.num_frames_required() * 2
        self.vad_consecutive_frames = 0
        self.vad_on_consecutive_needed = vad_on_needed
        self.vad_off_consecutive_needed = vad_off_needed
        self.prev_vad_state = False
        self.peak_vad_on = 0  # Highest number of vad on frames
        self.logger = logger

    def vad_analyze_frame(self, chunk: bytes, is_ulaw: bool = False):
        """Analyze incoming audio chunk for voice activity."""
        try:
            if is_ulaw:
                chunk = audioop.ulaw2lin(chunk, 2)
            self.vad_buffer += chunk
            if len(self.vad_buffer) > self.vad_bytes_per_chunk:
                for i in range(0, len(self.vad_buffer), self.vad_bytes_per_chunk):
                    vad_frame = self.vad_buffer[i:i + self.vad_bytes_per_chunk]
                    if len(vad_frame) < self.vad_bytes_per_chunk:
                        continue
                    vad_state = self.vad.voice_confidence(vad_frame) > .75
                    if vad_state == self.prev_vad_state:
                        self.vad_consecutive_frames += 1
                        if vad_state:
                            self.peak_vad_on += 1
                            if self.vad_consecutive_frames >= self.vad_on_consecutive_needed:
                                self.vad_detected.set()
                        else:
                            if self.vad_consecutive_frames >= self.vad_off_consecutive_needed:
                                self.vad_detected.clear()
                    else:
                        self.vad_consecutive_frames = 0
                    self.prev_vad_state = vad_state

                self.vad_buffer = b''
        except Exception as e:
            self.logger.error(f"Failed VAD analysis audio: {e}")

    def get_vad_segments(self, audio: bytes) -> List[Tuple[float, float]]:
        """Get a list of start/stop timestamps for VAD segment for the given audio bytes.

        Args:
            audio (bytes): The audio data to analyze.

        Returns:
            List[float]: A list of tuples representing the start and stop times of voice activity segments.
        """
        segments = []
        chunk_size = self.vad_bytes_per_chunk
        num_chunks = len(audio) // chunk_size
        start_time = None

        for i in range(num_chunks):
            chunk = audio[i * chunk_size:(i + 1) * chunk_size]
            self.vad_analyze_frame(chunk)
            if self.vad_detected.is_set():
                if start_time is None:
                    start_time = (i * chunk_size / self.sample_width) / self.vad.sample_rate
            else:
                if start_time is not None:
                    end_time = (i * chunk_size / self.sample_width) / self.vad.sample_rate
                    segments.append((start_time, end_time))
                    start_time = None

        if start_time is not None:
            segments.append((start_time, len(audio) / self.vad.sample_rate))

        return segments