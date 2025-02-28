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
-- Data for Name: lithology; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.lithology (code, description, data_set, data_set_2, data_set_3, loaded_by, load_date) FROM stdin;
BX	Breccia	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
CLY	Clay	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
GVL	Gravel	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
SHLE	Shale	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
SLST	Siltstone	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
DLST	Dolostone	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
PIST	Pisolite	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
CLCR	Calcrete	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
SND	Sand	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
QZT	Quartzite	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
GO	Gossan	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
SDST	Sandstone	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
DOL	Dolerite	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
MDST	Mudstone	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
QTT	Quartzite	Capricorn	\N	\N	br	2012-12-03 17:00:00+01
\.


--
-- PostgreSQL database dump complete
--

