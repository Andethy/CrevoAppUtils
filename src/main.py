from sys import argv
from manipulator_json import main as json
from manipulator_xlsx import main as xlsx



if __name__ == '__main__' and len(argv) >= 1:
    if argv[1] == 'json':
        json.execute()
    elif argv[1] == 'xlsx':
        xlsx.execute()
