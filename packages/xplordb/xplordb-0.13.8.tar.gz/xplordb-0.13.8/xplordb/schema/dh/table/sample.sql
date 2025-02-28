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
-- Name: sample; Type: TABLE; Schema: dh; Owner: postgres
--
CREATE TABLE dh.sample (
    data_set character varying(50) NOT NULL,
    sample_id character varying(30) NOT NULL,
    hole_id character varying(20) NOT NULL,
    from_m real NOT NULL,
    to_m real NOT NULL,
    weight_total real,
    hole_diameter character varying(10),
    sample_type character varying(10),
    sample_method character varying(50),
    company character varying(100),
    date_sampled timestamp with time zone,
    sampled_by character varying(50),
    comment character varying(100),
    historic_sample_id character varying(20),
    data_source character varying(150) NOT NULL,
    loaded_by character varying(30) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    class character varying(16) NOT NULL,
    geom_trace public.geometry(MultiLineStringZM, 4326),
    CONSTRAINT dh_sample_check_from_to CHECK (((from_m < to_m) AND (from_m >= (0)::double precision)))
);

ALTER TABLE dh.sample OWNER TO postgres;

--
-- Name: TABLE sample; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON TABLE dh.sample IS 'Down hole drill hole sample table';

--
-- Name: COLUMN sample.data_set; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.data_set IS 'Data set for the sample, see ref.data_set';

--
-- Name: COLUMN sample.sample_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.sample_id IS 'Sample Identification(id) number or code, see ref.qc_type for quality control codes';

--
-- Name: COLUMN sample.hole_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.hole_id IS 'Drill hole Identification(id) number/ code, needs to have a match in dh.dh_collars.hole_id';

--
-- Name: COLUMN sample.from_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.from_m IS 'Starting distance in metres(m) down the drill hole from the collar the sample was taken';

--
-- Name: COLUMN sample.to_m; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.to_m IS 'Ending distance in metres(m) down the drill hole from the collar the sample was taken';

--
-- Name: COLUMN sample.weight_total; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.weight_total IS 'Weight of the total drill sample, typically weighed in the field';

--
-- Name: COLUMN sample.hole_diameter; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.hole_diameter IS 'Diameter of drill core in mm';

--
-- Name: COLUMN sample.sample_type; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.sample_type IS 'Type of sample taken see ref.sample_type e.g. half core, RC composite';

--
-- Name: COLUMN sample.sample_method; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.sample_method IS 'Method used to take sample see ref.sample_method';

--
-- Name: COLUMN sample.company; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.company IS 'Exploration or Mining company that took the sample see ref.company';

--
-- Name: COLUMN sample.date_sampled; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.date_sampled IS 'Date the sample was taken';

--
-- Name: COLUMN sample.sampled_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.sampled_by IS 'The person who took the sample, see ref.person';

--
-- Name: COLUMN sample.comment; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.comment IS 'Any comment';

--
-- Name: COLUMN sample.historic_sample_id; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.historic_sample_id IS 'A previous Sample Identification(id) number or code that was used for the sample ';

--
-- Name: COLUMN sample.data_source; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.data_source IS 'The source of the information for the sample, ref.data_source';

--
-- Name: COLUMN sample.loaded_by; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN sample.load_date; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN sample.class; Type: COMMENT; Schema: dh; Owner: postgres
--
COMMENT ON COLUMN dh.sample.class IS 'Sample class, see ref.sample-class';

--
-- Name: sample dh_sample_pkey; Type: CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_pkey PRIMARY KEY (sample_id);

--
-- Name: dh_sample_hole_id_interval_idx; Type: INDEX; Schema: dh; Owner: postgres
--
CREATE INDEX dh_sample_hole_id_interval_idx ON dh.sample USING btree (hole_id, from_m, to_m);



--
-- Name: sample dh_sample_class_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_class_fkey FOREIGN KEY (class) REFERENCES ref.sample_class (code);

--
-- Name: sample dh_sample_company_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_company_fkey FOREIGN KEY (company) REFERENCES ref.company (company);

--
-- Name: sample dh_sample_data_set_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_data_set_fkey FOREIGN KEY (data_set) REFERENCES ref.data_sets (data_set);

--
-- Name: sample dh_sample_data_source_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: sample dh_sample_hole_id_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_hole_id_fkey FOREIGN KEY (hole_id) REFERENCES dh.collar (hole_id);

--
-- Name: sample dh_sample_loaded_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: sample dh_sample_sample_method_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_sample_method_fkey FOREIGN KEY (sample_method) REFERENCES ref.sample_method (code);

--
-- Name: sample dh_sample_sample_type_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_sample_type_fkey FOREIGN KEY (sample_type) REFERENCES ref.sample_type (code);

--
-- Name: sample dh_sample_sampled_by_fkey; Type: FK CONSTRAINT; Schema: dh; Owner: postgres
--
ALTER TABLE ONLY dh.sample
    ADD CONSTRAINT dh_sample_sampled_by_fkey FOREIGN KEY (sampled_by) REFERENCES ref.person (code);

--
-- Name: TABLE sample; Type: ACL; Schema: dh; Owner: postgres
--
-- GRANT SELECT ON TABLE dh.sample TO fp;

--
-- PostgreSQL database dump complete
--
