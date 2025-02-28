"""
Short description of this Python module.

Longer description of this module.

xplordb

Copyright (C) 2022  Oslandia / OpenLog
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__authors__ = ["jmkerloch"]
__contact__ = "geology@oslandia.com"
__date__ = "2022/02/02"
__license__ = "AGPLv3"

import math
import unittest
from typing import List

import pytest
import sqlalchemy
from pytest import approx
from sqlalchemy import text

from xplordb.minimal_dao import MinimalDao

PERSON = 'xdb'  # Maximum 3 char
DATA_SET = 'test'
COLLAR = 'collar'

X_COLLAR = 100
Y_COLLAR = 150
Z_COLLAR = 0
SRID = 3857
EOH = 775.0


def test_person_import_lite_db(db_session, litedb_with_data):
    """
    Test if person sample data are imported with xplordb lite
    """
    _check_person_table_import(db_session, 6)


def test_person_import_full_db(db_session, fulldb_with_data):
    """
    Test if person sample data are imported with xplordb full
    """
    _check_person_table_import(db_session, 6)


def test_person_import_no_data(db_session, litedb_no_data):
    """
    Test that no person are imported with xplordb lite without sample data
    """
    _check_person_table_import(db_session, 0)


def test_person_import_no_data_full_db(db_session, fulldb_no_data):
    """
    Test that no person are imported with xplordb lite without sample data
    """
    _check_person_table_import(db_session, 0)


def _check_person_table_import(db_session, expected_number: int):
    """
    Test number of person available in xplordb

    :param db_session: psycog2 connection
    :param expected_number: expected number of person
    """
    with db_session.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM ref.person")
        rec = cur.fetchone()
        assert expected_number == rec[0]


def test_person_creation(sqlalchemy_session, litedb_no_data):
    """
    Test person creation with xplordb lite
    """
    dao = MinimalDao(sqlalchemy_session)
    dao.create_person(PERSON)
    sqlalchemy_session.commit()

    rec = sqlalchemy_session.execute(text("SELECT code FROM ref.person")).first()
    assert PERSON == rec[0]


def test_collar_creation(sqlalchemy_session, litedb_no_data):
    """
    Test collar creation without survey on xplordb lite
    """
    dao = MinimalDao(sqlalchemy_session)
    dao.create_collar(COLLAR, DATA_SET, PERSON)
    sqlalchemy_session.commit()

    rec = sqlalchemy_session.execute("SELECT hole_id,geom_trace FROM dh.collar").first()
    assert COLLAR == rec[0]
    assert not rec[1]


def test_collar_surv_creation(sqlalchemy_session, litedb_no_data):
    """
    Test collar creation with survey on xplordb lite
    """
    _create_and_check_collar_surv_creation(sqlalchemy_session)


def test_collar_surv_creation_full_database(sqlalchemy_session, fulldb_no_data):
    """
    Test collar creation with survey on xplordb full
    """
    _create_and_check_collar_surv_creation(sqlalchemy_session)


def _create_and_check_collar_surv_creation(sqlalchemy_session):
    """
    Create a collar and a simple survey and check that geometry is created

    :param db_session: psycog2 connection
    """
    surveys = _simple_collar_surv_creation(sqlalchemy_session, PERSON, DATA_SET, COLLAR, X_COLLAR, Y_COLLAR,
                                           Z_COLLAR,
                                           SRID, EOH)

    depth, x, y, z = _minimum_curvature_method(surveys, X_COLLAR, Y_COLLAR, Z_COLLAR, EOH)
    _check_table_geom_trace(sqlalchemy_session, x, y, z, depth, SRID, 'collar')


def _simple_collar_surv_creation(sqlalchemy_session, person: str, data_set: str,  collar: str,
                                 x_collar: float, y_collar: float, z_collar: float, srid: int, eoh: float = None):
    """
    Create a collar and a simple survey

    :param db_session: psycog2 connection
    :param person: person associated with collar
    :param data_set: data set associated with collar
    :param collar: collar name unique identifier
    :param x_collar: collar x coordinate
    :param y_collar: collar y coordinate
    :param z_collar: collar z coordinate
    :param srid: coordinate srid
    :param eoh: (optional) collar end of hole
    :return: list of surveys used
    """
    dao = MinimalDao(sqlalchemy_session)
    dao.create_collar(collar, data_set, person, x_collar, y_collar, z_collar, srid, eoh)

    surveys = [{'depth': 0.0, 'dip': 45.0, 'azimuth': 0.0},
               {'depth': 100.00, 'dip': 45.0, 'azimuth': 0.0},
               {'depth': 200.00, 'dip': 45.0, 'azimuth': 5.0},
               {'depth': 300.00, 'dip': 45.0, 'azimuth': 7.0},
               {'depth': 400.00, 'dip': 45.0, 'azimuth': 6.0}, ]
    for survey in surveys:
        dao.create_surv(survey['depth'], survey['dip'], survey['azimuth'], collar, data_set, person)

    sqlalchemy_session.commit()

    return surveys


def _check_table_geom_trace(sqlalchemy_session, x: List[float], y: List[float], z: List[float], depth: List[float],
                            srid: int, dh_table: str):
    """
    Check table geom_trace geometry from references values

    :param db_session: psycog2 connection
    :param x: expected point list x coordinates
    :param y: expected point list y coordinates
    :param z: expected point list z coordinates
    :param depth: expected point list m coordinates
    :param srid: point srid
    :param dh_table: table to check
    """
    values = sqlalchemy_session.execute(text(
        f"with point_list AS (SELECT (ST_DumpPoints(ST_Transform(geom_trace,{srid}))).geom as geom FROM dh.{dh_table})"
        "SELECT ST_X(geom), ST_Y(geom), ST_Z(geom),ST_M(geom) FROM point_list ORDER BY ST_Z(geom)")).all()
    assert len(values) == len(x)
    for i in range(0, len(values)):
        assert values[i][0] == approx(x[i])
        assert values[i][1] == approx(y[i])
        assert values[i][2] == approx(z[i])
        assert values[i][3] == approx(depth[i])


def _minimum_curvature_method(surveys, x_collar: float, y_collar: float, z_collar: float, eoh: float):
    """
    Define point list coordinates from Minimum curvature method implementation from https://www.drillingformulas.com/minimum-curvature-method/

    :param surveys: surveys list
    :param x_collar: collar x coordinate
    :param y_collar: collar y coordinate
    :param z_collar: collar z coordinate
    :return: depth, x, y, z : list of calculated coordinates
    """

    # A survey at depth 0.0 if not available
    if len(surveys):
        if surveys[0]['depth'] != 0.0:
            surveys.insert(0,{"dip": surveys[0]['dip'],
                            "azimuth": surveys[0]['azimuth'],
                            "depth": 0
                            }
                           )
    # append eoh survey
    surveys.append({'depth': eoh, 'dip': 45.0, 'azimuth': 6.0})

    surveys.sort(key = lambda x : x["depth"])

    depth_collar = 0.0
    x = [x_collar]
    y = [y_collar]
    z = [z_collar]
    depth = [depth_collar]
    current_x = x_collar
    current_y = y_collar
    current_z = z_collar
    current_depth = depth_collar
    for i in range(0, len(surveys) - 1):
        s2 = surveys[i + 1]
        s1 = surveys[i]
        # In xplordb dip is changed (for convention ?)
        i2 = math.radians(s2['dip'] + 90.0)
        i1 = math.radians(s1['dip'] + 90.0)
        a2 = math.radians(s2['azimuth'])
        a1 = math.radians(s1['azimuth'])
        CL = s2['depth'] - s1['depth']
        DL = math.acos(math.cos(i2 - i1) - (math.sin(i1) * math.sin(i2)) * (1 - math.cos(a2 - a1)))

        # Formula with different https//directionaldrillingart.blogspot.com/2015/09/directional-surveying-calculations.html
        # Produce same results
        # DL = math.acos((math.sin(i1) * math.sin(i2) * math.cos(a2 - a1)) + (math.cos(i1) * math.cos(i2)))
        RF = 1.0
        if DL != 0.0:
            # Formula with different method https//directionaldrillingart.blogspot.com/2015/09/directional-surveying-calculations.html
            # RF = math.tan(DL / 2) * (180 / math.pi) * (2 / DL)
            RF = math.tan(DL / 2) * (2 / DL)

        current_x = ((math.sin(i1) * math.sin(a1)) + (math.sin(i2) * math.sin(a2))) * (RF * (CL / 2)) + current_x
        current_y = ((math.sin(i1) * math.cos(a1)) + (math.sin(i2) * math.cos(a2))) * (RF * (CL / 2)) + current_y
        current_z = - (math.cos(i1) + math.cos(i2)) * (CL / 2) * RF + current_z
        current_depth += CL
        x.append(current_x)
        y.append(current_y)
        z.append(current_z)
        depth.append(current_depth)
    return depth, x, y, z


#def test_collar_details_surv_creation(sqlalchemy_session, litedb_no_data):
#    """
#    Test collar creation with survey and details on xplordb lite
#    """
#    _create_and_check_collar_surv_details_creation(sqlalchemy_session)


