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
''' An interface and runner of model consistency constraints.
'''
from dataclasses import dataclass
import logging
from ace import models


LOGGER = logging.getLogger(__name__)
#: Accumulated list of all constraints to check
CONSTRAINTS = {}


@dataclass
class Issue:
    ''' An issue resulting from a failed constraint.
    '''
    #: The name of the constraint noting the issue, which will be set automatically
    check_name: str = None
    #: The name of the ADM containing the issue, which will be set automatically
    adm_name: str = None
    #: The object containing the issue
    obj: object = None
    #: Any specific detail about the issue
    detail: str = None


def register(obj):
    ''' A decorator to mark a function as being ADM constraint-checking.

    All constraint functions must take arguments of:
      - issuelist: a list of aggregated :class:`Issue` objects
      - obj: The object being checked, starting at the :class:`AdmFile`
      - db_sess: The database session being run under.
    '''
    if isinstance(obj, type):
        name = f'{obj.__module__}.{obj.__name__}'
        obj = obj()
    elif callable(obj):
        name = f'{obj.__module__}.{obj.__name__}'
    else:
        raise TypeError(f'Object given to register() is not usable: {obj}')
    CONSTRAINTS[name] = obj


class Checker:
    ''' A class which visits objects of the ORM and performs checks
    to create Issue objects.

    :param db_sess: A database session to operate within.
    '''

    def __init__(self, db_sess):
        self._db_sess = db_sess

    def check(self, src: models.AdmFile = None):
        ''' Check a specific ADM for issues.

        :param src: The ADM to check or None.
        :return: A list of found :class:`Issue` objects.
        '''
        if src is not None:
            adm_list = (src,)
        else:
            adm_list = self._db_sess.query(models.AdmFile).all()

        check_count = 0
        allissues = []

        # Run global constraints once
        for cst_name, cst in CONSTRAINTS.items():
            if getattr(cst, 'is_global', False):
                issuelist = []
                self._add_result(issuelist, check_count, cst_name, cst, adm=None)
                allissues += issuelist

        # Run non-global constraints per each adm
        for adm in adm_list:
            adm_name = adm.norm_name
            LOGGER.debug('Checking ADM: %s', adm_name)
            for cst_name, cst in CONSTRAINTS.items():
                if getattr(cst, 'is_global', False):
                    continue

                issuelist = []
                self._add_result(issuelist, check_count, cst_name, cst, adm)
                allissues += issuelist

        LOGGER.info('Checked %d rules and produced %d issues',
                    check_count, len(allissues))
        return allissues

    def _add_result(self, issuelist, check_count, cst_name, cst, adm):
        LOGGER.debug('Running constraint check: %s', cst_name)
        count = cst(issuelist, adm, self._db_sess) or 0
        check_count += count

        for issue in issuelist:
            if issue.adm_name is None:
                if adm is not None:
                    issue.adm_name = adm.norm_name
                elif isinstance(issue.obj, models.AdmFile):
                    issue.adm_name = issue.obj.norm_name
            if issue.check_name is None:
                issue.check_name = cst_name
        LOGGER.debug(
            'Checked %d rules and produced %d issues:\n%s',
            count, len(issuelist),
            '\n'.join(repr(iss) for iss in issuelist)
        )
