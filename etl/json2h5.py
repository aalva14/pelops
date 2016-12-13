'''transform the json files into h5py files

Input:
    one json encoded dict / line
    dict should have the following keys:
        colorID     - colorID of the vehicle
        vehicleID   - vehicle ID
        resnet50    - feature vector of the vehicle
        imageName   - name of the file in storage
        typeID      - ??
        cameraID    - which camera took the image

Output:
    h5py file with the following datasets
        colorID     - int colorID of the vehicle
        vehicleID   - int vehicle ID
        resnet50    - [float] feature vector of the vehicle
        imageName   - str name of the file in storage
        typeID      - int ??
        cameraID    - which camera took the image

Usage:
    json2h5.py [-hv]
    json2h5.py -i <INFILE> -o <OUTFILE>

Arguments:
    INFILE - json infile name
    OUTFILE - h5py outfile name

Options:
    -h, --help      :show this message
    -v, --version   :Version of the program
    -i, --input     :input file for the program
    -o, --output    :output file for the program

'''
import docopt
import h5py
import json
import numpy as np
import sys


def makeJsonList(fileName):
    retval = list()
    with open(fileName, 'r') as f:
        for line in f:
            line = line.strip()
            line = json.loads(line)
            retval.append(line)
    return retval


def extractColumn(colName, jsonList, t):
    retval = list()
    for line in jsonList:
        if t == str:
            retval.append(str(line[colName]).encode('ascii', 'ignore'))
        if t == int:
            retval.append(int(line[colName]))
        if t == float:
            for element in line[colName]:
                retval.append(float(element))
    return retval


def make5file(file5Name, names, jsonList):
    with h5py.File(file5Name, 'w') as f:
        for o, i, t, t2 in names:
            temp = extractColumn(o, jsonList, t)
            f.create_dataset(i, data=temp, dtype=t2)


def main(args):
    try:
        inFileName = args['--input']
        outFileName = args['--output']
    except docopt.DocoptExit as e:
        sys.exit('error: input invalid options: {0}'.format(e))

    jsonList = makeJsonList(inFileName)
    f = np.dtype('float')
    c = h5py.special_dtype(vlen=bytes)
    names = [('colorID', 'colorID', int, int),
             ('vehicleID', 'vehicleID', int, int),
             ('resnet50', 'feats', float, f),
             ('imageName', 'ids', str, c),
             ('typeID', 'typeID', int, int),
             ('cameraID', 'cameraID', str, c)]
    make5file(outFileName, names, jsonList)

if __name__ == '__main__':
    args = docopt.docopt(__doc__, version='json2h5.py 1.0')
    main(args)
    main(sys.argv[1], sys.argv[2])
