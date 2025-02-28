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
----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION display.display_trace ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $function$
BEGIN
    
        PERFORM display.display_planned_trace (NEW.data_set, NEW.hole_id);
        PERFORM display.display_effective_trace (NEW.data_set, NEW.hole_id);
    RETURN NEW;
END;
$function$
