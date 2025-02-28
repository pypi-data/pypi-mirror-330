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
-- Data for Name: lab; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.lab (lab_code, lab_company, lab_location, lab_address, lab_email, lab_phone, lab_fax, loaded_by, load_date, account_no) FROM stdin;
analabs_perth	Analabs	Perth	\N	\N	\N	\N	br	2012-12-03 17:00:00+01	\N
amdel_perth	Amdel Laboratories 	Perth	\N	\N	\N	\N	br	2012-12-03 17:00:00+01	\N
genalysis_perth	Genalysis Laboratory Services	Perth	\N	\N	\N	\N	br	2012-12-03 17:00:00+01	\N
gen_kal	Genalysis	Kalgoorlie	\N	\N	\N	\N	fp	2010-09-29 18:00:00+02	\N
amd_kal	Amdel	Kalgoorlie	\N	\N	\N	\N	fp	2010-10-11 18:00:00+02	\N
gen_kal_perth	Genalysis	Sample prep Kal, anaysis Perth	\N	\N	\N	\N	fp	2010-11-09 17:00:00+01	\N
as_kal	Analytical Services (WA) Pty Ltd	Kalgoorlie	\N	\N	\N	\N	fp	2010-11-09 17:00:00+01	\N
minlab	Minlab	u	\N	\N	\N	\N	fp	2010-11-09 17:00:00+01	\N
gen_perth	Genalysis	Perth	\N	\N	\N	\N	fp	2010-11-10 17:00:00+01	\N
KI	King Island	King Island	\N	\N	\N	\N	fp	2012-05-15 18:00:00+02	\N
u	Unknown	u	\N	\N	\N	\N	fp	2010-11-09 17:00:00+01	\N
BR	ALS	Brisbane	ALS Brisbane, 32 Shand Street, Stafford, QLD 4053.	\N	+61 7 3243 7222	\N	fp	2012-01-03 17:00:00+01	PEEEXP
OR	ALS	Orange	ALS Orange, 10 Leewood Drive, Orange, NSW 2800.	incoming.orange@alsglobal.com	+61 2 6393 1100	+61 2 6393 1111	fp	2012-01-03 17:00:00+01	PEEEXP
PH	ALS	Perth	ALS Perth, 79 Distinction Road, Wangara, WA 6065.	\N	+61 8 9406 9200	\N	fp	2012-05-21 18:00:00+02	PEEEXP
TV	ALS	u	\N	\N	\N	\N	fp	2012-04-30 18:00:00+02	PEEEXP
VA	ALS	Vancouver?	\N	\N	\N	\N	fp	2012-05-22 18:00:00+02	PEEEXP
as_perth	Analytical Services (WA) Pty Ltd	Perth	Analytical Services Perth, 19 Augusta St, Willetton, Western Australia	\N	\N	\N	fp	2010-11-02 17:00:00+01	\N
srl_perth	Standard and Reference Laboratories	Perth	SRL Perth, 59 Crocker Drive, Malaga, Perth, Western Australia 6090	ben@standardandreference.com	+61 8 9249 1981	+61 8 9249 1801	fp	2010-12-01 17:00:00+01	\N
INT_Perth	Intertek	Perth	\N	\N	\N	\N	fp	2013-06-13 18:00:00+02	\N
Genalysis	Genalysis	u	\N	\N	\N	\N	fp	2013-06-03 18:00:00+02	\N
Analytical Services	Analytical Services	u	\N	\N	\N	\N	fp	2013-06-03 18:00:00+02	\N
unknown	unknown	u	\N	\N	\N	\N	fp	2013-06-03 18:00:00+02	\N
KA	ALS	Kalgoorlie	ALS Kalgoorlie, 5 Keogh Way, Kalgoorlie, WA 6430.	\N	+61 8 9021 1457	\N	fp	2011-06-07 18:00:00+02	\N
FE	ALS	Perth	Iron ore technical centre, 26 Rigali Way, Wangara, WA	\N	\N	\N	fp	2014-07-22 18:00:00+02	\N
WM	SGS	Perth	28 Reid Road, Perth Airport, Perth, Western Australia 6105	\N	+61 8 9373 3500	+61 8 9373 3556	fp	2016-06-15 18:00:00+02	\N
SGS	SGS	u	\N	\N	\N	\N	fp	2016-06-15 18:00:00+02	\N
comlabs	Comlabs Pty Ltd	Adelaide, South Australia	\N	\N	\N	\N	fp	2017-04-03 18:00:00+02	\N
amd	Amdel	u	\N	\N	\N	\N	fp	2017-04-04 18:00:00+02	\N
AAL	Australian Assay Laboratories	Orange	\N	\N	\N	\N	fp	2017-04-04 18:00:00+02	\N
ALS	ALS	u	\N	\N	\N	\N	fp	2013-06-03 18:00:00+02	\N
WY	SGS	West Wyalong	Lot 9 Gelling Street (off Showgrd), West Wyalong, New South Wales, Australia, 2671	\N	+61 2 6972 1507	+61 2 6972 0911	fp	2016-06-15 18:00:00+02	\N
SL	u	u	\N	\N	\N	\N	fp	2020-03-05 11:14:42.207159+01	\N
\.


--
-- PostgreSQL database dump complete
--

