import json
import os

def setData(inputFile, funcDict, testName):
    """
    this methos get the the file name and pars all of the data
    :param inputFile: the input file to pharse
    :param funcDict:  ths data struct to work with
   :return:
    """
    with open(inputFile) as f:
        data = f.readlines()
        for line in data:
            if "function" in line and "main" not in line and not "file" in line:
                if line.split(",")[-2] != '0':
                    functionName = (line.split(":")[-1].split(",")[-1].rstrip())
                    print("functionName is: {0}".format(functionName))
                    #funcDict[testname].append(functionName)
                    if not functionName in funcDict.keys():
                        funcDict[functionName] = [testName]
                    else:
                        if not testName in funcDict[functionName]:
                            funcDict[functionName].append(testName)



def main():
    # phase 1 : create test list
    tests = []
    TESTS_FOLDER = "./tests_functions"
    os.chdir(TESTS_FOLDER)
    os.system("rm -f *.gc*")
    os.system("rm -f functions.c.gcov")
    os.system("rm -f functionTotes.json")
    # r=root, d=directories, f = files
    for r, d, f in os.walk("."):
        for file in f:
            if file.endswith('.c') and file != "functions.c":
                tests.append(os.path.join(r, file))

    # phase 2: if json file exists, load dict from file, otherwise - create a new dict
    gcovFiles = []
    for root, dir, files in os.walk("."):
        for file in files:
            if file.endswith('.gcov'):
                gcovFiles.append(os.path.join(root, file))

    if os.path.isfile('functionTotes.json'):
        with open('functionTotes.json') as json_file:
            funcDict = json.load(json_file)
    else:
        funcDict = {}



    # phase 3: for each file ron gcove
    cmds=[1, 2, 3]
    for file in tests:
        cmds[0] = "gcc -Wall -fprofile-arcs -ftest-coverage functions.c {0} -o {1}".format(file, os.path.splitext(file)[0]+ ".o")
        cmds[1] = "{0}".format(os.path.splitext(file)[0]+ ".o")
        cmds[2] =  "gcov  -i --function-summaries functions.c"
        for cmd in cmds:
            os.system(cmd)
        setData('functions.c.gcov', funcDict, os.path.splitext(file)[0].replace("./",""))
        print funcDict
        #os.system("rm -f functions.c.gcov")


    # for gcovFile in gcovFiles:
    #     setData(gcovFile,funcDict)

    print "funcDict\n"
    print funcDict
    # # dump the dict to json file
    with open('functionTotes.json', 'w') as outfile:
        json.dump(funcDict, outfile)

if __name__ == '__main__':
    main()