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
-- Data for Name: event; Type: TABLE DATA; Schema: dh; Owner: postgres
--

COPY dh.event (data_set, hole_id, event, depth_m, data_source, comment, logged_by, logged_date, loaded_by, load_date) FROM stdin;
Capricorn	WA15/12590	tofr	49	a62436	very hard interface of fresh rock.  Hole terminated due to high waterflow	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	RC00WA001	boco	31.5	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	RC00WA001	tofr	35	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	RC00WA002	boco	45	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	RC00WA002	tofr	56	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA10/11200	boco	59	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA12/10825	boco	30	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA13/10525	boco	69	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA13/10600	tofr	66	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA13/10750	tofr	75	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA13/10675	boco	75	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA13/10975	boco	30	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA13/11200	boco	30	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA14/11050	boco	55	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA14/10975	boco	50	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA14/11050	tofr	66	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA15/11875	tofr	75	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA14/11500	boco	30	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA15/12100	tofr	67	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA15/12325	tofr	75	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA15/12440	tofr	66	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA15/12440	boco	57	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
Capricorn	WA15/12625	boco	39	a62436	\N	kd	2002-06-30 18:00:00+02	br	2012-12-03 17:00:00+01
\.


--
-- PostgreSQL database dump complete
--

