----------------------------------------------------------------------------
-- xplordb
-- 
-- Copyright (C) 2022  Oslandia / OpenLog
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as published
-- by the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
-- 
-- You should have received a copy of the GNU Affero General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.
-- 
-- __authors__ = ["davidms"]
-- __contact__ = "geology@oslandia.com"
-- __date__ = "2022/02/02"
-- __license__ = "AGPLv3"
----------------------------------------------------------------------------

--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: surv; Type: TABLE DATA; Schema: dh; Owner: postgres
--

COPY dh.surv (data_set, hole_id, depth_m, dip, azimuth, azimuth_type, azimuth_grid, dh_survey_method_dip, dh_survey_method_azimuth, srid, date_surveyed_dip, date_surveyed_azimuth, dh_survey_company_dip, dh_survey_company_azimuth, dh_survey_operator_dip, dh_survey_operator_azimuth, dh_survey_instrument_dip, dh_survey_instrument_azimuth, comment, load_date, loaded_by, data_source, local_grid_azimuth, local_grid_id) FROM stdin;
Capricorn	WA13/10900	0	-90	0	magnetic	0	u	u	20350	2000-06-23 18:00:00+02	2000-06-23 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA10/11350	0	-90	0	magnetic	0	u	u	20350	2000-06-25 18:00:00+02	2000-06-25 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	mag susc. Not as elevated as in WA10/11200.   1000-2000SI units in pisolitic clays	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA15/12475	0	-90	0	magnetic	0	u	u	20350	2000-06-20 18:00:00+02	2000-06-20 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA14/11175	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA15/12625	0	-90	0	magnetic	0	u	u	20350	2000-06-20 18:00:00+02	2000-06-20 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	siliceous siltstone outcrop 545610  7264403 so40 340	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA13/10600	0	-90	0	magnetic	0	u	u	20350	2000-06-23 18:00:00+02	2000-06-23 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10375	0	-90	0	magnetic	0	u	u	20350	2000-06-25 18:00:00+02	2000-06-25 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA14/11275	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10975	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/11050	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	shale and carbonate outcrop on site so 10-90	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA13/10525	0	-90	0	magnetic	0	u	u	20350	2000-06-23 18:00:00+02	2000-06-23 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA13/10975	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA15/11875	0	-90	0	magnetic	0	u	u	20350	2000-06-21 18:00:00+02	2000-06-21 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	Hammer 0-43m	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA14/11050	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA15/12100	0	-90	0	magnetic	0	u	u	20350	2000-06-21 18:00:00+02	2000-06-21 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	Terminated due to high ground water flow pushing mud between inner and outer rods and stopping air flow.  Water table at 63m	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA15/12325	0	-90	0	magnetic	0	u	u	20350	2000-06-20 18:00:00+02	2000-06-20 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	Hammer 0-18m clay horizon blocks rods	2012-12-03 17:00:00+01	br	a62436	\N	\N
Yerilla	95YBD010	0	-60	295	grid	295	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Capricorn	WA15/12400	0	-90	0	magnetic	0	u	u	20350	2000-06-20 18:00:00+02	2000-06-20 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	Hammer from 16-22m	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA14/11350	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA14/11425	0	-90	0	magnetic	0	u	u	20350	2000-06-21 18:00:00+02	2000-06-21 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Yerilla	95YBD009	0	-60	295	grid	295	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Capricorn	WA14/11125	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA15/12550	0	-90	0	magnetic	0	u	u	20350	2000-06-20 18:00:00+02	2000-06-20 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA15/12590	0	-90	0	magnetic	0	u	u	20350	2000-06-25 18:00:00+02	2000-06-25 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA13/11125	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA13/11200	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA14/10975	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10750	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10825	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10900	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10525	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10600	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	limonitic shale - after chlorite?	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA15/12440	0	-90	0	magnetic	0	u	u	20350	2000-06-25 18:00:00+02	2000-06-25 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA13/11050	0	-90	0	magnetic	0	u	u	20350	2000-06-22 18:00:00+02	2000-06-22 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	RC00WA002	0	-90	0	magnetic	0	u	u	20350	2000-10-13 18:00:00+02	2000-10-13 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	Blew sample hose at 10m.  Ground water at 40m.  136m hydraulic pump failure on rig	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA14/11500	0	-90	0	magnetic	0	u	u	20350	2000-06-21 18:00:00+02	2000-06-21 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	Outcrop of siltstone in creek at 544193E 7264616N.   So 10 to 110.  Dolerite boulders on drill site	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10450	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA13/10750	0	-90	0	magnetic	0	u	u	20350	2000-06-23 18:00:00+02	2000-06-23 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA13/10825	0	-90	0	magnetic	0	u	u	20350	2000-06-23 18:00:00+02	2000-06-23 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA13/10675	0	-90	0	magnetic	0	u	u	20350	2000-06-23 18:00:00+02	2000-06-23 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10675	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	RC00WA001	0	-60	260	magnetic	260	u	u	20350	2000-10-12 18:00:00+02	2000-10-12 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	Water at 56m.  Two mineralised faults-ferruginised and slightly magnetic	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA10/11200	0	-90	0	magnetic	0	u	u	20350	2000-06-25 18:00:00+02	2000-06-25 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u	Drill site full of quartzite boulders.  Hole drilled into mag anomaly.  Gravel and clays very magnetic 500 -7000 SI Units.  Abandoned due to caving ground	2012-12-03 17:00:00+01	br	a62436	\N	\N
Capricorn	WA12/10300	0	-90	0	magnetic	0	u	u	20350	2000-06-24 18:00:00+02	2000-06-24 18:00:00+02	Drillcorp	Drillcorp	u	u	u	u		2012-12-03 17:00:00+01	br	a62436	\N	\N
Yerilla	95YBD010	30	-57.7	294	grid	294	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD010	60	-56.2	293	grid	293	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD010	90	-55	292	grid	292	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD010	127	-54.7	291.5	grid	291.5	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD010	159.4	-54.7	291	grid	291	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD010	192.1	-54.3	291.5	grid	291.5	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD010	202	-54.3	292	grid	292	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	62	-59.2	292.5	grid	292.5	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	90	-59.2	294	grid	294	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	117	-59	296	grid	296	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	150	-58.4	296	grid	296	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	183.5	-57	293	grid	293	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	210.5	-56.3	290	grid	290	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	245.5	-56.2	290	grid	290	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	273	-56	292	grid	292	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	306	-55.9	291	grid	291	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	342.5	-56	291	grid	291	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
Yerilla	95YBD009	32.1	-59	295	grid	295	u	u	28351	1995-01-09 17:00:00+01	1995-01-09 17:00:00+01	Rio Tinto	Rio Tinto	u	u	u	u		2014-10-30 17:00:00+01	fp	terra_search_db	\N	\N
\.


--
-- PostgreSQL database dump complete
--