#def test_collar_details_surv_creation_full_database(sqlalchemy_session, fulldb_no_data):
#    """
#    Test collar creation with survey and details on xplordb full
#    """
#    _create_and_check_collar_surv_details_creation(sqlalchemy_session)


def _create_and_check_collar_surv_details_creation(sqlalchemy_session):
    """
    Create a collar with a simple survey and details and check that geometry is created

    :param db_session: psycog2 connection
    """
    surveys = _collar_with_details_creation(sqlalchemy_session, PERSON, DATA_SET, COLLAR, X_COLLAR, Y_COLLAR,
                                            Z_COLLAR, SRID, EOH)
    depth, x, y, z = _minimum_curvature_method(surveys, X_COLLAR, Y_COLLAR, Z_COLLAR, EOH)
    _check_table_geom_trace(sqlalchemy_session, x, y, z, depth, SRID, 'collar')
    _check_table_geom_trace(sqlalchemy_session, x, y, z, depth, SRID, 'details')

    # Add new survey and check that details geom_trace is updated with new survey
    dao = MinimalDao(sqlalchemy_session)
    new_surveys = [{'depth': 750.0, 'dip': 45.0, 'azimuth': 8.0}, ]
    for survey in new_surveys:
        dao.create_surv(survey['depth'], survey['dip'], survey['azimuth'], COLLAR, DATA_SET, PERSON)
        surveys.append(survey)
    sqlalchemy_session.commit()

    depth, x, y, z = _minimum_curvature_method(surveys, X_COLLAR, Y_COLLAR, Z_COLLAR, EOH)
    _check_table_geom_trace(sqlalchemy_session, x, y, z, depth, SRID, 'collar')
    _check_table_geom_trace(sqlalchemy_session, x, y, z, depth, SRID, 'details')


