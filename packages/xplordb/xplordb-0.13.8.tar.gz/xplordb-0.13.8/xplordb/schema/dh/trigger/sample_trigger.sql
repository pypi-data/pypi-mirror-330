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
-- Name: sample check_from_m_dh_sample; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_from_m_dh_sample
    BEFORE INSERT OR UPDATE OF from_m ON dh.sample
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_from_m ();

--
-- Name: sample check_to_m_dh_sample; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER check_to_m_dh_sample
    BEFORE INSERT OR UPDATE OF to_m ON dh.sample
    FOR EACH ROW
    EXECUTE FUNCTION dh.check_to_m ();

--
-- Name: sample trace_row_sample; Type: TRIGGER; Schema: dh; Owner: postgres
--
CREATE TRIGGER trace_row_sample
    AFTER INSERT OR UPDATE OF hole_id,
    from_m,
    to_m ON dh.sample
    FOR EACH ROW
    EXECUTE FUNCTION dh.trace_update_row ();