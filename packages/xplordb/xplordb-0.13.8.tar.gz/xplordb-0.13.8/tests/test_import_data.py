from datetime import datetime

import pytest
from sqlalchemy import text

from xplordb.datamodel.collar import Collar
from xplordb.datamodel.metadata import RawCollarMetadata
from xplordb.datamodel.dataset import Dataset
from xplordb.datamodel.lith import Lith
from xplordb.datamodel.person import Person
from xplordb.datamodel.survey import Survey
from xplordb.import_data import ImportData

def test_metadata_import(data_importer, db_session, litedb_no_data):

    # first, add some collars
    persons = [Person('xdb')]
    data_importer.import_persons_array(persons)

    datasets = [Dataset('test', 'xdb'), ]
    data_importer.import_datasets_array(datasets)

    collars = [Collar('collar', 'test',  'xdb', 100.0, 100.0, 0.0, 3857, 100.0, 100.0, 0.0,1000),
               Collar('collar2', 'test',  'xdb', 100.0, 100.0, 0.0, 3857, 100.0, 100.0, 0.0,None),
               Collar('collar3', 'test',  'xdb', 100.0, 100.0, 0.0, 3857, 100.0, 100.0, 0.0,None, None,datetime.now())]
    data_importer.import_collars_array(collars)
    data_importer.commit()

    # import metadata
    metadatas = [RawCollarMetadata(hole_id="collar", extra_cols={"col_a" : 10}),
                 RawCollarMetadata(hole_id="collar3", extra_cols={"col_b" : 5})]
    
    data_importer.import_metadatas_array(metadatas)
    data_importer.commit()
    expected = [("collar", 10, None), 
                ("collar2", None, None), 
                ("collar3", None, 5)]
    
    with db_session.cursor() as cur:
        cur.execute("SELECT * FROM dh.metadata ORDER BY hole_id")
        values = cur.fetchall()
        assert len(values) == len(collars)
        for value, exp in zip(values, expected):
            assert value == exp




def test_person_import(data_importer, db_session, litedb_no_data):
    """
    Test person import
    """
    persons = [Person('a', 'a'),
               Person('b', 'b'),
               Person('c', 'c'), ]
    data_importer.import_persons_array(persons)
    data_importer.commit()

    with db_session.cursor() as cur:
        cur.execute("SELECT code,loaded_by,person,type,active FROM ref.person")
        values = cur.fetchall()
        assert len(values) == len(persons)
        for i in range(0, len(values)):
            assert values[i][0] == persons[i].code
            assert values[i][1] == persons[i].loaded_by
            assert values[i][2] == persons[i].full_name
            assert values[i][3] == persons[i].type
            assert values[i][4] == persons[i].active


def test_get_available_persons(data_importer, db_session, litedb_no_data):
    """
    Test person read from database
    """
    test_person_import(data_importer, db_session, litedb_no_data)
    assert data_importer.get_available_person_codes() == ['a', 'b', 'c']


def test_dataset_import_invalid_person(data_importer, litedb_no_data):
    """
    Test dataset import with invalid person
    """
    with pytest.raises(ImportData.ImportException):
        datasets = [Dataset('test', 'invalid')]
        data_importer.import_datasets_array(datasets)
        data_importer.commit()


def test_dataset_import(data_importer, db_session, litedb_no_data):
    """
    Test dataset import
    """
    persons = [Person('xdb')]
    data_importer.import_persons_array(persons)

    datasets = [Dataset('test', 'xdb', 'full_test_name'),
                Dataset('test2', 'xdb', 'full_test2_name'), ]
    data_importer.import_datasets_array(datasets)
    data_importer.commit()

    with db_session.cursor() as cur:
        cur.execute("SELECT data_set,full_name,loaded_by FROM ref.data_sets")
        values = cur.fetchall()
        assert len(values) == len(datasets)
        for i in range(0, len(values)):
            assert values[i][0] == datasets[i].name
            assert values[i][1] == datasets[i].full_name
            assert values[i][2] == datasets[i].loaded_by


def test_get_available_datasets(data_importer, db_session, litedb_no_data):
    """
    Test datasets read from database
    """
    test_dataset_import(data_importer, db_session, litedb_no_data)
    assert data_importer.get_available_dataset_names() == ['test', 'test2']


def test_collar_import_invalid_fk(data_importer, litedb_no_data):
    """
    Test collar import with an invalid foreign key
    """
    with pytest.raises(ImportData.ImportException):
        collar = [Collar('collar', 'test', 'xdb', 100.0, 100.0, 0.0, 3857), ]
        data_importer.import_collars_array(collar)
        data_importer.commit()


