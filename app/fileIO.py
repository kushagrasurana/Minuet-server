import json, os.path


def create_json_file(name, path, data):
    """Creates a json file on server
    :param name: File name
    :param path: Path where the file needs to be stored
    :param data: The data new json file will have
    """
    file=os.path.join(path, str(name) + '.json')
    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


def read_json_file(name, path):
    """Reads a json file on server
    :param name: File name
    :param path: Path where the file is stored
    :return: Returns json data from the file
    """
    file=os.path.join(path, str(name) + '.json')
    with open(file, 'r') as infile:
        return json.load(infile)


def remove_file(name, path):
    """Deletes a file on server
    :param name: File name
    :param path: Path where the file is stored
    """
    file=os.path.join(path, str(name) + '.json')
    if os.path.exists(file):
        os.remove(file)