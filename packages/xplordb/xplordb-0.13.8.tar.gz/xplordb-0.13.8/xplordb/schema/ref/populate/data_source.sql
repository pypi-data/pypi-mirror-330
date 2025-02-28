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
-- Data for Name: data_source; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.data_source (data_set, data_source, file_location, title, author, report_date, comment, loaded_by, load_date, company, pages) FROM stdin;
Capricorn	a62436	capricorn	Final Report for period ending 8 April 2001 E52/1393, Walderberg 1, Capricorn Base Metals Rio Tinto Exploration Pty Limited., Final Report for Period ending 8th April 2001, E52/1393, Waldburg 1, Capricorn Base Metals, Mt Egerton SG50-03, Wstern Australia, Peak Hill Mineral Field.	KD	2000-11-30 17:00:00+01	\N	fp	2013-02-24 17:00:00+01	Rio Tinto	\N
Capricorn	AP1726_200010.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	AP1726_200011.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	AP1730_200014.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	GP1721_90732.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	GP1722_104003.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	GP1722_90732.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	GP1724_104004.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	GP1724_90732.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	ANP1730_200007.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	AP1725_200009.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Capricorn	AP1725_200012.csv	capricorn/assay/	Capricorn Assay Results	LAB	1999-12-31 17:00:00+01	\N	fp	2013-03-10 17:00:00+01	Rio Tinto	\N
Yerilla	terra_search_db	database	Terra Search Western Australian database	ts	2009-12-31 17:00:00+01	\N	fp	2014-10-30 17:00:00+01	Terra Search	\N
Capricorn	SL98787.csv	na	example assay results	u	2003-03-01 17:00:00+01	example assay data	fp	2020-03-05 15:36:25.966948+01	u	\N
Capricorn	field	u	\N	u	2020-04-29 18:00:00+02	\N	fp	2020-04-29 18:00:00+02	\N	\N
\.


--
-- PostgreSQL database dump complete
--

