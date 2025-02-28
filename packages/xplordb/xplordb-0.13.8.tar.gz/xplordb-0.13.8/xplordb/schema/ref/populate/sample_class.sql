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
-- Data for Name: sample_class; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.sample_class (code, description, loaded_by, load_date) FROM stdin;
pulp_lab	A sample that was re-assayed from a pulp sample at the lab	fp	2020-02-13
pxrf_extra	An pXRF analysed sample that was also sampled at a lab	fp	2020-02-13
part_comp	A sample that overlaps a composite sample that was only partly sampled. e.g only 29-30m of composite 25-30m was re-sampled	fp	2020-02-13
au_comp	Gold composite sample (usually overlaps other sampling)	fp	2020-02-13
not_set	\N	fp	2020-02-13
au_part	A gold sample that overlaps a gold composite sample that was only partly sampled. e.g only 29-30m of composite 25-30m was re-sampled	fp	2020-02-13
waiting	Results are awaited	fp	2020-02-13
resample	Samples that have been re-sampled (possibily by another method)	fp	2020-02-13
not_preferred	Result not prefered for some miscellaneous reason. Leave a comment	fp	2020-02-13
comp_resampled	Composite sample that has been resampled at a lesser interval value. e.g. 6m comp resampled at 1m 	fp	2020-02-13
au1m	Gold composite resample or initial 1m sample that does not overlap and has a corresponding pXRF or lab result	fp	2020-02-13
pxrf_dup	Duplicated pxrf result.	fp	2020-02-13
primary_au	1m or composite sample that has been lab assayed for gold only (and no pXRF result) or gold and multi element. No overlapping samples in conjuction with primary is the aim.	fp	2020-02-13
primary	The primary sample - drill or surface sample. No overlapping samples is the aim for drill samples.\n	fp	2020-02-13
\.


--
-- PostgreSQL database dump complete
--

