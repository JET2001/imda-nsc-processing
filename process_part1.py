from zipfile import ZipFile
import glob
import os, shutil
import librosa
import soundfile as sf
from collections import defaultdict
import string

## Generate wav files and filelists from the IMDA dataset. Variables for PART 1.
DATASET_PATH = r"C:\Users\teoju\Dropbox\IMDA - National Speech Corpus"
OUT_PATH = r"data/p1"

## PART 1 Global Variables
AUDIO_PATH = r"PART1/DATA"
CHANNEL_NUM = r"CHANNEL0"
WAV_PATH = "WAVE"


SCRIPT_DIR_PATH = "SCRIPT"

AUDIO_SAMPLE_RATE = 16000

def create_wavs_and_transcript(start_idx = 0) -> None:
    # try:
    #     os.makedirs("data/p1")
    # except OSError:
    #     shutil.rmtree("data/p1")

    ALL_SPEAKERS_DIR = f"{DATASET_PATH}/{AUDIO_PATH}/{CHANNEL_NUM}/{WAV_PATH}"

    ALL_SCRIPTS_DIR = f"{DATASET_PATH}/{AUDIO_PATH}/{CHANNEL_NUM}/{SCRIPT_DIR_PATH}"

    all_speakers_zipfile_paths =  glob.glob(f"{ALL_SPEAKERS_DIR}/*")

    all_script_textfile_paths = glob.glob(f"{ALL_SCRIPTS_DIR}/*")
    ## Get a speakerNum-->script mapping
    ## one speaker has one to many script files.
    speaker2ScriptsMap = get_speaker_to_script_mapping(all_script_textfile_paths)

    for zipfile_path in all_speakers_zipfile_paths[start_idx:]:

        ## Prepare speaker
        speaker_num_str = zipfile_path.split("SPEAKER")[1].split('.zip')[0]
        print("speaker_num_str = ", speaker_num_str)
        
        out_path_for_speaker = f"data/p1/{speaker_num_str}"
        os.makedirs(out_path_for_speaker)
        create_wavs_for_speaker(zipfile_path, out_path_for_speaker, speaker_num_str)

        create_transcript_for_speaker(speaker2ScriptsMap[int(speaker_num_str)], out_path_for_speaker)


def create_wavs_for_speaker(path_to_speaker: str, out_path: str, speaker_num: str) -> None:
    # remove all files if we are regenrating the folder.
    with ZipFile(path_to_speaker, 'r') as zObject:
        for item in zObject.filelist:
            if '.WAV' in item.filename:
                zObject.extract(item.filename, path = out_path)
        ## Move all the files.
        wavs_in_subfolders = glob.glob(f"{out_path}/**", recursive=True)
        for wav_file in wavs_in_subfolders:
            if '.WAV' in wav_file:
                new_name = out_path + "\\"  + wav_file.split('\\')[-1]
                os.rename(wav_file, new_name) ## move file
                resample_audio(new_name)

        ## In the above process a SPEAKER000X folder will be created. Remove this folder beofre closing the file.
        shutil.rmtree(f"data/p1/{speaker_num}/SPEAKER{speaker_num}")

        zObject.close()

    print("wavs for speaker generated!")


def create_transcript_for_speaker(paths_to_speaker: list[str], proc_audio_path: str)->None:

    out_wav_path_contents = glob.glob(f"{proc_audio_path}/**")

    ## Create a temp file combining all the files in the paths to speakers
    audioToScriptMap = dict()
    for path in paths_to_speaker:
        with open(path, "r") as script:
            while True:
                # p
                script_components = script.readline().split('\t')

                if script_components == [""]:
                    break ## end of file

                script_without_punctuation = script.readline().strip()
                audio_file_key = "".join(filter(lambda x: x in string.printable, script_components[0]))
                audioToScriptMap[audio_file_key] = {'with_punc': script_components[1], 'no_punc':script_without_punctuation}
    
    print("length of map = ", len(audioToScriptMap))
    print("map key =", list(audioToScriptMap.keys())[0])
    print("first item = ", audioToScriptMap[list(audioToScriptMap.keys())[0]])        

    # print("OUT_WAV_PATH_CONTENTS = ", OUT_WAV_PATH_CONTENTS[:10])
    with open("metadata.csv", "a") as outFile:
        for filepath in out_wav_path_contents:
                    
            audio_file_key = filepath.split('\\')[-1].split('.WAV')[0]

            try:
                script = audioToScriptMap[audio_file_key]["no_punc"]
                # Write to out file
                outFile.write(f"{proc_audio_path}/{audio_file_key}.WAV,{script}")
                outFile.write("\n")
            except KeyError:
                print(f"Unable to find transcription for {filepath}, removing file")
                os.unlink(filepath)

    print("Generation of transcript completed!")

def empty_folder(path: str):
    for root, dir, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dir:
            shutil.rmtree(os.path.join(root, d))
    print(f"{path} folder emptied!") 


def resample_audio(path_to_sound_file: str)->None:
    resampled_audio , _ = librosa.load(path_to_sound_file, sr = AUDIO_SAMPLE_RATE)
    sf.write(path_to_sound_file, resampled_audio, samplerate = AUDIO_SAMPLE_RATE)

## Files are named 000010.TXT and 000011.TXT for speaker 1, as the sentences were recorded in two sessions - sessions 0 and 1. 
## speaker fragment would be the substring that corresponds to the speaker number. 
## We store an integer speaker number in the speakerScripts dictionary for our processing.
def get_speaker_to_script_mapping(all_scripts_textfile_paths: list[str]) -> dict:
    speakerScripts = defaultdict(list) 
    for textfile_path in all_scripts_textfile_paths:
        speaker_fragment = textfile_path.split("\\")[-1].split(".TXT")[0]
        speaker_fragment = speaker_fragment[:len(speaker_fragment)-1]
        
        # print("speaker_fragment = ", speaker_fragment)
        
        speakerScripts[int(speaker_fragment)].append(textfile_path)

    # print("speakerscripts = ", len(speakerScripts))
    # print("1st speaker = ", speakerScripts[1])
    print("speaker_to_scripts_map_created: numkeys =", len(speakerScripts))
    return speakerScripts