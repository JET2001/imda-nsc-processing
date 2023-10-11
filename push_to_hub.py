from datasets import load_dataset

if __name__ == '__main__':
    PATH_TO_DATA = r"./data"
    
    audio_dataset = load_dataset("audiofolder", data_dir = PATH_TO_DATA)
    print("dataset = ", audio_dataset)
    print("dataset['train'][0]", audio_dataset["train"][0])

    print("Pushing to hub...")
    # audio_dataset.push_to_hub("JET2001/imda-nsc-processed", private = True)


