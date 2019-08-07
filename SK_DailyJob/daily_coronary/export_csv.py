import os
import datetime
import sys
import inject


def get():
    """
    科研数据导出
    时间区间内没有数据时生成空文件
    """
    today = datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d")
    start = sys.argv.get("start") or today
    end = sys.argv.get("end") or today

    session = inject.instance(MainDBSession)
    with CommitContext(session):
        cases = session.query(Case).filter(Case.upload_time <= end).filter(Case.upload_time >= start).all()
        case_nums = {case.case_num for case in cases}

    case_dirs = [
        os.path.join(DATA_INSTANCE_FOLDER, name)
        for name in os.listdir(DATA_INSTANCE_FOLDER)
        if os.path.isdir(os.path.join(DATA_INSTANCE_FOLDER, name)) and name in case_nums
    ]
    zfile_name = os.path.join(DATA_INSTANCE_FOLDER, 'export_research.zip')
    csv_files_name = []
    for path in case_dirs:
        csv_path = os.path.join(path, 'narrow_list')
        csv_files_name.extend(
            [
                os.path.join(csv_path, name)
                for name in os.listdir(csv_path)
                if os.path.isfile(os.path.join(csv_path, name)) and name.endswith(".csv")
            ]
        )

    if csv_files_name:
        try:
            with zipfile.ZipFile(zfile_name, "w") as zfile:
                for name in csv_files_name:
                    name_lst = name.split('/')
                    case_num, file_name = name_lst[-3], name_lst[-1]
                    zfile.write(name, f'{case_num}/{file_name}')
        except Exception as e:
            logger.error(e, exc_info=1)
    else:
        logger.error('all dirs no csv file')
        try:
            with zipfile.ZipFile(zfile_name, "w") as zfile:
                pass
        except Exception as e:
            logger.error(e, exc_info=1)
    return send_file(zfile_name, as_attachment=True)