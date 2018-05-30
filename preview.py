import sys
import yaml
from PIL import Image
from io import BytesIO
import base64

def main():
    if len(sys.argv) != 2:
        raise Exception("No testcase specified")

    testcase = sys.argv[1]
    stream = open('fixtures/vcr_cassettes/{}.yaml'.format(testcase), 'r')
    docs = yaml.load_all(stream)
    image = None
    for doc in docs:
        for key, value in doc.items():
            if key != 'interactions':
                continue
            request = value[0]
            image = request['response']['body']['string']
            break

    if image:
        preview = Image.open(BytesIO(image))
        preview.show()


if __name__ == "__main__":
    main()
