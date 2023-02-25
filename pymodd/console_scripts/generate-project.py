from argparse import ArgumentParser
import pymodd_generator


parser = ArgumentParser(
    description='Parse a modd.io json file into a pymodd project')
parser.add_argument('json_file_path', help='the path of the modd.io json file')


def main():
    json_file_path = parser.parse_args().json_file_path
    pymodd_generator.generate_project_from_json_file_path(json_file_path)


if __name__ == '__main__':
    main()