def test_collar_import(data_importer, db_session, litedb_no_data):
    """
    Test collar import
    """
    persons = [Person('xdb')]
    data_importer.import_persons_array(persons)

    datasets = [Dataset('test', 'xdb'), ]
    data_importer.import_datasets_array(datasets)

    collars = [Collar('collar', 'test',  'xdb', 100.0, 100.0, 0.0, 3857, 100.0, 100.0, 0.0,1000),
               Collar('collar2', 'test',  'xdb', 100.0, 100.0, 0.0, 3857),
               Collar('collar3', 'test',  'xdb', 100.0, 100.0, 0.0, 3857, None, None, None,None, None, datetime.now())]
    data_importer.import_collars_array(collars)
    data_importer.commit()

    with db_session.cursor() as cur:
        cur.execute("SELECT data_set,hole_id,loaded_by,x,y,z,srid,eoh, planned_x, planned_y, planned_z, planned_eoh,survey_date FROM dh.collar")
        values = cur.fetchall()
        assert len(values) == len(collars)
        for i in range(0, len(values)):
            assert values[i][0] == collars[i].data_set
            assert values[i][1] == collars[i].hole_id
            assert values[i][2] == collars[i].loaded_by
            assert values[i][3] == collars[i].x
            assert values[i][4] == collars[i].y
            assert values[i][5] == collars[i].z
            assert values[i][6] == collars[i].srid
            assert values[i][7] == collars[i].eoh
            assert values[i][8] == collars[i].planned_x
            assert values[i][9] == collars[i].planned_y
            assert values[i][10] == collars[i].planned_z
            assert values[i][11] == collars[i].planned_eoh
            if collars[i].survey_date:
                # Check date and time for no timezone comparison (not setted in now())
                assert values[i][12].date() == collars[i].survey_date.date()
                assert values[i][12].time() == collars[i].survey_date.time()


def test_survey_import_invalid_fk(data_importer, litedb_no_data):
    """
    Test survey import with an invalid foreign key
    """
    with pytest.raises(ImportData.ImportException):
        surveys = [Survey('collar', 'test', 'xdb', 0.0, 45.0, 0.0), ]
        data_importer.import_surveys_array(surveys)
        data_importer.commit()


def test_survey_import(data_importer, db_session, litedb_no_data):
    """
    Test survey import
    """
    persons = [Person('xdb')]
    data_importer.import_persons_array(persons)

    datasets = [Dataset('test', 'xdb'), ]
    data_importer.import_datasets_array(datasets)

    collars = [Collar('collar', 'test', 'xdb', 100.0, 100.0, 0.0, 3857), ]
    data_importer.import_collars_array(collars)

    surveys = [Survey('collar', 'test', 'xdb', 0.0, 45.0, 0.0), ]
    data_importer.import_surveys_array(surveys)
    data_importer.commit()

    with db_session.cursor() as cur:
        cur.execute("SELECT data_set,hole_id,loaded_by,depth_m,dip,azimuth_grid FROM dh.surv")
        values = cur.fetchall()
        assert len(values) == len(surveys)
        for i in range(0, len(values)):
            assert values[i][0] == surveys[i].data_set
            assert values[i][1] == surveys[i].hole_id
            assert values[i][2] == surveys[i].loaded_by
            assert values[i][3] == surveys[i].depth
            assert values[i][4] == surveys[i].dip
            assert values[i][5] == surveys[i].azimuth


def test_lith_import(data_importer, db_session, litedb_no_data):
    """
    Test lith import
    """
    persons = [Person('xdb')]
    data_importer.import_persons_array(persons)

    datasets = [Dataset('test', 'xdb'), ]
    data_importer.import_datasets_array(datasets)

    collars = [Collar('collar', 'test',  'xdb', 100.0, 100.0, 0.0, 3857), ]
    data_importer.import_collars_array(collars)

    liths = [Lith('lith1', 'test', 'collar', 'xdb',  0.0, 10.0),
             Lith('lith1', 'test', 'collar', 'xdb',  10., 100.0)]
    data_importer.import_liths_array(liths)
    data_importer.commit()

    with db_session.cursor() as cur:
        cur.execute("SELECT data_set,hole_id,loaded_by,lith_code_1,from_m,to_m FROM dh.lith")
        values = cur.fetchall()
        assert len(values) == len(liths)
        for i in range(0, len(values)):
            assert values[i][0] == liths[i].data_set
            assert values[i][1] == liths[i].hole_id
            assert values[i][2] == liths[i].loaded_by
            assert values[i][3] == liths[i].lith_code
            assert values[i][4] == liths[i].from_m
            assert values[i][5] == liths[i].to_m
