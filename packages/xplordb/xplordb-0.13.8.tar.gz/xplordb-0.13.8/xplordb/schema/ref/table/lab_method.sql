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
-- Name: lab_method; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.lab_method (
    lab character varying(20) NOT NULL,
    lab_method_code character varying(20) NOT NULL,
    element character varying(10) NOT NULL,
    sample_weight real,
    sample_weight_units character varying(5),
    limit_description character varying(50),
    det_limit_lower real,
    det_limit_upper real,
    det_limit_units character varying(10),
    description character varying(500),
    application character varying(500),
    price character varying(100),
    loaded_by character varying(5) DEFAULT "current_user" () NOT NULL,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    o_method character varying(10)
);

ALTER TABLE ref.lab_method OWNER TO postgres;

--
-- Name: TABLE lab_method; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.lab_method IS 'Reference table listing laboratory methods';

--
-- Name: COLUMN lab_method.lab; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.lab IS 'Code for laboratory, see ref.lab';

--
-- Name: COLUMN lab_method.lab_method_code; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.lab_method_code IS 'Laboratory method code';

--
-- Name: COLUMN lab_method.element; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.element IS 'Element the method relates to';

--
-- Name: COLUMN lab_method.sample_weight; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.sample_weight IS 'The weight(mass) of the analysed portion of the sample';

--
-- Name: COLUMN lab_method.sample_weight_units; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.sample_weight_units IS 'Unit of the sample weight(mass)';

--
-- Name: COLUMN lab_method.limit_description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.limit_description IS 'Description of the method limits, e.g. ore grade';

--
-- Name: COLUMN lab_method.det_limit_lower; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.det_limit_lower IS 'The lower limit of the method';

--
-- Name: COLUMN lab_method.det_limit_upper; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.det_limit_upper IS 'The upper limit of the method';

--
-- Name: COLUMN lab_method.det_limit_units; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.det_limit_units IS 'Units of the upper and lower limits';

--
-- Name: COLUMN lab_method.description; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.description IS 'Description of the method';

--
-- Name: COLUMN lab_method.application; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.application IS 'What the method can be used for';

--
-- Name: COLUMN lab_method.price; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.price IS 'The price/ cost of the method per sample';

--
-- Name: COLUMN lab_method.loaded_by; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: COLUMN lab_method.load_date; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.lab_method.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: lab_method lab_method_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab_method
    ADD CONSTRAINT lab_method_pkey PRIMARY KEY (lab, lab_method_code, element);

--
-- Name: lab_method ref_lab_method_lab_method_code_element_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab_method
    ADD CONSTRAINT ref_lab_method_lab_method_code_element_key UNIQUE (lab, lab_method_code, element);

--
-- Name: lab_method lab_method_lab_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab_method
    ADD CONSTRAINT lab_method_lab_fkey FOREIGN KEY (lab) REFERENCES ref.lab (lab_code) NOT VALID;

--
-- Name: lab_method lab_method_o_method_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab_method
    ADD CONSTRAINT lab_method_o_method_fkey FOREIGN KEY (o_method) REFERENCES ref.lab_o_method (code) NOT VALID;

--
-- Name: lab_method ref_lab_method_loaded_by_fkey; Type: FK CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.lab_method
    ADD CONSTRAINT ref_lab_method_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: TABLE lab_method; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.lab_method TO fp;

--
-- PostgreSQL database dump complete
--
