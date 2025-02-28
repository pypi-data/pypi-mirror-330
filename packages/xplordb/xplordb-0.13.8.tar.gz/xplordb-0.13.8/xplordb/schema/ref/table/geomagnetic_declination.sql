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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: geomagnetic_declination; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.geomagnetic_declination (
    lat real NOT NULL,
    lon real NOT NULL,
    rl_km real NOT NULL,
    date timestamp with time zone NOT NULL,
    declination real,
    grid_convergence real,
    change_to_grid real,
    data_set character varying(50) NOT NULL,
    data_source character varying(100)
);

ALTER TABLE ref.geomagnetic_declination OWNER TO postgres;

--
-- Name: TABLE geomagnetic_declination; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.geomagnetic_declination IS 'Reference table listing geomagnetic declination at different locations/ projects/ data sets';

--
-- Name: COLUMN geomagnetic_declination.lat; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.geomagnetic_declination.lat IS 'Latitude of the geomagnetic declination';

--
-- Name: COLUMN geomagnetic_declination.lon; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.geomagnetic_declination.lon IS 'Longitude of the geomagnetic declination';

--
-- Name: COLUMN geomagnetic_declination.rl_km; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.geomagnetic_declination.rl_km IS 'The relative level from mean sea level in kilometres of the geomagnetic declination';

--
-- Name: COLUMN geomagnetic_declination.date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.geomagnetic_declination.date IS 'The date of the geomagnetic declination';

--
-- Name: COLUMN geomagnetic_declination.declination; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.geomagnetic_declination.declination IS 'The geomagnetic declination value';

--
-- Name: COLUMN geomagnetic_declination.grid_convergence; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.geomagnetic_declination.grid_convergence IS 'Grid convergence of the geomagnetic declination';

--
-- Name: COLUMN geomagnetic_declination.change_to_grid; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.geomagnetic_declination.change_to_grid IS 'The degrees required to change the geomagnetic declination to a grid value';

--
-- Name: COLUMN geomagnetic_declination.data_set; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.geomagnetic_declination.data_set IS 'Data set for the geomagnetic declination information, see ref.data_set';

--
-- Name: geomagnetic_declination geomagnetic_declination_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.geomagnetic_declination
    ADD CONSTRAINT geomagnetic_declination_pkey PRIMARY KEY (lat, lon, rl_km, date);

--
-- Name: geomagnetic_declination ref_geomagnetic_declination_lat_lon_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.geomagnetic_declination
    ADD CONSTRAINT ref_geomagnetic_declination_lat_lon_key UNIQUE (lat, lon, date);

--
-- Name: geomagnetic_declination ref_geomagnetic_declination_data_set_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.geomagnetic_declination
    ADD CONSTRAINT ref_geomagnetic_declination_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: geomagnetic_declination ref_geomagnetic_declination_data_source_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.geomagnetic_declination
    ADD CONSTRAINT ref_geomagnetic_declination_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: TABLE geomagnetic_declination; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.geomagnetic_declination TO fp;

--
-- PostgreSQL database dump complete
--
