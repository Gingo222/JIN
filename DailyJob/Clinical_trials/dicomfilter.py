import os
import csv
import pydicom


file_paths = []


def take_off_tag(path, file_path, Patient_ID):
        dicom_path = os.path.join(path, file_path)
        print(dicom_path)
        dcms = os.listdir(dicom_path)
        for dcm in dcms:
            if dcm.endswith('.dcm'):
                dicoms = os.path.join(dicom_path, dcm)
                try:
                    ds = pydicom.dcmread(dicoms)
                    ds.PatientName = 'Unknown'
                    ds.PatientID = Patient_ID
                    ds.save_as(dicoms)
                    print('success change {}'.format(dicoms))
                except Exception as e:
                    print(e)


def getFilePath(path, file_paths):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if file_name.endswith('DS_Store'):
            pass
        elif os.path.isdir(file_path):
            getFilePath(file_path, file_paths)
        elif os.path.isfile(file_path) and 'slices' in file_path and file_path.endswith('dcm') and os.path.dirname(file_path) not in file_paths:
            file_paths.append(os.path.dirname(file_path))


def readcsv(file_path, csv_path):
    csv_file = csv.reader((open(csv_path, 'r')))
    for stu in csv_file:
        take_off_tag(file_path, stu[0], stu[2])


if __name__ == '__main__':
    path = '/Users/jinjie/staging/original'
    csv_path = '/Users/jinjie/staging/tester/1.csv'
    readcsv(file_path=path, csv_path=csv_path)
