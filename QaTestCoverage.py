# cretae  a dict with key:value the key is the function and the value is list of tests
import os
import json

def main():
    TESTS_FOLDER = "C:\\Users\\shepss\\PycharmProjects\\Hackaton2019"
    testsName = []

    for root, dir, files in os.walk(TESTS_FOLDER):
        for file in files:
            if file.endswith('.gcov'):
                testsName.append(os.path.join(root, file))

    # check if the file exist else create it
    if os.path.isfile("data.json"):
        with open('data.json') as json_file:
            funcDict = json.load(json_file)
    else:
        funcDict={}


    for inputFile in testsName:
        setData(inputFile,funcDict)
    print(funcDict)

    # dump the dict to json file
    with open('data.json', 'w') as outfile:
        json.dump(funcDict, outfile)


def setData(inputFile,funcDict):
    """
    this methos get the the file name and pars all of the data
    :param inputFile: the input file to pharse
    :param funcDict:  ths data struct to work with
    :return:
    """
    with open(inputFile) as f:
        data = f.readlines()
        for line in data:
            if "file" in line:
                testname = (line.split(":")[1].rstrip())
                print("testname is:{0}".format(testname))
            if "function" in line and "main" not in line:
                functionName = (line.split(":")[-1].split(",")[-1].rstrip())
                print("functionName is: {0}".format(functionName))
                funcDict[functionName] = [testname]






if __name__ == "__main__":
    main()
