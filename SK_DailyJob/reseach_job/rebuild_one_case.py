# -*- coding: utf-8 -*-
import datetime
import json
import logging
import sys
import os
from app import mongo, db
from app.models import *
from app.modules.case import add_case_by_path, prepare_for_show
from app.settings import DATA_INSTANCE_FOLDER
from app.tools.ffr_helper import get_ffr_meta

logger = logging.getLogger(__name__)


def rebuild_test(case_id):
    def generate_test_data(case_id):
        session = db.session
        case = Case.query.filter(Case.case_num == case_id).first()
        if case:
            # �~H| �~Y�mysql
            db.session.delete(case)
            # mongo�~H| �~Y��~U��~M�
            filter_string = {'case_num': case_id}
            mongo.db.cases.delete_one(filter_string)
            mongo.db.reports.delete_one(filter_string)

        session.flush()

        for case_num in os.listdir(DATA_INSTANCE_FOLDER):
            if case_num != case_id:
                continue
            # case路�~D
            case_fp = os.path.join(DATA_INSTANCE_FOLDER, case_num)
            # case�~I~@�~L~E�~P��~N~_�~I~G路�~D
            slice_fp = os.path.join(case_fp, 'slices')

            if (not os.path.isdir(case_fp)
                    or not os.path.isdir(slice_fp)
                    or case_num.startswith('.')):
                continue

            logger.info('Generating test data for %s', case_num)
            try:
                if case_num.startswith('CEREBRAL'):
                    category = 'cerebral'
                else:
                    category = 'coronary'
                # 添�~J| mysql记�~U
                add_case_by_path(slice_fp, case_num, case_type=category)
                c = Case.query.filter(Case.case_num == case_num).first()
                # 添�~J| mongo记�~U
                prepare_for_show(c)
                # �~T~_�~H~Pffr�~I~@�~\~@json
                ffr_meta = get_ffr_meta(case_num)
                with open(os.path.join(DATA_INSTANCE_FOLDER, case_num, 'ffr_meta.json'), 'w') as fp:
                    json.dump(ffr_meta, fp)
            except BaseException:
                print("error")
                logger.warning('Failed to process %s', case_num, exc_info=1)
                continue

            Case.query.update({
                Case.study_datetime: datetime.datetime.now(), Case.upload_time: datetime.datetime.now(),
                Case.finish_time: datetime.datetime.now(),
                Case.state: Case.GENERATED
            })

            session.commit()

    generate_test_data(case_id)
    from migrations.add_migration_log import add_migration_log
    add_migration_log()
    print("success")


if __name__ == '__main__':
    rebuild_test(case_id=str(sys.argv[1]))