def _collar_with_details_creation(sqlalchemy_session, person: str, data_set: str, collar: str,
                                  x_collar: float, y_collar: float, z_collar: float, srid: int, eoh: float):
    """
    Create a collar with simple survey and add details

    :param db_session: psycog2 connection
    :param person: person associated with collar
    :param data_set: data set associated with collar
    :param collar: collar name unique identifier
    :param x_collar: collar x coordinate
    :param y_collar: collar y coordinate
    :param z_collar: collar z coordinate
    :param srid: coordinate srid
    :return: list of surveys used
    """
    surveys = _simple_collar_surv_creation(sqlalchemy_session, person, data_set, collar,
                                           x_collar, y_collar, z_collar, srid, eoh)
    dao = MinimalDao(sqlalchemy_session)
    dao.create_details(0.0, 750.0, collar, data_set, person)
    sqlalchemy_session.commit()
    return surveys


def test_surv_depth_check_with_eoh(sqlalchemy_session, litedb_no_data):
    """
    Test survey creation outside collar details
    """
    _simple_collar_surv_creation(sqlalchemy_session, PERSON, DATA_SET, COLLAR, X_COLLAR, Y_COLLAR, Z_COLLAR, SRID,
                                 750.0)
    # Add new survey after details maximum depth
    expected_message = "error! depth exceeds maximum hole depth (750). Check input or add details for collar in dh.details."
    with pytest.raises(sqlalchemy.exc.InternalError) as expect:
        dao = MinimalDao(sqlalchemy_session)
        new_surveys = [{'depth': 800.0, 'dip': 45.0, 'azimuth': 8.0}, ]
        for survey in new_surveys:
            dao.create_surv(survey['depth'], survey['dip'], survey['azimuth'], COLLAR, DATA_SET, PERSON)
        sqlalchemy_session.commit()
    assert expected_message in str(expect.value)


