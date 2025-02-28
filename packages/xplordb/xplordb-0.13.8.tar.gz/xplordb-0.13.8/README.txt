xplordb
Version 0.87
April 2020
Sixth beta-release

This file is part of xplordb.

    xplordb is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    xplordb is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with xplordb.  If not, see <http://www.gnu.org/licenses/>.


--xplordb database template - xplordb_dh_0.87.sql
	*re-organisation of schemas will hopefully be more clear
	   and logical. dh. assay. dem. ref. qa. surf.
	*removed 'with oids' from spatial tables, no longer needed.
	*improvements to 3D downhole function dh.trace, changed
	   geometry type to CompundCurveZM
	*perl import script example replaced with assay.import() function example
	*dh.assay table modified and simplified. assay_result_num is
	   now a range data type (numrange), this records if the result
	   is overange or below detection limit, therefore assay_result_code
	   column is no longer needed. Also removed data_source column as
	   redundant (recorded in assay.batch)
	*dh.details table added
	*ref.preffered the 0 code no longer indicates over range value
	*ref.lab_o_method added to implement o_method in assay.assay table
	*dates changed to time stamp
	*changes to ref.lease table
	*changes to ref.prospect table, added geometry columns and more
	*dh.sample - add sample class
	*dh.petrology - changes for sample depth and other changes
	*various changes to primary keys, constraints and comments(douments)
	*additional ref. (reference) tables
	*added trigger on ref.lab_method to insert new codes into
		ref.lab_method_code on insert or update
	*refinements to some existing triggers
	*added QGIS example project - ref.qgis_capricorn_project. Load
		via Project-Open From-PostgreSQL
	*new tables
		dh.sample_image
		dh.sample_weight
		ref.company_type
		ref.core_type
		ref.loc_confidence
		ref.program
		ref.rl_method
		ref.sample_class
		ref.sg_method
		ref.strat_name
		ref.xrf_instrument
		assay.flat_ppm
		assay_flat_method
		assay.raw
	
	*new views
		v.missing_samples
		v.missing_surv
		dh.collar_view
		dh.collar_view_geom
		dh.collar_view_geom_trace
		assay.intercept example of a query to report a summary 
			of siginificant assay intercepts
	
	*new functions
		assay.flat_ppm()
			assay results in ppm
		assay.flat_method()
			flat table of assay method
		assay.import
			sql example to convert lab assay results to
			assay.assay table 
	
	*new trigger funtions
		dh.trace_update_tables_hole_trigger() updates dh.* tables
			when dh.collar.geom_trace is inserted, deleted or
			updated
		dh.trace_update_row() updates the particular row on dh.*
			tables when a row is inserted or updated				
		dh.trace_update_xyz() updates the dh trace (geom_trace) on
			dh.collar when x,y,z,hole_id is inserted or updated		
--Perl import script example
	*depreciated by built-in \copy and SQL function example

TODO
        Documentation todo
        *Workflow
	*function/trigger comments
	*update wiki
	*ssl root certificate, verify-full 
		http://www.howtoforge.com/postgresql-ssl-certificates

        Other
	*Audit/ version history or summary e.g. https://github.com/pgaudit/pgaudit 
		or https://wiki.postgresql.org/wiki/Audit_trigger_91plus
		or aquameta? bundles?
		or https://github.com/beaud76/emaj
	*add some default logging codes to ref.struc
	*new overlap constraint?
	*implement lab dispatch tables ref.lab_pulp_rejects
	*on moving collar geom point trigger to change co-ords xyz?
	*to store exploration geophysics data
	*QGIS Data entry, Roam QGIS?
	*QGIS geopackage gpkg version ogr2ogr
	*add roles client, dataentry, dbadmin
	*store files/photos - QGIS
	*add spatial to ref.data_source?
	*alerts - assays entered, notification when offline etc. 
		(enterprisedb also aquameta)

 

Version 0.86
October 2017

Fifth beta-release

--xplordb database template - xplordb_dh_0.85.sql
        *3D downhole survey position calculated with much 
	   improvedfunction dh.dh_trace(), the single hole 
	   or multiple hole result is inserted into
           dh.dh_collar.geom_trace, which can be viewed in
           QGIS (www.qgis.org).


Version 0.85
July 2015

Fourth beta-release

--Perl import script - xdb_im-0.85.pl
	*lower limit may now be null

--xplordb database template - xplordb_dh_0.85.sql
	*flat assay table query/view re-written
	*3D downhole survey position calculated with function
	   dh.dh_trace(), the single hole result is inserted into 
	   dh.dh_collar.geom_trace, which can be viewed in 
	   QGIS (www.qgis.org).
	*dh_surv table - more columns added for separate dip
	   and azimuth details. Extra corresponding reference
	   tables also added.

--documentation
	*numerous updates and improvements

--example data added

--template now as postgres backup file which can be restored to 
	a schema called 'dh'.  

TODO
	Documentation todo
	*Workflow

	Other 
	*R graphs
	*check for entry in ref_data_source in assay import perl script
	*assay intersection calculation


Version 0.84
10 April 2012

Third beta-release

--Perl import script - xdb_im-0.84.pl
	*numerous improvments
	*user interaction and review
	*less manual data entry
	*example script now uses a more detailed lab file format

--xplordb database template - xplordb_dh_0.84.sql
	*flat assay table query/view re-written
	*a number of new queries/ reports/ validation/ contraints
	*check interval overlap contraint added
	*tables, columns added

--documentation
	*numerous updates and improvements


TODO
	Documentation todo
	*Views/ Reports
	*QA/QC
	*Workflow

	Other 
	*function to create 3D drill trace
	*graphs
	*check for entry in ref_data_source in assay import perl script
	*dh_survey.depth <= dh.collar.max_depth
	*assay intersection calculation

Version 0.83
26 November 2011

Second beta-release 

--Perl import script - xplordb_im-0.81.pl
	*results are now imported directly into database with INSERT statements.
	*database tests if batch already exsits and user asked to continue
	*database tests if batch is in dh.assay_batch
	*user input reviewed and asked to continue
	*calculates batch statistics and inserts into dh.assay+_batch
	*updated to accept lower limit values from the header of the lab assay file , see script for other improvements.
	*example lab file --lab_result.csv

--xplordb database template - xplordb_dh_0.83.sql
	*project name and file naming changed to all lower case due to problems restoring the database in upper case
	*documentation of tables, views and columns added to comment field
	*number of improvements to tables, constraints etc.
	*function to create geometry column for dh.dh_collars and dh.surf_sample

--Documentation 
	*Tables, views and columns now added to database comments as above.
	*Wiki extensively updated - User Access, Vailidation, Linux Install, Tables, etc.
	
Contact the project if you would like to help. 
Summary page: https://sourceforge.net/projects/xplordb/
Files: https://sourceforge.net/projects/xplordb/files/
Documentation Wiki: https://sourceforge.net/p/xplordb/xdb/Main_Page/
