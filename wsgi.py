
from os import getenv
from webapp import create_app
from argparse import ArgumentParser


app = create_app(getenv('FLASK_CONFIG') or 'development')


def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", help="port number")
    args = parser.parse_args()
    port = int(args.port or 5000)
    app.run(port=port)

if __name__ == "__main__":
    main()
