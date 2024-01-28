

# we want to be able to take an mp3 file 
# of a host and a guest talking
# get a word level transcript of the audio using whisper
# it should be diarized so we know who is talking

# then we want to take the transcript and produce a video with the transcript
# on the screen, with the and have a picture of the speaker fill the screen



import whisperx
import gc
import json
from moviepy.editor import ImageClip, TextClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip

from settings import *

device = "cpu" 
audio_file = "/Users/rudolfkischer/Projects/PodcastGPT/static/audio/JoeRoganBenShapiro.mp3"
access_token = '<hf access token>'
batch_size = 16 # reduce if low on GPU mem
compute_type = "float32" # change to "int8" if low on GPU mem (may reduce accuracy)

def get_word_level_transcript(audio_file_path):
    model = whisperx.load_model("small", device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file_path)
    result = model.transcribe(audio, batch_size=batch_size)

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    # temporary output file for testing
    output_file = "/Users/rudolfkischer/Projects/PodcastGPT/static/audio/JoeRoganBenShapiroTEST.json"
    with open(output_file, 'w') as outfile:
        json.dump(result, outfile)

    diarize_model = whisperx.DiarizationPipeline(use_auth_token=access_token, device=device)
    diarize_segments = diarize_model(audio)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    print(diarize_segments)
    print(result["segments"])

    diarized_output_file = "/Users/rudolfkischer/Projects/PodcastGPT/static/audio/JoeRoganBenShapiroDIARIZED.json"
    with open(diarized_output_file, 'w') as outfile:
        json.dump(result, outfile)
    

    return result

def create_freeze_frame(clip, end_time):
    """Create a freeze frame from the last frame of the clip, extended until end_time."""
    last_frame = clip.to_ImageClip(clip.duration)
    freeze_frame = last_frame.set_duration(end_time - clip.end)
    return freeze_frame


def create_clip(segment, host_image, guest_image, host_name, guest_name):
    # Choose image based on speaker
    # print(f'speaker: {segment["speaker"]}')
    # print(host_name)
    # image_file = host_image if segment['speaker'] == host_name else guest_image
    image_file = guest_image
    image_file = '/Users/rudolfkischer/Projects/PodcastGPT/static/profiles/ben_shapiro.jpg'
    if segment['speaker'] == host_name:
        image_file = host_image
    else:
        image_file = guest_image
    


    image_clip = ImageClip(image_file).set_duration(segment['end'] - segment['start'])
    text_clip = TextClip(f'{segment["speaker"]}:{segment["text"]}', fontsize=10, color='white').set_position('bottom').set_duration(segment['end'] - segment['start'])
    combined_clip = CompositeVideoClip([image_clip, text_clip]).set_start(segment['start'])

    return combined_clip


def smooth_clips(clips):
    extended_clips = []
    for i, clip in enumerate(clips):
        if clip.duration < 1:  # Skip short clips and extend the previous freeze frame
            if extended_clips:
                extended_clips[-1] = create_freeze_frame(extended_clips[-1], extended_clips[-1].duration + clip.duration)
            continue

        extended_clips.append(clip)
        if i < len(clips) - 1:
            next_clip_start = clips[i + 1].start
            freeze_frame_duration = next_clip_start - clip.end
            freeze_frame = create_freeze_frame(clip, freeze_frame_duration)
            extended_clips.append(freeze_frame)

    return extended_clips
    

def get_video_from_audio(audio_file_path, 
                         transcript_file_path,
                         guest_name, host_name):
    
    # diarized_transcript = get_word_level_transcript(audio_file_path)
    diarized_transcript = json.load(open(transcript_file_path))
    personality_profiles = { personality: f'{PROFILES_PATH}/{personality}.jpg' for personality in PERSONALITIES }
    guest_profile = personality_profiles[guest_name]
    host_profile = personality_profiles[host_name]

    # get the list of all speakers
    speakers = set([segment['speaker'] for segment in diarized_transcript['segments']])
    # map the host and guests to first two speakers, and the rest to the guest
    speakers = list(speakers)
    # reverse sort so that the host is first
    speakers.sort(reverse=True)
    print(speakers)
    speaker_to_name = { speakers[0]: host_name, speakers[1]: guest_name }
    for speaker in speakers[2:]:
        speaker_to_name[speaker] = guest_name

    # replace SPEAKER_02 and SPEAKER_01 with guest and host names
    for segment in diarized_transcript['segments']:
        segment['speaker'] = speaker_to_name[segment['speaker']]

    


    audio_clip = AudioFileClip(audio_file_path)
    background_image_path = host_profile
    background = ImageClip(background_image_path, duration=audio_clip.duration).set_position("center")

    clips = [create_clip(segment, host_profile, guest_profile, host_name, guest_name) for segment in diarized_transcript['segments']]

    clips = smooth_clips(clips)


    clips.insert(0, background)
    dimensions = clips[0].size
    final_clip = CompositeVideoClip(clips, size=(512,512)).set_duration(audio_clip.duration)
    final_clip = final_clip.set_audio(audio_clip)
    final_clip.write_videofile(f'{PODCASTS_PATH}/{guest_name}_{host_name}.mp4', fps=24)

def main():
    # result = get_word_level_transcript(audio_file)
    # print(result)
    diarized_transcript_path = "/Users/rudolfkischer/Projects/PodcastGPT/static/audio/JoeRoganBenShapiroDIARIZED.json"
    get_video_from_audio(audio_file, diarized_transcript_path, 'joe_rogan', 'ben_shapiro')

if __name__ == "__main__":
    main()


