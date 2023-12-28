import process_part1
import os, glob, shutil



if __name__ == "__main__":
    ## Data folder creation
    # try:
    #     os.mkdir("data")
    # except OSError:
    #     print("Folder 'data' exists. Removing contents of data")
    #     shutil.rmtree("data")

    ## Metadata.csv creation
    # f = open("metadata.csv", "w")
    # f.close()

    process_part1.create_wavs_and_transcript(99)