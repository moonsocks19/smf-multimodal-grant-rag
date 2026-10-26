# knowledge_base/03_audio/audio/

## If the .mp3 files here are 0 bytes, they are placeholders

The audio is **generated from the scripts in `../scripts/`**, not shipped as
recordings. Generating rather than recording keeps the corpus reproducible for
whoever marks the project, keeps the transcripts in sync with the audio by
construction, and avoids handling anyone's voice data.

Generation needs network access to Google's text-to-speech endpoint. The build
sandbox used to assemble this folder has no route to it (nor to any other TTS
provider), so the files were left as 0-byte placeholders.

## Fixing it — one command, from any machine with internet

```bash
python tools/make_audio.py --kb knowledge_base/03_audio
```

`gTTS.save()` truncates and rewrites, so the placeholders are replaced in place;
nothing needs deleting. Each file is then validated with `ffprobe`, and anything
that is not actually decodable is reported rather than silently accepted.

Expect roughly 800 KB – 1.1 MB per clip, 45–75 seconds each.

## Or just run notebook 1

`notebooks/01_Build_and_Evaluate.ipynb` §3.3 does the same thing automatically:
it regenerates any file that ffprobe cannot read a duration from, prints the
duration of each one it accepts, and lists any it rejected. A previous Colab run
of this pipeline produced all four clips successfully (812 KB, 903 KB, 1084 KB,
961 KB) and Whisper transcribed all four.

## If you have no network at all

The pipeline still works. It falls back to `../reference_transcripts/`, and
records `audio_provenance: reference_transcript` per clip in
`artifacts/config.json` — so the report can state that the audio modality was
present as text only, rather than implying a working ASR path.
