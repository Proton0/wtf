import wtf
import os
import shutil

if os.path.exists("tests/converted_wtf"):
    shutil.rmtree("tests/converted_wtf")

if os.path.exists("tests/converted_back"):
    shutil.rmtree("tests/converted_back")

if os.path.exists("tests/unarchived"):
    shutil.rmtree("tests/unarchived")

os.mkdir("tests/converted_wtf")
os.mkdir("tests/converted_back")
os.mkdir("tests/unarchived")

print("Converting the data")

k = os.listdir("tests/testdata")

for z in k:
    wtf.convert_to_wtf(f"tests/testdata/{z}", f"tests/converted_wtf/{z}")

print("Converting the data back")

k = os.listdir("tests/converted_wtf")

for z in k:
    wtf.convert_wtf_to_file(f"tests/converted_wtf/{z}", f"tests/converted_back/{z}")

print("Testing archive function")
print("creating")

wtf.archive_files("tests/ziptest", "wtfarchive.wtfa")

print("unarchiving")

wtf.unarchive_files("wtfarchive.wtfa", "tests/unarchived")

print("Testing metadata function")
k = os.listdir("tests/converted_wtf")

for z in k:
    print("creating metadata object")
    meta = wtf.Metadata(f"tests/converted_wtf/{z}")
    print("get_metadata")
    print(meta.get_metadata())
    print("get version")
    print(meta.get_value("version"))
    print("set version")
    meta.edit("version", 3)
    print(meta.get_value("version"))
print("All tests complete")