def test_trace_update_tables_all_function(sqlalchemy_session, litedb_no_data):
    """
    Test call for function dh.trace_update_tables_all() on xplordb lite

    For now only check if no error is raised when executing function
    """
    _check_trace_update_tables_all_function(sqlalchemy_session)


def test_trace_update_tables_all_function_full_database(sqlalchemy_session, fulldb_no_data):
    """
    Test call for function dh.trace_update_tables_all() on xplordb full

    For now only check if no error is raised when executing function
    """
    _check_trace_update_tables_all_function(sqlalchemy_session)


def _check_trace_update_tables_all_function(sqlalchemy_session):
    """
    Create a collar with survey and details and check dh.trace_update_tables_all() execution

    :param db_session: psycog2 connection
    """
    _collar_with_details_creation(sqlalchemy_session, PERSON, DATA_SET, COLLAR, X_COLLAR, Y_COLLAR, Z_COLLAR, SRID, EOH)
    sqlalchemy_session.execute(text("SELECT dh.trace_update_tables_all()"))


def test_trace_update_tables_hole_function_full_database(sqlalchemy_session, fulldb_no_data):
    """
    Test call for function dh.trace_update_tables_hole() on xplordb full

    For now only check if no error is raised when executing function
    """
    _check_trace_update_tables_hole(sqlalchemy_session)


def test_trace_update_tables_hole_function(sqlalchemy_session, litedb_no_data):
    """
    Test call for function dh.trace_update_tables_hole() on xplordb lite

    For now only check if no error is raised when executing function
    """
    _check_trace_update_tables_hole(sqlalchemy_session)


def _check_trace_update_tables_hole(sqlalchemy_session):
    """
    Create a collar with survey and details and check dh.trace_update_tables_hole() execution

    :param db_session: psycog2 connection
    """
    _collar_with_details_creation(sqlalchemy_session, PERSON, DATA_SET, COLLAR, X_COLLAR, Y_COLLAR, Z_COLLAR, SRID, EOH)
    sqlalchemy_session.execute(text(f"SELECT dh.trace_update_tables_hole('{COLLAR}')"))


def test_survey_incomplete_azimuth_values(sqlalchemy_session, litedb_no_data):
    """
    Test exception raised if survey with azimuth defined an no azimuth date
    """
    dao = MinimalDao(sqlalchemy_session)
    dao.create_collar(COLLAR, DATA_SET, PERSON, X_COLLAR, Y_COLLAR, Z_COLLAR, SRID)
    expected_message = 'new row for relation "surv" violates check constraint "dh_surv_check_azimuth_date"'
    with pytest.raises(sqlalchemy.exc.IntegrityError) as expect:
        dao.create_invalid_surv(0.0, 0.0, 0.0, COLLAR, DATA_SET, PERSON)
    assert expected_message in str(expect.value)


if __name__ == '__main__':
    unittest.main()
