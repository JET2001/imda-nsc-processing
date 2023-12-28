# imda-nsc-processing
Repository for processing National Speech Corpus by IMDA for Speech T5 Finetuning

## Implementation Details
The IMDA NSC has 6 parts, for the finetuning of Microsoft's Speech T5 model, to get this model,(https://github.com/JET2001/speech-t5-finetune-public), I only processed the data in Part 1, Channel 0 of the NSC.

### Part 1 Processing
The relevant parts of the directory structure for the IMDA Corpus is as such: 
```
PART1
    | - DATA
        | - CHANNEL0
            | - SCRIPT
                | > 000010.TXT (Transcript for Speaker 1, Session 0)
                | > 000011.TXT (Transcript for Speaker 1, Session 1)
                | > 000020.TXT (Transcript for Speaker 2, Session 0)
                | > 000021.TXT (Transcript for Speaker 2, Session 1)
                | > ...
            | - WAVE
                | - SPEAKER0001.zip
                    | - SPEAKER0001
                        | - SESSION0
                            | > 000010001.WAV 
                            | > 000010002.WAV
                            | > ... (about 400 of such files with prefix 000010???.WAV, that correspond to all the text in transcript for Speaker 1, Session 0)
                        | - SESSION1
                            | > 000011401.WAV
                            | > 000011402.WAV
                            | > ... (about 400 of such files with prefix 000011???.WAV, that correspond to all text in the transcript for Speaker 1, Session 1)
                | - SPEAKER0002.zip
                    ...
        | - CHANNEL1
            # Not used
        | - CHANNEL2
            # Not used
```
General Contents of transcript file `PART1/DATA/CHANNEL0/SCRIPT/000029.TXT`:
```
000029301	The Quick Brown Fox jumps, over the lazy dog.
	the quick brown fox jumps over the lazy dog
000029302<TAB><PUNCTUATED VERSION><NEWLINE>
<TAB><lowercased version with no punctuation>
```
(Note: Not the actual sentence)

These correspond to Speaker 1 audio files `*301.WAV` and `*302.WAV` respectively.

As of 9 Dec 2023, I am using the **lowercased version with no punctuation** to build the model.

### Data Processing Pipeline
I am using Hugging Face hub's [AudioFolder](https://huggingface.co/docs/datasets/audio_dataset#audiofolder).

Target output of data processing:
```
data
    | - p1
        | > 000010001.WAV
        | > 000010002.WAV
        | ... 
        | > 000029301.WAV
        | ...
        (this folder size would be around 800 recordings per speaker x num_speakers)
        | > metadata.csv
```
`data/p1/metadata.csv` will then have the following file format:
```
filename,transcription,speaker
...
000029301.WAV,the quick brown fox jumps over the lazy dog,0029
...
```
The length of `metadata.csv` must be equal to the number of audio files `data/p1`.

**Note:** In the IMDA NSC Corpus, there were some missing audio files with an existing transcription, as well as some missing transcriptions for existing audio files. (Haiz...)


### Overview of the data processing functions

In `process_part1.py`,
- `create_wavs_and_transcript(start_idx = 0)` - starts processing the transcript of speaker `start_idx` (I use this in case of errors, so I don't need to reparse all processed speakers again)
- `create_wavs_for_speaker(...)` - this creates wavs for speaker in the target folder at the specified `OUT_PATH`.
- `create_transcript_for_speaker(...)` - this is called AFTER `create_wavs_for_speaker` has run for that speaker. We retrieve only the transcripts for the audio files present. 
    - This allows us audio does not exist, we drop the transcription. 
    - If audio exists, but transcription does not, we drop that audio. (Got enough audio for finetuning) (see line 109) 

`main.py` then contains the call to the `process_part1.create_wavs_and_transcript(start_idx)`

After the `data` has been created successfully, run `push_to_hub.py`


#### Running Time
I processed about 338000 audio clips, or about 400 speakers worth of data over night. 
`push_to_hub` took about 3 hours to complete with these 338000 audio clips. It uploads them as a [parquet shard](https://huggingface.co/docs/datasets-server/parquet), each parquet shard contains about 50 or so speakers. 

