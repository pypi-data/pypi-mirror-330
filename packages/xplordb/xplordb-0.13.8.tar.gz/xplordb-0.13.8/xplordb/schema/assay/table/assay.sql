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
-- Name: assay; Type: TABLE; Schema: assay; Owner: postgres
--
CREATE TABLE assay.assay (
    sample_id character varying(25) NOT NULL,
    sample_prep character varying(20),
    digest character varying(20),
    lab_method character varying(30) NOT NULL,
    lab_element character varying(20) NOT NULL,
    element character varying(20) NOT NULL,
    repeat integer NOT NULL,
    preferred integer NOT NULL,
    o_method character varying(20),
    unit character varying(10) NOT NULL,
    ar character varying(20) NOT NULL,
    arr numrange,
    lab character varying(20) NOT NULL,
    batch character varying(25) NOT NULL,
    lower_limit real,
    upper_limit real,
    load_date timestamp with time zone DEFAULT ('now'::text) ::timestamp with time zone NOT NULL,
    loaded_by character varying(50) DEFAULT "current_user" () NOT NULL,
    id integer NOT NULL
);

ALTER TABLE assay.assay OWNER TO postgres;

--
-- Name: TABLE assay; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON TABLE assay.assay IS 'Assay table for drill hole and surface samples. See assay.import function for importing lab data from files';

--
-- Name: COLUMN assay.sample_id; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.sample_id IS 'Sample identification(id) number/ code for the drill sample, see ref.qc_type for quality control codes';

--
-- Name: COLUMN assay.sample_prep; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.sample_prep IS 'The sample preperation code(s) used for the sample';

--
-- Name: COLUMN assay.digest; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.digest IS 'The digest used on the sample';

--
-- Name: COLUMN assay.lab_method; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.lab_method IS 'Sample assay method, see ref.lab_method and ref.lab_method_code';

--
-- Name: COLUMN assay.lab_element; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.lab_element IS 'The element the assay result relates to as described by the laboratory, see ref.lab_element';

--
-- Name: COLUMN assay.element; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.element IS 'The element the assay result relates to, standardised to xplordb, the first assay result will always be [element]1 e.g. Au1 subsequent assay results will be [element]2, [element]3 etc. e.g Au2, Au3 etc. See ref.element';

--
-- Name: COLUMN assay.repeat; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.repeat IS 'Assay repeat code, 0 - result, 1 - 1st repeat, 2 - 2nd repeat';

--
-- Name: COLUMN assay.preferred; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.preferred IS 'Assay preferred code, see ref.preferred. 1 = prefered, 0 (zero) = over range, 2 = resample, 3 = 2nd resample';

--
-- Name: COLUMN assay.o_method; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.o_method IS 'The assay method used, standardised to xplordb ';

--
-- Name: COLUMN assay.unit; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.unit IS 'Units of the assay result, see ref.units';

--
-- Name: COLUMN assay.ar; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.ar IS 'Assay result as reported by the laboratory';

--
-- Name: COLUMN assay.arr; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.arr IS 'Assay result as a number';

--
-- Name: COLUMN assay.lab; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.lab IS 'Code for laboratory that reported the (assay) result, see ref.lab';

--
-- Name: COLUMN assay.batch; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.batch IS 'The laboratory batch number/ code';

--
-- Name: COLUMN assay.lower_limit; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.lower_limit IS 'The lower limit of the laboratory method';

--
-- Name: COLUMN assay.upper_limit; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.upper_limit IS 'The upper limit of the laboratory method';

--
-- Name: COLUMN assay.load_date; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.load_date IS 'The date the data was loaded into xplordb';

--
-- Name: COLUMN assay.loaded_by; Type: COMMENT; Schema: assay; Owner: postgres
--
COMMENT ON COLUMN assay.assay.loaded_by IS 'The person who loaded the data into xplordb, see ref.person';

--
-- Name: assay_id_seq; Type: SEQUENCE; Schema: assay; Owner: postgres
--
CREATE SEQUENCE assay.assay_id_seq
    AS integer START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE assay.assay_id_seq OWNER TO postgres;

--
-- Name: assay_id_seq; Type: SEQUENCE OWNED BY; Schema: assay; Owner: postgres
--
ALTER SEQUENCE assay.assay_id_seq OWNED BY assay.assay.id;

--
-- Name: assay id; Type: DEFAULT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.assay
    ALTER COLUMN id SET DEFAULT nextval('assay.assay_id_seq'::regclass);

--
-- Name: assay_result_num_idx; Type: INDEX; Schema: assay; Owner: postgres
--
CREATE INDEX assay_result_num_idx ON assay.assay USING gist (arr);

--
-- Name: assay assay_batch_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.assay
    ADD CONSTRAINT assay_batch_fkey FOREIGN KEY (batch) REFERENCES assay.batch (batch);

--
-- Name: assay assay_lab_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.assay
    ADD CONSTRAINT assay_lab_fkey FOREIGN KEY (lab) REFERENCES ref.lab (lab_code);

--
-- Name: assay assay_lab_method_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.assay
    ADD CONSTRAINT assay_lab_method_fkey FOREIGN KEY (lab_method) REFERENCES ref.lab_method_code (lab_method_code);

--
-- Name: assay assay_loaded_by_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.assay
    ADD CONSTRAINT assay_loaded_by_fkey FOREIGN KEY (loaded_by) REFERENCES ref.person (code);

--
-- Name: assay assay_o_method_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.assay
    ADD CONSTRAINT assay_o_method_fkey FOREIGN KEY (o_method) REFERENCES ref.lab_o_method (code);

--
-- Name: assay assay_preferred_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.assay
    ADD CONSTRAINT assay_preferred_fkey FOREIGN KEY (preferred) REFERENCES ref.preferred (code);

--
-- Name: assay assay_unit_fkey; Type: FK CONSTRAINT; Schema: assay; Owner: postgres
--
ALTER TABLE ONLY assay.assay
    ADD CONSTRAINT assay_unit_fkey FOREIGN KEY (unit) REFERENCES ref.units (code);

--
-- PostgreSQL database dump complete
--
