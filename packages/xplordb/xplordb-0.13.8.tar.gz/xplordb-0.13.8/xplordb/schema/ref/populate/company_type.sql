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
-- Data for Name: company_type; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.company_type (company_type, description, loaded_by, load_date) FROM stdin;
geological consulting	\N	fp	2020-02-13
exploration	\N	fp	2020-02-13
QAQC material	\N	fp	2020-02-13
unknown	\N	fp	2020-02-13
government	\N	fp	2020-02-13
transport	\N	fp	2020-02-13
laboratory	\N	fp	2020-02-13
survey	\N	fp	2020-02-13
geological consultants	\N	fp	2020-02-13
drilling	\N	fp	2020-02-13
database management	\N	fp	2020-02-13
mining	\N	fp	2020-02-13
downhole survey	\N	fp	2020-02-13
geophysics contractor	\N	fp	2020-02-13
exploration contractor	\N	fp	2020-02-13
\.


--
-- PostgreSQL database dump complete
--

