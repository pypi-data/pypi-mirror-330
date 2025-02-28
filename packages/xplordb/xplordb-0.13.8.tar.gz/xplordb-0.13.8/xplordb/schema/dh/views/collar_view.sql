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

SET standard_conforming_strings = ON;

SELECT
    pg_catalog.set_config('search_path', '', FALSE);

SET check_function_bodies = FALSE;

SET xmloption = content;

SET client_min_messages = warning;

SET row_security = OFF;

--
-- Name: collar_view; Type: VIEW; Schema: dh; Owner: postgres
--
CREATE VIEW dh.collar_view AS SELECT DISTINCT ON (c.hole_id)
    c.data_set,
    c.hole_id,
    c.x,
    c.y,
    c.z,
    c.grid_id,
    c.hole_type,
    s.dip AS dip_collar,
    s.azimuth_grid AS azimuth_grid_collar,
    min(d.date_start) OVER (PARTITION BY hole_id) AS date_start,
    max(d.date_completed) OVER (PARTITION BY hole_id) AS date_completed,
    c.eoh AS max_depth,
    min(d.from_m) FILTER (WHERE ((d.hole_type)::text = 'DDH'::text)) OVER (PARTITION BY d.hole_id) AS precollar,
c.hole_status,
c.survey_method,
c.survey_date,
c.surveyed_by_company,
c.lease_id,
c.prospect,
c.comment,
c.data_source,
c.historic_hole,
c.srid,
c.surveyed_by_person,
c.location_confidence_m,
c.rl_method,
d.parent_hole,
d.program,
string_agg((((d.program)::text || '-'::text) || (d.hole_type)::text), ','::text) OVER (PARTITION BY d.hole_id) AS program_all,
d.company,
d.drilling_company,
d.drill_rig,
d.driller,
public.st_x (c.geom) AS long_wgs84,
public.st_y (c.geom) AS lat_wgs84,
c.ctid,
c.local_grid_east,
c.local_grid_north,
row_number() OVER () AS oid
FROM ((dh.collar c
    LEFT JOIN dh.surv s USING (hole_id))
    LEFT JOIN dh.details d USING (hole_id))
WHERE (s.depth_m = (SELECT min(depth_m) FROM dh.surv WHERE  surv.hole_id=s.hole_id));

ALTER TABLE dh.collar_view OWNER TO postgres;

--
-- PostgreSQL database dump complete
--
