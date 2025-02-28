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
-- Data for Name: batch; Type: TABLE DATA; Schema: assay; Owner: postgres
--

COPY assay.batch (lab, batch, dispatch_no, lab_received_date, lab_completed_date, lab_sample_prep, validated, validated_by, validated_date, data_source, import_script, lab_sample_count, samples_imported, lab_result_count, result_import, over_range_total, qaqc_total, batch_status, loaded_by, load_date) FROM stdin;
analabs_perth	ANP1730_200007	200007	2000-06-28 18:00:00+02	2000-08-31 18:00:00+02	\N	\N	\N	\N	ANP1730_200007.csv	xdb_im-0.84	124	124	\N	3844	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	AP1730_200014	200014	2000-10-24 18:00:00+02	2000-11-30 17:00:00+01	\N	\N	\N	\N	AP1730_200014.csv	xdb_im-0.84	77	77	\N	2387	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	AP1725_200009	200009	1999-06-28 18:00:00+02	1999-08-31 18:00:00+02	dry, crush to <2mm, riffle split to 3kg, pulverise to 95% <75um in Cr free bowl	\N	\N	\N	AP1725_200009.csv	xdb_im-0.84	10	10	\N	80	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	AP1725_200012	200012	1999-09-28 18:00:00+02	1999-10-31 17:00:00+01	dry, crush to <2mm, riffle split to 3kg, pulverise to 95% <75um in Cr free bowl	\N	\N	\N	AP1725_200012.csv	xdb_im-0.84	12	12	\N	120	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	AP1726_200010	200010	1999-07-28 18:00:00+02	1999-08-31 18:00:00+02	pulverise 3kg split to 95% <75um in Cr free bowl	\N	\N	\N	AP1726_200010.csv	xdb_im-0.84	8	8	\N	48	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	AP1726_200011	200011	1999-07-28 18:00:00+02	1999-08-31 18:00:00+02	pulverise 3kg split to 95% <75um in Cr free bowl	\N	\N	\N	AP1726_200011.csv	xdb_im-0.84	15	15	\N	195	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	GP1721_90732	90732	1999-09-28 18:00:00+02	1999-10-31 17:00:00+01	dry, crush, single stage mix and grind	\N	\N	\N	GP1721_90732.csv	xdb_im-0.84	5	5	\N	15	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	GP1722_104003	104003	1999-09-28 18:00:00+02	1999-10-31 17:00:00+01	dry, crush, single stage mix and grind	\N	\N	\N	GP1722_104003.csv	xdb_im-0.84	27	27	\N	702	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	GP1724_104004	104004	1999-09-28 18:00:00+02	1999-10-31 17:00:00+01	dry, crush, single stage mix and grind	\N	\N	\N	GP1724_104004.csv	xdb_im-0.84	18	18	\N	288	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	GP1724_90732	90732	1999-09-28 18:00:00+02	1999-10-31 17:00:00+01	dry, crush, single stage mix and grind	\N	\N	\N	GP1724_90732.csv	xdb_im-0.84	9	9	\N	63	0	0	Finalized	fp	2013-03-10 17:00:00+01
analabs_perth	GP1722_90732	90732	1999-09-28 18:00:00+02	1999-10-31 17:00:00+01	dry, crush, single stage mix and grind	\N	\N	\N	GP1722_90732.csv	xdb_im-0.84	7	7	\N	35	0	0	Finalized	fp	2013-03-10 17:00:00+01
SL	SL98787	\N	2010-04-07 18:00:00+02	2010-04-27 18:00:00+02	\N	\N	\N	\N	SL98787.csv	sql0.87	60	\N	\N	\N	\N	\N	Finalized	fp	2020-03-05 15:36:38.026308+01
\.


--
-- PostgreSQL database dump complete
--

