
# .WTF Format

The WORST format ever!


## .WTF File Structure

### JSON Data / Metadata
 - filename (String)
 - author (String)
 - version (Integer)
 - pack_ver (Integer)
 - hash (String)
 Example: {'filename': 'main.py', 'author': 'Testing', 'version': 1, 'pack_ver': 1, 'hash': 'AAAAAAAAAAAAA'}

### File Data

| WTF Bit 	| Regular Bit 	|
|---------	|-------------	|
| fuck    	| 0           	|
| fucked  	| 1           	|

convert_to_wtf function reads the file's bits and converts it according to the table above
## .WTFA File Structure


- .WTF file (saved as .WTFA)
  - ZIP Archive (no compression)
    - WTF file
      - Original File
    - WTF File
      - File 2

[archive_file()](https://github.com/proton0/wtf/blob/main/wtf.py#L190)
 does the following this in order to make the final .wfta archive file

- Gets all files in archive_target
- Runs [convert_to_wtf()](https://github.com/proton0/wtf/blob/main/wtf.py#L56)
- Makes the .ZIP archive with the .WTF files
- Runs [convert_to_wtf()](https://github.com/proton0/wtf/blob/main/wtf.py#L56) to the .ZIP file which results in the final archive (.WTFA)
## Usage/Examples

Convert demo.mov to demo.wtf and back to .mov

```python
import wtf

wtf.convert_to_wtf("demo.mov", "demo.wtf")

wtf.convert_wtf_to_file("demo.wtf", "demo.mov")
```

Read a .wtf file's metadata and set the author to Proton0

```python
import wtf

meta = wtf.Metadata("demo.wtf")

print(meta.get_metadata()) # Prints the entire metadata of the file

print(meta.get_value("author")) # Prints the 'author'

meta.edit("author", "Proton0") # Sets the author to Proton0

print(meta.get_value("author")) # Prints the new author
```

Create a archive called "archive.wfta" and then extract it as "extracted"

```python
import wtf

wtf.archive_files("archive_target", "archive.wtfa")

wtf.unarchive_files("archive.wtfa", "extracted")

```

## Running Tests

Create the following folders like this below

- tests
   - testdata
   - ziptest
then put your files in testdata or ziptest

Finally run main.py

```bash
  python3 main.py
```

