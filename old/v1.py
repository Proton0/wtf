"""

.WTF Archive Format
Made by Proton0

The most un-optimized archive ever (4743.44% file size increase while testing)

.WTF file structure and how to read

Line 1 : JSON data / Metadata
    -> filename | String
    -> author  | String
    -> version | Integer
    -> pack_ver| Integer
    example: {'filename': 'main.py', 'author': 'Testing', version: 1, pack_ver: 1}

The rest is file data

fuck = 1
fucked = 0

"""

package_version = 1

import json
import os
import logging

logging.basicConfig(level=logging.DEBUG)


def byte_to_binary(byte):
    return format(byte, "08b")


def convert_to_wtf(
    file, wtf_file, filename=None, author=None, version=1, pack_ver=package_version
):
    # Convert file data and stuff
    if filename is None:
        logging.debug("filename set to file")
        filename = file
        filename = os.path.basename(filename) # get only the filename
    if not wtf_file.endswith(".wtf"):
        wtf_file = wtf_file + ".wtf"
    if author is None:
        author = ""
    logging.debug("create file metadata")

    file_data = {  # Make JSON
        "filename": filename,
        "author": author,
        "version": version,
        "pack_ver": pack_ver,
    }

    if os.path.exists(wtf_file):  # check if file exists and stuff
        logging.debug("deleted old file")
        os.remove(wtf_file)
    if not os.path.exists(file):
        raise Exception("The file does not exist")
    logging.debug("open wtf file")
    wtf = open(wtf_file, "w")
    logging.debug("write metadata")
    wtf.write(json.dumps(file_data) + "\n")

    # Convert the file to the .WTF format
    with open(file, "rb") as main_file:
        byte = main_file.read(1)
        while byte:
            logging.debug("converted byte: " + str(byte))
            # Convert the byte to its binary representation
            binary_str = byte_to_binary(byte[0])
            # Loop through each bit in the binary representation
            for bit in binary_str:
                # Check if the bit is '1' or '0'
                if bit == "0":
                    wtf.write("fuck ")
                elif bit == "1":
                    wtf.write("fucked ")
                else:
                    raise ValueError("Invalid bit value. Data may be corrupt or read error")
            # Read the next byte
            byte = main_file.read(1)


def get_wtf_metadata(file):
    f = open(file, "r")
    return json.loads(f.readline())


def convert_wtf_to_file(wtf_file, main_file):
    if not os.path.exists(wtf_file):
        raise Exception("The WTF file does not exist")
    if os.path.exists(main_file):
        os.remove(main_file)

    # convert to main_file
    f = open(wtf_file, "r")
    lines = f.readlines()
    if len(lines) == 0:
        raise Exception("No data found in file")
    metadata = lines[0]

    # Support for no metadata or corrupted data
    if len(lines) == 1:
        if lines[0].startswith("{"):
            raise Exception("Metadata found but no file data")
        else:
            metadata = f"{'filename': '', 'author': '', version: 0, pack_ver: 0}"
            logging.warning(
                "No metadata found. The version might be incorrect (a another warning will popup soon)"
            )

    data = lines[1]  # the actual data
    metadata = json.loads(metadata)  # turn it to JSON

    # Check package version
    if metadata["pack_ver"] != package_version:
        logging.critical(
            f"The WTF file version is not the same as this converter version! (file: {metadata['pack_ver']}, converter version: {package_version})"
        )
    if metadata["pack_ver"] < package_version:
        raise ValueError(
            "Please upgrade the converter. The file is newer then what the converter supports"
        )
    else:
        if metadata["pack_ver"] == package_version:
            pass
        else:
            logging.warning(
                "It is recommended to downgrade the converter because the file is older then what the converter supports which can cause issues"
            )

    # Convert the file
    binary_data = ""
    for word in data.split():
        if word == "fuck":
            binary_data += "0"
        elif word == "fucked":
            binary_data += "1"
        else:
            logging.critical(f"Invalid data found: {word}")
            raise ValueError(f"Invalid data found:", word)

    # Convert the 1 and 0 to the file
    with open(main_file, "wb") as ze:
        ze.write(
            bytes(
                [int(binary_data[i : i + 8], 2) for i in range(0, len(binary_data), 8)]
            )
        )
    logging.info("converted succesfully")