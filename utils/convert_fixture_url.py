import argparse
import urllib.parse
import json

def convert_file(file: str, output_file: str, directory: str,
                 field_from: str, field_to: str) -> None:

    with open(file, "r") as f:
        fixture = json.load(f)

    if directory.endswith("/"):
        directory = directory[:-1]

    new_fixture = []
    for obj in fixture:
        # Skip if field is not available
        if field_from not in obj["fields"]:
            continue

        # Convert url to filepath
        url = obj["fields"][field_from]
        if url is None:
            obj["fields"][field_to] = None
        else:
            filename = url.split("/")[-1]
            filename = urllib.parse.unquote_plus(filename)

            obj["fields"][field_to] = f"{directory}/{filename}"

        # Remove old field
        if field_to != field_from:
            del obj["fields"][field_from]

        new_fixture.append(obj)

    with open(output_file, "w") as f:
        json.dump(new_fixture, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file', type=str,
                        required=True,
                        help='the path to the JSON file')
    parser.add_argument("-of", '--output_file', type=str,
                        required=True,
                        help='the name of the output JSON file')
    parser.add_argument("-dir", '--directory', type=str,
                        required=True,
                        help='directory in MEDIA_ROOT where the files are stored')
    parser.add_argument("-ff", '--field_from', type=str,
                        required=True,
                        help='the name of the field to change from')
    parser.add_argument("-ft", '--field_to', type=str,
                        required=True,
                        help='the name of the field to change to')
    args = parser.parse_args()

    file = args.file
    output_file = args.output_file
    directory = args.directory
    field_from = args.field_from
    field_to = args.field_to

    convert_file(file, output_file, directory, field_from, field_to)

