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
-- __authors__ = ["vlarmet"]
-- __contact__ = "vincent.larmet@apeiron.technology"
-- __date__ = "2024/03/18"
-- __license__ = "AGPLv3"


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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: surv; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE display.display_collar (
    data_set character varying(80) NOT NULL,
    hole_id character varying(40) NOT NULL,
    eoh real,
    planned_eoh real,
    effective_geom public.geometry(CompoundCurveZM, 4326),
    planned_geom public.geometry(CompoundCurveZM, 4326),
    -- same geometries in original (or 3857 if not planar) SRID
    proj_effective_geom public.geometry(CompoundCurveZM),
    proj_planned_geom public.geometry(CompoundCurveZM)
);


--
-- Name: TABLE display_collar; Type: COMMENT; Schema: display; Owner: postgres
--
COMMENT ON TABLE display.display_collar IS 'Table used to provide geometries used only for display. (True geometries are in dh.collar)';

--
-- Name: TABLE display_collar; Type: COMMENT; Schema: display; Owner: postgres
--

COMMENT ON COLUMN display.display_collar.effective_geom IS 'Effective trace shape with length = max(eoh, planned_eoh)';

--
-- Name: TABLE display_collar; Type: COMMENT; Schema: display; Owner: postgres
--

COMMENT ON COLUMN display.display_collar.planned_geom IS 'Planned trace shape with length = max(eoh, planned_eoh)';

--
-- Name: collar dh_collar_hole_id_key; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY display.display_collar
    ADD CONSTRAINT display_collar_hole_id_key UNIQUE (hole_id);

--
-- Name: collar dh_collar_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY display.display_collar
    ADD CONSTRAINT display_collar_pkey PRIMARY KEY (hole_id);

--
-- Name: idx_dh_collar_geom; Type: INDEX; Schema: dh; Owner: postgres
--
CREATE INDEX idx_display_collar_geom ON display.display_collar USING gist (effective_geom);

--
-- Name: sidx_collar_geom_trace; Type: INDEX; Schema: dh; Owner: postgres
--
CREATE INDEX idx_display_collar_planned_geom ON display.display_collar USING gist (planned_geom);

