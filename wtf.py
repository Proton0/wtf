"""

.WTF Format version 1.4
Made by Proton0

Documentation moved to the README.md file (https://github.com/proton0/wtf)
"""

import shutil
import datetime
import zipfile
import json
import os
import logging
import hashlib
import random

package_version = 3  # do not change unless an edit in how data (or metadata) works

level = logging.DEBUG

logging.basicConfig(
    level=level, format="[%(asctime)s] [%(funcName)s] [%(levelname)s] %(message)s"
)


def byte_to_binary(byte):
    return format(byte, "08b")


def convert_to_wtf(
    file,
    wtf_file,
    filename=None,
    author=None,
    version=1,
    pack_ver=package_version,
    noExtenstion=False,
    description="",
    license="",
    created_unix = None
):
    # Convert file data and stuff
    if filename is None:
        logging.debug("filename set to file")
        filename = file
        filename = os.path.basename(filename)  # get only the filename
    if not noExtenstion:
        if not wtf_file.endswith(".wtf"):
            wtf_file = wtf_file + ".wtf"
    if author is None:
        author = ""
    if created_unix is None:
        created_unix = int(datetime.datetime.now().timestamp())
    logging.debug("create file metadata")

    file_data = {  # Make JSON
        "filename": filename,
        "author": author,
        "version": version,
        "pack_ver": pack_ver,
        "hash": hashlib.md5(open(file, "rb").read()).hexdigest(),
        "description": description,
        "license": license,
        "created_unix": created_unix
    }

    if os.path.exists(wtf_file):  # check if file exists and stuff
        logging.debug("deleted old file")
        os.remove(wtf_file)

    if not os.path.exists(file):
        raise FileNotFoundError("The file does not exist")
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
                    raise ValueError(
                        "Invalid bit value. Data may be corrupt or read error"
                    )
            # Read the next byte
            byte = main_file.read(1)


def convert_wtf_to_file(wtf_file, main_file, ignoreHashInvalid=False):
    if not os.path.exists(wtf_file):
        raise FileNotFoundError("The WTF file does not exist")
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
            logging.warning("No metadata found. Package version will be set to 0")

    data = lines[1]  # the actual data
    metadata = json.loads(metadata)  # turn it to JSON

    # Check package version
    if metadata["pack_ver"] != package_version:
        logging.critical(
            f"The WTF file version is not the same as this converter version! (file: {metadata['pack_ver']}, converter version: {package_version})"
        )
    if metadata["pack_ver"] > package_version:
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

            # Make old files and archives skip the hash check because most likely they dont have the hash in the metadata
            if metadata["pack_ver"] > 2 or metadata["pack_ver"] == 2:
                logging.info("Not ignoring hash because according the package version it supports it")
            else:
                ignoreHashInvalid = True

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
    hash = hashlib.md5(open(main_file, "rb").read()).hexdigest()
    if metadata["hash"] != hash:
        if not ignoreHashInvalid:
            logging.warning(f"Hash is invalid! {metadata['hash']} changed to {hash}")
            raise ValueError(
                "Hash changed. To ignore this then set ignoreHashInvalid to True"
            )
    logging.info("converted succesfully")


def archive_files(archive_target, archive_file):
    if not os.path.exists(archive_target):
        raise FileNotFoundError("Archive target does not exist!")
    k = str(random.randint(1, 2000))
    os.mkdir(str(k))
    for files in os.listdir(archive_target):
        file = f"{k}/{files}"
        logging.info(f"archive {file}")
        convert_to_wtf(f"{archive_target}/{files}", file)
    logging.info("converted all files in target")
    logging.info("creating the zip")
    shutil.make_archive(archive_file, "zip", k)
    logging.info("deleting the old folder")
    shutil.rmtree(k)  # remove temp
    fe = archive_file
    logging.info("converting zip to wtf")
    convert_to_wtf(f"{archive_file}.zip", f"{fe}", noExtenstion=True)
    logging.info("deleting old .zip file")
    os.remove(f"{archive_file}.zip")
    logging.info("archive success")


def unarchive_files(archive_file, unarchive):
    if not os.path.exists(unarchive):
        logging.warning("Destination folder does not exist. Creating it now")
        os.mkdir(unarchive)
    logging.info("convert wtf to zip")
    convert_wtf_to_file(archive_file, "temp.zip")
    with zipfile.ZipFile("temp.zip", "r") as zip_ref:
        zip_ref.extractall("temp-data")
    logging.info("Extracted data from zip")
    for file in os.listdir("temp-data"):
        jf = file
        logging.debug("processing file: {}".format(jf))
        if file.endswith(".wtf"):
            logging.info(f"file {jf} ends with .wtf cutting it")
            jf = jf.split(".wtf")[0]
        convert_wtf_to_file(f"temp-data/{file}", f"{unarchive}/{jf}")
    logging.info("deleting old data")
    shutil.rmtree("temp-data")
    os.remove(f"temp.zip")
    logging.info("unarchived successfully")


class Metadata:
    disableChecking = False  # Should always be true

    def __init__(self, file):
        if not os.path.exists(file):
            raise FileNotFoundError("File does not exist")
        # just incase because sometimes idk
        k = open(file, "r").readlines()
        if len(k) > 2 or len(k) == 0 or len(k) < 0:
            logging.warning(f"{file} did not pass checks")
            raise self.MetadataException("Data might be corrupted")
        if k[0].startswith("{"):
            logging.info(f"{file} has passed the checks")
            self.file = file
        else:
            logging.warning("No metadata found!")
            raise self.MetadataException("No metadata was found in the file!")

    def CheckFile(self, file=None):
        if file is None:
            file = self.file
        if self.disableChecking:
            return
        else:
            file2 = file
            file = open(file, "r")
            file.seek(0)
            k = file.readlines()
            if len(k) > 2 or len(k) == 0 or len(k) < 0:
                raise self.MetadataException("Data might be corrupted")
            if not k[0].startswith("{"):
                raise self.MetadataException("No metadata was found in the file")
            file.seek(0)
            logging.info(f"{file2} has passed the check`")
            return True

    class MetadataException(Exception):
        def __init__(self, message=None):
            if message is None:
                message = "Unknown error"
            self.message = message
            super().__init__(message)

    def edit(self, metadata, new_value):
        f = open(self.file, "r")
        data = f.readlines()
        f.close()
        f = open(self.file, "w")
        f.seek(0)
        self.CheckFile()
        f.seek(0)
        j = json.loads(data[0])
        j[metadata] = new_value
        j = json.dumps(j)
        f.write(j + "\n")
        f.write(data[1])
        f.close()

    def get_metadata(self):
        f = open(self.file, "r")
        z = f.readlines()[0]
        f.seek(0)
        self.CheckFile()
        f.seek(0)
        return json.loads(z)

    def get_value(self, metadata):
        f = open(self.file, "r")
        f.seek(0)
        self.CheckFile()
        f.seek(0)
        k = json.loads(f.readlines()[0])
        f.close()
        return k[metadata]
