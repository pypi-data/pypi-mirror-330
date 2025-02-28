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
-- Data for Name: sg_method; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.sg_method (code, description, loaded_by, load_date) FROM stdin;
immersion	immersion on non porous core, no coating or wax used	fp	2020-02-13
OA-GRA08	ALS. Specific Gravity on solid objects. Determined by weighing a sample in air and in water, and it is reported as a ratio between the density of the sample and the density of water.	fp	2020-02-13
OA-GRA08b	ALS. Specific Gravity on solid objects. A prepared sample (3.0g) is weighed into an empty pycnometer, which is then filled with a solvent (methanol) and then weighed. SG = (Weight of Sample (g)/Weight	fp	2020-02-13
OA-GRA08f	ALS. Specific Gravity on solid objects. A prepared sample (3.0g) is weighed into an empty pycnometer, which is then filled with a solvent (ethanol) and then weighed	fp	2020-02-13
\.


--
-- PostgreSQL database dump complete
--

