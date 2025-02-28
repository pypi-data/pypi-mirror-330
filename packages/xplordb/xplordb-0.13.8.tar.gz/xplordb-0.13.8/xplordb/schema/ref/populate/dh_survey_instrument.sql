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
-- Data for Name: dh_survey_instrument; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.dh_survey_instrument (code, description, loaded_by, load_date, type) FROM stdin;
unknown	unknown	fp	2020-02-13	\N
na	not applicable	fp	2020-02-13	\N
compass	hand held magnetic compass	fp	2020-02-13	magnetic
Eastman camera	Eastman camera - magnetic readings	fp	2020-02-13	magnetic
eastman singleshot	eastman singleshot - magnetic readings	fp	2020-02-13	magnetic
pathfinder	pathfinder - magnetic readings	fp	2020-02-13	magnetic
ranger	Ranger downhole survey single shot camera - magnetic readings	fp	2020-02-13	magnetic
Reflex Ez-Shot	Reflex Ez-Shot - magnetic readings	fp	2020-02-13	magnetic
REFLEX_EZ_GYRO	Reflex EZ-GYRO north seeking gyro solid state	fp	2020-02-13	gyro north seeking solid state
reflex_gyro	reflex_gyro unknown Reflex relative gyro type	fp	2020-02-13	gyro relative
axis_champ_gyro	Axis Champ north seeking solid state Gyro	fp	2020-02-13	gyro north seeking solid state
NS GYRO	North Seeking Gyro	fp	2020-02-13	gyro north seeking
REFLEX	Reflex unknown model - magntic readings	fp	2020-02-13	magnetic
REFLEX_EZTrac	Reflex Eztrac - magnetic readings	fp	2020-02-13	magnetic
\.


--
-- PostgreSQL database dump complete
--

