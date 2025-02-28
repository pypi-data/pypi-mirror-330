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
-- Data for Name: lease; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.lease (data_set, lease_id, auth_id, status, stage, grant_date, expire_date, owner, owner_2, owner_3, as_date, load_date, loaded_by, geom) FROM stdin;
Capricorn	E52/1393	\N	Active	Final	1999-04-08 18:00:00+02	2001-04-08 18:00:00+02	Rio Tinto	\N	\N	2000-11-30 17:00:00+01	2012-12-03 17:00:00+01	br	0106000020E610000001000000010300000001000000250000008B80449716605D40F47D4B98AABF38C026FA5086055F5D40F47DFD9AAABF38C0C0334C75F45D5D40F47DAF9DAABF38C0596D4764E35C5D40F47D61A0AABF38C0F3A6B852D25B5D40F47D1EA7AABF38C08D203B41C15A5D40F57D96ADAABF38C0275AAC2FB0595D40F57D53B4AABF38C0279ABD2FB0595D405C648E6D66BB38C0271AE02FB0595D40C24AC92622B738C0265AF12FB0595D40283104E0DDB238C027DA8032B0595D408E173F9999AE38C0271AFF34B0595D40F4FD345255AA38C08DA0DE44C15A5D40F4FD8B4C55AA38C08D209F46C15A5D405BE40B0611A638C0F3A6AF55D25B5D405AE4A70011A638C0582DC064E35C5D405AE443FB10A638C0BFF3C475F45D5D405AE474FA10A638C027BAC986055F5D405AE460F910A638C08C40BD9716605D405AE491F810A638C0F386B3A927615D405AE49AF510A638C058CDA9BB38625D405AE45EF210A638C0BF13A0CD49635D405AE467EF10A638C0261AB6DE5A645D405AE470EC10A638C08CE0BAEF6B655D405BE479E910A638C08C60C9EE6B655D40F4FD2A2F55AA38C08CE0D7ED6B655D408F17217599AE38C08C60E6EC6B655D40273117BBDDB238C027DAF2DB5A645D40273170BCDDB238C0C013EECA49635D402731C9BDDDB238C0C053CECB49635D408E17E77899AE38C0598D84BA38625D408E17997B99AE38C0F2C63AA927615D408E17067E99AE38C08CC0DF9716605D408E17738099AE38C08C00F19716605D40293141C4DDB238C08C40BD9716605D40C14A060B22B738C08D80899716605D405A64CB5166BB38C08B80449716605D40F47D4B98AABF38C0
\.


--
-- PostgreSQL database dump complete
--

