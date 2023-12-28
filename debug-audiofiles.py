import glob, shutil, os

if __name__ == '__main__':
    # counter = 0

    speaker_paths = glob.glob("./data/p1/*/")
    # NEW_FILE_DIR_PATH = r"./data/p1"
    # for path in speaker_paths:
    #     audio_file_for_speaker = glob.glob(f"{path}/*")
    #     for audio_file in audio_file_for_speaker:
    #         print("audio_file_path = ", audio_file)
    #         ## file path example - ./data/p1\0001\000010001.WAV
    #         audio_filename = audio_file.split('\\')[-1]
    #         # print("filename = ", audio_filename)

    #         new_name = f"{NEW_FILE_DIR_PATH}/{audio_filename}"
    #         os.rename(audio_file, new_name)
    #         # counter += 1

    #         # if counter > 5 : break
    #     print(f"Processing for speaker {path} completed!")

        # if counter > 1: break
    for path in speaker_paths:
        shutil.rmtree(path)