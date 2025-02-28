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
-- Data for Name: minerals; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.minerals (code, description, type, loaded_by, load_date) FROM stdin;
ad	adularia	mineral	fp	2012-04-09 18:00:00+02
alb	albite	mineral	fp	2012-04-09 18:00:00+02
cy	clay	mineral	fp	2012-04-09 18:00:00+02
hm	hematite	mineral	fp	2012-04-09 18:00:00+02
jsp	jasperoid	mineral	fp	2012-04-09 18:00:00+02
ta	talc	mineral and alteration	fp	2012-04-09 18:00:00+02
si	silicification	alteration	fp	2012-04-09 18:00:00+02
fe	iron oxide	mineral	fp	2012-04-09 18:00:00+02
pro	propylitic	alteration	fp	2012-04-09 18:00:00+02
arg	argillic	alteration	fp	2012-04-09 18:00:00+02
sil	silicic	alteration	fp	2012-04-09 18:00:00+02
pot	potassic	alteration	fp	2012-04-09 18:00:00+02
skn	skarn	alteration	fp	2012-04-09 18:00:00+02
w	weak	alteration strength	fp	2012-04-09 18:00:00+02
m	moderate	alteration strength	fp	2012-04-09 18:00:00+02
s	strong	alteration strength	fp	2012-04-09 18:00:00+02
apy	arsenopyrite	mineral	fp	2012-04-09 18:00:00+02
az	azurite	mineral	fp	2012-04-09 18:00:00+02
bn	bornite	mineral	fp	2012-04-09 18:00:00+02
cer	cerussite	mineral	fp	2012-04-09 18:00:00+02
cc	chalcocite	mineral	fp	2012-04-09 18:00:00+02
cpy	chalcopyrite	mineral	fp	2012-04-09 18:00:00+02
cup	cuprite	mineral	fp	2012-04-09 18:00:00+02
mal	malachite	mineral	fp	2012-04-09 18:00:00+02
mly	molybdenite	mineral	fp	2012-04-09 18:00:00+02
po	phyrotite	mineral	fp	2012-04-09 18:00:00+02
py	pyrite	mineral	fp	2012-04-09 18:00:00+02
ga	galena	mineral	fp	2012-04-09 18:00:00+02
sp	sphalerite	mineral	fp	2012-04-09 18:00:00+02
stb	stibnite	mineral	fp	2012-04-09 18:00:00+02
bt	biotite	mineral	fp	2012-04-09 18:00:00+02
carb	carbonate	mineral	fp	2012-04-09 18:00:00+02
ca	calcite	mineral	fp	2012-04-09 18:00:00+02
cl	chlorite	mineral	fp	2012-04-09 18:00:00+02
ep	epidote	mineral	fp	2012-04-09 18:00:00+02
gnt	garnet	mineral	fp	2012-04-09 18:00:00+02
mn	manganese	mineral	fp	2012-04-09 18:00:00+02
feld	feldspar	mineral	fp	2012-04-09 18:00:00+02
lmn	limonite	mineral	fp	2012-04-09 18:00:00+02
mg	magnetite	mineral	fp	2012-04-09 18:00:00+02
ms	muscovite	mineral	fp	2012-04-09 18:00:00+02
pl	plagioclase	mineral	fp	2012-04-09 18:00:00+02
qz	quartz	mineral	fp	2012-04-09 18:00:00+02
ser	sericite	mineral	fp	2012-04-09 18:00:00+02
sd	siderite	mineral	fp	2012-04-09 18:00:00+02
\.


--
-- PostgreSQL database dump complete
--

