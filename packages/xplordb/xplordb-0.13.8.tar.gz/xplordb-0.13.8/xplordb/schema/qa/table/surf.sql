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
-- Name: surf; Type: TABLE; Schema: qa; Owner: postgres
--
CREATE TABLE qa.surf (
    data_set character varying(20) NOT NULL,
    sample_id character varying(50) NOT NULL,
    original_sample character varying(20) NOT NULL,
    qc_type character varying(10) NOT NULL,
    standard_id character varying,
    date_submitted timestamp with time zone,
    comment character varying(100),
    loaded_by character varying(50) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    class character varying(16) NOT NULL
);

ALTER TABLE qa.surf OWNER TO postgres;

--
-- Name: TABLE surf; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON TABLE qa.surf IS 'Quality control table for surface samples';

--
-- Name: COLUMN surf.data_set; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.surf.data_set IS 'Data set for the surface sample quality control information, see ref.data_set';

--
-- Name: COLUMN surf.sample_id; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.surf.sample_id IS 'Sample identification(id) number/ code, , see ref.qc_type for quality control codes';

--
-- Name: COLUMN surf.original_sample; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.surf.original_sample IS 'Sample identification(id) number/ code of the original sample where relevant, e.g. duplicate samples';

--
-- Name: COLUMN surf.qc_type; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.surf.qc_type IS 'Quality control category code, see qc_ref_qc_type';

--
-- Name: COLUMN surf.standard_id; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.surf.standard_id IS 'Standard reference material identification number/ code';

--
-- Name: COLUMN surf.date_submitted; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.surf.date_submitted IS 'The date the quality control item was submitted';

--
-- Name: COLUMN surf.comment; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.surf.comment IS 'Any comment';

--
-- Name: COLUMN surf.loaded_by; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.surf.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: surf qc_surf_sample_id_qc_category_key; Type: CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.surf
    ADD CONSTRAINT qc_surf_sample_id_qc_category_key UNIQUE (sample_id, qc_type);

--
-- Name: surf surf_pkey; Type: CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.surf
    ADD CONSTRAINT surf_pkey PRIMARY KEY (sample_id, qc_type);

--
-- Name: surf qc_surf_data_set_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.surf
    ADD CONSTRAINT qc_surf_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: surf qc_surf_loaded_by_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.surf
    ADD CONSTRAINT qc_surf_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: surf qc_surf_qc_type_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.surf
    ADD CONSTRAINT qc_surf_qc_type_fkey FOREIGN KEY (qc_type) REFERENCES qa.qc_type (code);

--
-- PostgreSQL database dump complete
--
