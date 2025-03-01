from pathlib import Path
import pytest
from seavad.main import SeaVAD

@pytest.fixture
def seavad():
    sample_rate = 16000
    sample_width = 2
    return SeaVAD(sample_rate=sample_rate, sample_width=sample_width)

def test_get_vad_segments(seavad):
    # Read test audio byte sequence
    audio_path = Path(__file__).parent.parent / "data/test_audio/16k_en_zh.wav"
    with open(audio_path, "rb") as f:
        audio = f.read()

    # Call get_vad_segments and check the result
    segments = seavad.get_vad_segments(audio)
    expected_segments = [(1.376, 2.784), (4.512, 6.368)]
    assert segments == expected_segments
