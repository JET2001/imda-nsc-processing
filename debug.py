import glob

if __name__ == '__main__':
    audio_folder_structure = glob.glob("./data/**", recursive=True)
    audio_path_list = []
    metadata_path = []
    with open("./metadata.csv", "r") as f:
        scriptlines = f.readlines()
        for f in scriptlines[1:]:
            filepath = f.split(",")[0].split("/")[-1]
            metadata_path.append(filepath)

    for audio_path in audio_folder_structure:
        if '.WAV' not in audio_path: continue
        audio_file_name = audio_path.split('\\')[-1]
        audio_path_list.append(audio_file_name)

    print("metadata_path = ", metadata_path[:5])
    print("audio_path_list = ", audio_path_list[:5])

    audio_path_set = set(audio_path_list)
    metadata_path_set = set(metadata_path)

    print("items in metadata but not in audio ", metadata_path_set.difference(audio_path_set))

    print("items in audio but not in metadata", audio_path_set.difference(metadata_path_set))
    
