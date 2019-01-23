import numpy as np
import time
import lmdb
import sys
import math
import gc

caffe_root = '/data/jiaxin/caffe/'
sys.path.insert(0, caffe_root+'python')
import caffe

from txt2npz import Txt2npz
from npz2lmdb import Npz2lmdb
from npz2lmdb_invert import Npz2lmdb_Invert

from npz2lmdb_classify import Npz2lmdb_Classify
from npz2lmdb_classify_invert import Npz2lmdb_Classify_Invert
from lmdb_processing import Post_process_lmdb

COMMIT_LENGTH = 10000


if __name__ == "__main__":


    # ================= npz -> lmdb =====================
    t0 = time.time()
    # LMDB construction for regressor
    # with Npz2lmdb_Invert('npz/my_log_15h.npz', 10) as npz2lmdb:
    
    # LMDB construction for classifier
    with Npz2lmdb_Classify_Invert('npz/my_log_15h.npz', 10) as npz2lmdb:
        #npz2lmdb.add_noise_to_scan()
        npz2lmdb.normalize_scan()

        # only for classifier, add the extremely low frequency for negative data
        npz2lmdb.insert_data_into_lmdb(0.001, 'lmdb/', is_add_to_label_stat=False)
        #npz2lmdb.insert_data_into_lmdb(0.005, 'lmdb/', is_add_to_label_stat=False)
        #npz2lmdb.insert_data_into_lmdb(0.01, 'lmdb/', is_add_to_label_stat=False)
        npz2lmdb.insert_data_into_lmdb(0.05, 'lmdb/', is_add_to_label_stat=False)
        npz2lmdb.insert_data_into_lmdb(0.2, 'lmdb/', is_add_to_label_stat=False)

        # for both classifier and regressor
        npz2lmdb.insert_data_into_lmdb(0.5, 'lmdb/', is_add_to_label_stat=True)
        npz2lmdb.insert_data_into_lmdb(1, 'lmdb/', is_add_to_label_stat=True)
        npz2lmdb.insert_data_into_lmdb(2, 'lmdb/', is_add_to_label_stat=True)

        # necessary for regressor
        # npz2lmdb.normalize_label('lmdb/')

        # print npz2lmdb.m_label_dx_mean
        # print npz2lmdb.m_label_dx_std
        # print npz2lmdb.m_label_dy_mean
        # print npz2lmdb.m_label_dy_std
        # print npz2lmdb.m_label_dtheta_mean
        # print npz2lmdb.m_label_dtheta_std

    print('npz2lmdb. Time consumed (s): {0}'.format(time.time()-t0))

    gc.collect()
    # ================= lmdb shuffle =====================
    t0 = time.time()
    with Post_process_lmdb('lmdb/') as post_processing:
        post_processing.shuffle_lmdb_data_only('train')
    print('lmdb shuffle. Time consumed (s): {0}'.format(time.time() - t0))
