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
-- Data for Name: dh_survey_method; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.dh_survey_method (code, description, loaded_by, load_date) FROM stdin;
gt   	geophysical tool                                                                                    	fp	2012-04-07 18:00:00+02
g    	gyro                                                                                                	fp	2012-04-07 18:00:00+02
c    	collar                                                                                              	fp	2012-04-07 18:00:00+02
e    	estimate                                                                                            	fp	2012-04-07 18:00:00+02
u    	unknown                                                                                             	fp	2012-04-07 18:00:00+02
gns  	gyro north seeking                                                                                  	fp	2020-03-27 10:14:56.591103+01
gr   	gyro relative                                                                                       	fp	2020-03-27 10:15:26.566094+01
gss  	gyro north seeking solid state                                                                      	fp	2020-03-27 10:15:49.150632+01
dhc  	down hole camera - magnetic                                                                         	fp	2012-04-07 18:00:00+02
\.


--
-- PostgreSQL database dump complete
--

