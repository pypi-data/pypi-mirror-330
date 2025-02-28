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
-- Name: elements; Type: TABLE; Schema: ref; Owner: postgres
--
CREATE TABLE ref.elements (
    at_no integer NOT NULL,
    bp_k double precision,
    mp_k double precision,
    density double precision,
    at_wt double precision,
    most_stable_oxidation_state integer,
    covalent_radius double precision,
    at_radius__angstroms double precision,
    first_ip double precision,
    specific_heat_capacity double precision,
    thermal_conductivity double precision,
    electrical_conductivity double precision,
    heat_of_fusion double precision,
    heat_of_vaporization double precision,
    electro_negativity double precision,
    "group" integer,
    "2nd_most_stable_oxidation_state" integer,
    "3rd_most_stable_oxidation_state" integer,
    "4th_most_stable_oxidation_state" integer,
    mg_per_kg_crust double precision,
    mg_per_l_seawater double precision,
    pct_human_body_mass double precision,
    length_of_name integer,
    name text,
    symbol text,
    years_since_discovery text,
    family text,
    orbital text,
    metal_or_nonmetal text,
    portugues_name text
);

ALTER TABLE ref.elements OWNER TO postgres;

--
-- Name: TABLE elements; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON TABLE ref.elements IS 'Reference table listing elements';

--
-- Name: COLUMN elements.at_no; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.at_no IS 'Atomic Number';

--
-- Name: COLUMN elements.bp_k; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.bp_k IS 'Boiling point in Kelvin';

--
-- Name: COLUMN elements.mp_k; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.mp_k IS 'Melting point in Kelvin';

--
-- Name: COLUMN elements.density; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.density IS 'Density';

--
-- Name: COLUMN elements.at_wt; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.at_wt IS 'Atomic weight';

--
-- Name: COLUMN elements.most_stable_oxidation_state; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.most_stable_oxidation_state IS 'Most stabel oxidation state';

--
-- Name: COLUMN elements.covalent_radius; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.covalent_radius IS 'Covalent Radius';

--
-- Name: COLUMN elements.at_radius__angstroms; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.at_radius__angstroms IS 'Atomic radius in angstroms';

--
-- Name: COLUMN elements.first_ip; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.first_ip IS 'First Ionization potential at 0 k in electronvolts';

--
-- Name: COLUMN elements.specific_heat_capacity; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.specific_heat_capacity IS 'Specific heat capacity';

--
-- Name: COLUMN elements.thermal_conductivity; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.thermal_conductivity IS 'Thermal conductivity';

--
-- Name: COLUMN elements.electrical_conductivity; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.electrical_conductivity IS 'Electrical conductivity';

--
-- Name: COLUMN elements.heat_of_fusion; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.heat_of_fusion IS 'Heat of fusion';

--
-- Name: COLUMN elements.heat_of_vaporization; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.heat_of_vaporization IS 'Heat of Vaporization';

--
-- Name: COLUMN elements.electro_negativity; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.electro_negativity IS 'Electro Negativity';

--
-- Name: COLUMN elements."group"; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements. "group" IS 'Group on the periodic table the element belongs to';

--
-- Name: COLUMN elements."2nd_most_stable_oxidation_state"; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements. "2nd_most_stable_oxidation_state" IS 'Second most stable oxidation state';

--
-- Name: COLUMN elements."3rd_most_stable_oxidation_state"; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements. "3rd_most_stable_oxidation_state" IS 'Third most stable oxidation state';

--
-- Name: COLUMN elements."4th_most_stable_oxidation_state"; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements. "4th_most_stable_oxidation_state" IS 'Forth most stable oxidation state';

--
-- Name: COLUMN elements.mg_per_kg_crust; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.mg_per_kg_crust IS 'Miligrams per Kilogram in crust';

--
-- Name: COLUMN elements.mg_per_l_seawater; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.mg_per_l_seawater IS 'Miligrams per litre in seawater';

--
-- Name: COLUMN elements.pct_human_body_mass; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.pct_human_body_mass IS 'Percentage in human body by mass';

--
-- Name: COLUMN elements.length_of_name; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.length_of_name IS 'Lenght of name';

--
-- Name: COLUMN elements.name; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.name IS 'Name of element';

--
-- Name: COLUMN elements.symbol; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.symbol IS 'Element symbol';

--
-- Name: COLUMN elements.years_since_discovery; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.years_since_discovery IS 'Years since discovery';

--
-- Name: COLUMN elements.family; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.family IS 'Elemental family';

--
-- Name: COLUMN elements.orbital; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.orbital IS 'Orbital of the element';

--
-- Name: COLUMN elements.metal_or_nonmetal; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.metal_or_nonmetal IS 'Metal or non-metal ';

--
-- Name: COLUMN elements.portugues_name; Type: COMMENT; Schema: ref; Owner: postgres
--
COMMENT ON COLUMN ref.elements.portugues_name IS 'Portugues Name';

--
-- Name: elements ref_elements_pkey; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.elements
    ADD CONSTRAINT ref_elements_pkey PRIMARY KEY (at_no);

--
-- Name: elements ref_elements_symbol_key; Type: CONSTRAINT; Schema: ref; Owner: postgres
--
ALTER TABLE ONLY ref.elements
    ADD CONSTRAINT ref_elements_symbol_key UNIQUE (symbol);

--
-- Name: TABLE elements; Type: ACL; Schema: ref; Owner: postgres
--
-- GRANT SELECT ON TABLE ref.elements TO fp;

--
-- PostgreSQL database dump complete
--
