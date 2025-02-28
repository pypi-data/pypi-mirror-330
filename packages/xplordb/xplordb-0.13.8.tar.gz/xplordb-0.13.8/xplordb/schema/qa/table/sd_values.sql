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
-- Name: sd_values; Type: TABLE; Schema: qa; Owner: postgres
--
CREATE TABLE qa.sd_values (
    standard_id character varying(20) NOT NULL,
    element character (10) NOT NULL,
    method character varying(20) NOT NULL,
    units character varying(10) NOT NULL,
    expected_value double precision,
    expected_min double precision,
    expected_max double precision,
    expected_sdev double precision,
    n_ double precision,
    cv double precision,
    precision_ double precision,
    cl_95_pct character varying(50),
    data_source character varying(500),
    notes character varying(500),
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    standard_maker character varying(100) NOT NULL,
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    o_method character varying(10)
);

ALTER TABLE qa.sd_values OWNER TO postgres;

--
-- Name: TABLE sd_values; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON TABLE qa.sd_values IS 'Quality control table of standard/ reference material values/ results for drill holes and surface samples';

--
-- Name: COLUMN sd_values.standard_id; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.standard_id IS 'The standard/ reference material identification(id) number/ code';

--
-- Name: COLUMN sd_values.element; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.element IS 'The element the expected value relates to';

--
-- Name: COLUMN sd_values.method; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.method IS 'The laboratory method used to determine the expected value';

--
-- Name: COLUMN sd_values.units; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.units IS 'Units of the expected value';

--
-- Name: COLUMN sd_values.expected_value; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.expected_value IS 'The expected assay result value';

--
-- Name: COLUMN sd_values.expected_min; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.expected_min IS 'The minium expected assay result value';

--
-- Name: COLUMN sd_values.expected_max; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.expected_max IS 'The maxium expected assay result value';

--
-- Name: COLUMN sd_values.expected_sdev; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.expected_sdev IS 'The standard deviation of the sample population';

--
-- Name: COLUMN sd_values.n_; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.n_ IS 'The number of assay results taken';

--
-- Name: COLUMN sd_values.cv; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.cv IS 'The co-variance of the sample population';

--
-- Name: COLUMN sd_values.precision_; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.precision_ IS 'The precision of the sample population';

--
-- Name: COLUMN sd_values.cl_95_pct; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.cl_95_pct IS 'The 95 perectile confidence level of the sample population';

--
-- Name: COLUMN sd_values.data_source; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.data_source IS 'The source of the standard/ reference material values information, see ref.data_source';

--
-- Name: COLUMN sd_values.notes; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.notes IS 'Any notes/ comments';

--
-- Name: COLUMN sd_values.load_date; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN sd_values.standard_maker; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.standard_maker IS 'The company who prepared the standard/ reference material';

--
-- Name: COLUMN sd_values.loaded_by; Type: COMMENT; Schema: qa; Owner: postgres
--
COMMENT ON COLUMN qa.sd_values.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: sd_values sd_values_pkey; Type: CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.sd_values
    ADD CONSTRAINT sd_values_pkey PRIMARY KEY (standard_id, element, method);

--
-- Name: sd_values sd_values_standard_id_key; Type: CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.sd_values
    ADD CONSTRAINT sd_values_standard_id_key UNIQUE (standard_id);

--
-- Name: sd_values qc_sd_values_data_source_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.sd_values
    ADD CONSTRAINT qc_sd_values_data_source_fkey FOREIGN KEY (data_source) REFERENCES ref.data_source (data_source);

--
-- Name: sd_values qc_sd_values_element_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.sd_values
    ADD CONSTRAINT qc_sd_values_element_fkey FOREIGN KEY (element) REFERENCES ref.elements (symbol);

--
-- Name: sd_values qc_sd_values_load_by_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.sd_values
    ADD CONSTRAINT qc_sd_values_load_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: sd_values qc_sd_values_o_method_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.sd_values
    ADD CONSTRAINT qc_sd_values_o_method_fkey FOREIGN KEY (o_method) REFERENCES ref.lab_o_method (code);

--
-- Name: sd_values qc_sd_values_standard_maker_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.sd_values
    ADD CONSTRAINT qc_sd_values_standard_maker_fkey FOREIGN KEY (standard_maker) REFERENCES ref.company (company);

--
-- Name: sd_values qc_sd_values_units_fkey; Type: FK CONSTRAINT; Schema: qa; Owner: postgres
--
ALTER TABLE ONLY qa.sd_values
    ADD CONSTRAINT qc_sd_values_units_fkey FOREIGN KEY (units) REFERENCES ref.units (code);

--
-- PostgreSQL database dump complete
--
