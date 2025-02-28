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
-- Data for Name: lab_method; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.lab_method (lab, lab_method_code, element, sample_weight, sample_weight_units, limit_description, det_limit_lower, det_limit_upper, det_limit_units, description, application, price, loaded_by, load_date, o_method) FROM stdin;
genalysis_perth	WEI-21	NA	\N	\N	\N	\N	\N	\N	\N	\N	\N	fp	2013-03-07 17:00:00+01	weigh
amdel_perth	ICPOES	Ag	\N	\N	\N	1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Al	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	As	\N	\N	\N	3	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Ba	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Bi	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Ca	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Cd	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Co	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Cr	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Cu	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Ag	\N	\N	\N	1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Al	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	As	\N	\N	\N	3	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Ba	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Bi	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Ca	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Cd	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Co	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Cr	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Cu	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Fe	\N	\N	\N	100	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	K	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Cr	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Cu	\N	\N	\N	1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Fe	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Mn	\N	\N	\N	1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Mo	\N	\N	\N	0.1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Ni	\N	\N	\N	1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	P	\N	\N	\N	20	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Pb	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Pd	\N	\N	\N	0.05	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Pt	\N	\N	\N	0.05	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Sb	\N	\N	\N	0.05	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Sr	\N	\N	\N	0.05	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Th	\N	\N	\N	0.01	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Ti	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	U	\N	\N	\N	0.01	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	V	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	W	\N	\N	\N	0.1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Zn	\N	\N	\N	1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Fe	\N	\N	\N	100	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	K	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Mg	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Mn	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Mo	\N	\N	\N	3	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Na	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Nb	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Ni	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	P	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Pb	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	S	\N	\N	\N	50	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Sb	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Sr	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Th	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Ti	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Mg	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Mn	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Mo	\N	\N	\N	3	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Na	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Nb	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Ni	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	P	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Pb	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	S	\N	\N	\N	50	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Sb	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Sr	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Th	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Ti	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	U	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Au	\N	\N	\N	0.05	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Ag	\N	\N	\N	0.1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	As	\N	\N	\N	1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Ba	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Bi	\N	\N	\N	0.01	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Cd	\N	\N	\N	0.1	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
genalysis_perth	ICPOES	Co	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	U	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	V	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	W	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Zn	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
amdel_perth	ICPOES	Zr	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	V	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	W	\N	\N	\N	10	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Zn	\N	\N	\N	2	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
analabs_perth	ICPOES	Zr	\N	\N	\N	5	\N	ppm	\N	\N	\N	br	2012-12-03 17:00:00+01	four_acid
\.


--
-- PostgreSQL database dump complete
--

