import wtf

metadata = wtf.Metadata("tests/corrupted_data/file-no-metadata.txt")

metadata.edit("version", "3")

metadata.get_metadata()

metadata.get_value("version")
