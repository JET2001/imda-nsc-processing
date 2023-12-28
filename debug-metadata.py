import glob, shutil

if __name__ == '__main__':
    with open("metadata-copy.csv", "r") as inputFile:
        with open("./data/p1/metadata.csv", "w") as outputFile:
            header = inputFile.readline().rstrip()
            updated_header = f"{header},speaker\n"
            outputFile.write(updated_header)
            
            while True:
                audio_file_line = inputFile.readline().rstrip()

                if (audio_file_line == ""): break ## end of file
                
                if ('.WAV' not in audio_file_line): continue

                audio_file_path, script = audio_file_line.split(',')
                folder, subfolder, speaker, filename = audio_file_path.split('/')
                ## Construct the updated path
                updated_path = f"{filename},{script},{speaker}\n"
                outputFile.write(updated_path)
