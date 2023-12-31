#
# Copyright (c) 2023 The Johns Hopkins University Applied Physics
# Laboratory LLC.
#
# This file is part of the Asynchronous Network Managment System (ANMS).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This work was performed for the Jet Propulsion Laboratory, California
# Institute of Technology, sponsored by the United States Government under
# the prime contract 80NM0018D0004 between the Caltech and NASA under
# subcontract 1658085.
#
''' Test the pure ORM models within models.py
'''
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ace.models import Base, AdmFile


class TestModels(unittest.TestCase):
    ''' Each test case run constructs a separate in-memory DB '''

    def setUp(self):
        self._db_eng = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self._db_eng)
        self._db_sess = Session(self._db_eng)

    def tearDown(self):
        self._db_sess.close()
        self._db_sess = None
        Base.metadata.drop_all(self._db_eng)
        self._db_eng = None

    def test_simple(self):
        self._db_sess.add(AdmFile(abs_file_path='hi'))
        self._db_sess.commit()

        objs = self._db_sess.query(AdmFile)
        self.assertEqual(1, objs.count())
        adm = objs.first()
        self.assertEqual('hi', adm.abs_file_path)
