import shutil
import datetime
import os


srv_upload_folder = '/Users/jinjie/staging/cfda2'
upload_folder = '/Users/jinjie/staging/cfda_bak'


today = datetime.date.today()
today = str(today).replace('-', '')


def copy_file():
    case_list = []
    for f in os.listdir(srv_upload_folder):
        if today in f and os.path.isdir(os.path.join(srv_upload_folder, f)):
            case_list.append(f)

    if len(case_list) == 0:
        return

    else:
        try:
            if len(case_list) == 1:
                srv_case_path = os.path.join(srv_upload_folder, case_list[0])
                cfda_case_path = os.path.join(upload_folder, case_list[0])
                shutil.copytree(srv_case_path, cfda_case_path)

            else:
                for x in range(2):
                    srv_case_path = os.path.join(srv_upload_folder, case_list[x])
                    cfda_case_path = os.path.join(upload_folder, case_list[x])
                    shutil.copytree(srv_case_path, cfda_case_path)
        except Exception as e:
            print(e)

    return True


if __name__ == '__main__':
    copy_file()




