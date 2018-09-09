# Audio Sample Tools
## Project planning

Deliverables:
### Convert all files to 16 bit audio bit depth

### Catalog audio files
Each file should have:
1. Unique identifier
    - Iterate through all records increasing by 1
    - Starting at 1
    - How to prepend 0s?
2. Original unique title ("noflex" etc.)
2. Sound category
    - Either from the subfolder name
    - Or from first segment of original name
3. Qualifier (BPM, wet/dry, key)
    - BPM:

        - `##`
        - `##BPM`
        - `##.#`
        - `##.#BPM`
        - `###`
        - `###BPM`
        - `###.#`
        - `###.#BPM`

    - Wet / Dry
        - `Wet`
        - `Dry`

    - Key
        - `A`
        - `A|B|C|D|E|F|G`
        - `Amaj`
        - `G#min`
        - `C2`
4. Original filename
5. Original drum sample set
6. Original drum sample set subfolder
6. Size (kB)
7. Length (seconds)
8. Length (beats)
9. Bit depth
10. Sample rate
9. Comments
12. Whether one-shot or loop
    - Look for presence of BPM for loops

### Rename audio files
Use audio file catalog to rename all files using 16 characters or less:

`#####-CCC-Q-BPM.wav`

2. `#` unique ID
3. `C` category
4. `Q` qualifier
5. `BPM` beats per minute
    - what about decimals?
    - what about case w/ BPM and key?

eg.
- `01425-BAS-F.wav`
- `13259-CYM-234.wav`




##Steps
1. Iterate through samples and make list of dicts. Fields:
    - `sample_id`
        - `enumerate(iterable, nstart=1)`
    - `filename`
        - `file`
    - `kit`
       - `dirpaths.split('\')[0]`
    - `subfolder`
        - `dirpaths.split('\')[0]`
    - `category`
        - `file.split('_')[0]`
    - `name`
        - `file.split('_')[1]`
    - `effect`
        - `if 'wet' or 'Wet' in file[2:]:`
        - `if 'dry' or 'Dry' in file[2:]:`
    - `filter`
        - `if 'filter' or 'Filter' or 'FX' or 'Delay' in file[2:]:`
    - `bpm`
        - `if 'BPM' in file:`
            -   `regex() ###, ##, ###.#, ##.# in file`
            - `except if regex match is 808`
    - `key`
        - `if '808' in file:`
            - `regex single letter maybe number`
        - `regex() [A|B|C|D|E|F|G], maybe #, maybe [min|maj], maybe [1-9] `
    - `stereo`
        - `if 'L' or 'R' in file[2:]`

