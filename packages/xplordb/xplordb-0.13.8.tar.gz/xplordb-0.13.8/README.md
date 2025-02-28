# xplordb

Mineral Exploration Database template/ system for Postgres/PostGIS and QGIS.

The project incorporates import scripts, data storage, validation, reporting, 3D drill trace generation and more. psql, pgAdmin and QGIS are the suggested database and GIS front-end programs.

The xplordb database template also comes with a python `xplordb` package.


## Installation
`xplordb` package can be installed with pip :

```
pip install xplordb
```

## Install xplordb schema
```python
from xplordb.import_ddl import ImportDDL
import_ddl = ImportDDL(db='xplordb',
                       user='postgres',
                       password='postgres',
                       host='localhost',
                       port=5432)

import_ddl.import_xplordb_schema(import_data=False,
                                 full_db=False)
```
> xplordb schema installation can only be done on existing database


## Create xplordb database
```python
from xplordb.create_db import CreateDatabase
create_db = CreateDatabase(connection_db='postgres',
                       user='postgres',
                       password='postgres',
                       host='localhost',
                       port=5432)

create_db.create_db(db='xplordb', import_data=False, full_db=False)
```
> connection database is needed for new database creation

Available options are :
- `import_data` : Import sample data
- `full_db` : Import not mandatory tables

## xplordb API

With xplordb package you can data to an xplordb database.

Here are some examples of API use.

### Create mandatory Person and Dataset
```python
from xplordb.sqlalchemy.base import create_session
from xplordb.datamodel.person import Person
from xplordb.datamodel.dataset import Dataset
from xplordb.import_data import ImportData

session = create_session(
        database='xplordb',
        host='localhost',
        port=5432,
        user='postgres',
        password='postgres')
import_data = ImportData(session)
import_data.import_persons_array([Person(trigram="xdb",full_name= "default")])
import_data.import_datasets_array([Dataset(name="default",loaded_by= "xdb")])
session.commit()
```

### Create a collar
```python
from xplordb.sqlalchemy.base import create_session
from xplordb.datamodel.collar import Collar
from xplordb.import_data import ImportData

session = create_session(
        database='xplordb',
        host='localhost',
        port=5432,
        user='postgres',
        password='postgres')
import_data = ImportData(session)
import_data.import_collars_array([Collar(hole_id="collar",
                                         data_set='default',  
                                         loaded_by='xdb',
                                         x=100.0,y= 100.0,z= 0.0,srid= 3857)])
session.commit()
```

> We assume that person and dataset are already available in xplordb database

### Add survey to collar
```python
from xplordb.sqlalchemy.base import create_session
from xplordb.datamodel.survey import Survey
from xplordb.import_data import ImportData

session = create_session(
        database='xplordb',
        host='localhost',
        port=5432,
        user='postgres',
        password='postgres')
import_data = ImportData(session)
import_data.import_surveys_array([Survey('collar', 'default', 'xdb', dip=0.0,azimuth= 45.0,depth= 0.0),
                                  Survey('collar', 'default', 'xdb', dip=0.1,azimuth= 44.5,depth= 100.0),
                                  Survey('collar', 'default', 'xdb', dip=0.0,azimuth= 45.0,depth= 200.0)])
session.commit()
```
> We assume that person dataset and collar are already available in xplordb database


### Use sqlalchemy session for new query

`xplordb` module provides sqlalchemy table description that can be used to interact with xplordb database without using `ImportData` class :

- `ref.person` : `xplordb.sqlalchemy.ref.person.XplordbPersonTable`
- `ref.dataset` : `xplordb.sqlalchemy.ref.dataset.XplordbDatasetTable`
- `dh.collar` : `xplordb.sqlalchemy.dh.collar.XplordbCollarTable`
- `dh.survey` : `xplordb.sqlalchemy.dh.survey.XplordbSurveyTable`
- `ref.lithology` : `xplordb.sqlalchemy.ref.lithcode.XplordbLithCodeTable`
- `df.lith` : `xplordb.sqlalchemy.df.lith.XplordbLithTable`

Example to get all survey for a collar list:

```python
from xplordb.sqlalchemy.base import create_session
from xplordb.sqlalchemy.dh.survey import XplordbSurveyTable

session = create_session(
        database='xplordb',
        host='localhost',
        port=5432,
        user='postgres',
        password='postgres')
collars_id = ['HOLE_1', 'HOLE_2']
surveys = session.query(XplordbSurveyTable).filter(XplordbSurveyTable.hole_id.in_(collars_id)).all()
```


