import torch
from TTS.api import TTS
from pydub import AudioSegment

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "cpu"

print("Using device:", device)

# List available 🐸TTS models
# print(TTS().list_models()._list_models())

# Init TTS



# Init TTS with the target model name
# tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False).to(device)

# # Run TTS
# tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path="/Users/rudolfkischer/Projects/PodcastGPT/trainingAudio/lex_freedman_out2.wav")

# # Example voice cloning with YourTTS in English, French and Portuguese
# tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to(device)
# tts.tts_to_file("This is voice cloning.", speaker_wav="/Users/rudolfkischer/Projects/PodcastGPT/trainingAudio/lex_freedman.wav", language="en", file_path="/Users/rudolfkischer/Projects/PodcastGPT/trainingAudio/lex_freedman_out.wav")
# tts.tts_to_file("C'est le clonage de la voix.", speaker_wav="my/cloning/audio.wav", language="fr-fr", file_path="output.wav")
# tts.tts_to_file("Isso é clonagem de voz.", speaker_wav="my/cloning/audio.wav", language="pt-br", file_path="output.wav")

def get_tts(text, speaker_wav, 
            output_path,
            model = "tts_models/multilingual/multi-dataset/xtts_v2"
            ):
  tts = TTS(model,
            ).to(device)

  # Run TTS
  # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
  # Text to speech list of amplitude values as output

  #  splitext(basename(speaker_wav))[0] + ".wav"
  wav_output_path = output_path.replace(".mp3", ".wav")

  wav = tts.tts(text=text, speaker_wav=speaker_wav, language="en")
  # Text to speech to a file
  tts.tts_to_file(text=text, speaker_wav=speaker_wav, language="en", file_path=wav_output_path)


  # convert to mp3
  sound = AudioSegment.from_wav(wav_output_path)
  sound.export(output_path, format="mp3")



  return output_path


def main():
    output_path = "/Users/rudolfkischer/Projects/PodcastGPT/trainingAudio/joe_biden_out.mp3"
    speaker_wav = "/Users/rudolfkischer/Projects/PodcastGPT/trainingAudio/joe_biden.wav"
    text = "This is voice cloning. I love to talk all about the latest in AI. I am a completely synthetic voice."
    get_tts(text, speaker_wav, output_path)

if __name__ == "__main__":
    main()



  


