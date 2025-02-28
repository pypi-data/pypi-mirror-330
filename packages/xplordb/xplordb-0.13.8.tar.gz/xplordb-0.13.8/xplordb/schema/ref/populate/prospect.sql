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
-- Data for Name: prospect; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.prospect (data_set, prospect, description, company, active, active_date_start, active_date_end, loaded_by, load_date, label, resource, commodity, label_x, label_y, label_font, geom, significance, drill_code, "group", geom_area) FROM stdin;
Yerilla	Bull Terrier	\N	Rio Tinto	f	\N	\N	fp	2014-10-31	Bull Terrier	\N	\N	\N	\N	\N	0101000020E61000003576E277307B5E40AFE9D450507D3DC0	\N	\N	Western Australia	0103000020E61000000100000005000000D13A0328A37B5E40AFE9D450507D3DC03576E277307B5E401EFC57111B7F3DC099B1C1C7BD7A5E40AFE9D450507D3DC03576E277307B5E4040D75190857B3DC0D13A0328A37B5E40AFE9D450507D3DC0
Capricorn	Waldburg		Rio Tinto	f	1999-04-08 18:00:00+02	2001-04-08 18:00:00+02	fp	2020-02-06	Waldburg			\N	\N	\N	0101000020E610000089D949F7885C5D4053EB894C2DB638C0	\N		Western Australia	0103000020E61000000100000005000000746A431FFC595D401A2DC6031ABE38C057CD90A2015A5D4013E1498540AE38C087939A2A115F5D40FDC9DE6A14AE38C0A4304DA70B5F5D403144311E46BE38C0746A431FFC595D401A2DC6031ABE38C0
\.


--
-- PostgreSQL database dump complete
--

