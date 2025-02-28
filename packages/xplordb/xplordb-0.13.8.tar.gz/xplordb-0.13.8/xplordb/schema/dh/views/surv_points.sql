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
-- Name: surv_points; Type: VIEW; Schema: dh; Owner: postgres
--
CREATE VIEW dh.surv_points AS
SELECT
    row_number() OVER () AS row_number,
    st.data_set,
    surv_dump.hole_id,
    surv_dump.m,
    st.dip,
    st.azimuth,
    st.azimuth_type,
    st.azimuth_grid,
    st.dh_survey_method_dip,
    st.dh_survey_method_azimuth,
    st.srid,
    st.date_surveyed_dip,
    st.date_surveyed_azimuth,
    st.dh_survey_company_dip,
    st.dh_survey_company_azimuth,
    st.dh_survey_operator_dip,
    st.dh_survey_operator_azimuth,
    st.dh_survey_instrument_dip,
    st.dh_survey_instrument_azimuth,
    st.comment,
    st.load_date,
    st.loaded_by,
    st.data_source,
    st.local_grid_azimuth,
    st.local_grid_id,
    surv_dump.points
FROM
    dh.surv st,
    LATERAL (
        SELECT
            surv.hole_id,
            (public.st_m ((surv.surv_points).geom))::real AS m,
            (surv.surv_points).geom AS points
        FROM (
            SELECT
                collar.hole_id,
                public.st_dumppoints (collar.geom_trace) AS surv_points
            FROM
                dh.collar) surv) surv_dump
WHERE (((surv_dump.hole_id)::text = (st.hole_id)::text)
    AND (surv_dump.m = st.depth_m));

ALTER TABLE dh.surv_points OWNER TO postgres;

--
-- PostgreSQL database dump complete
--
