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

CREATE OR REPLACE FUNCTION dh.trace_update_tables_hole_trigger ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $function$
DECLARE
    -- mustache parameters to define tables to be updated
    tablelist text:='{{geom_trace_tables}}';
    table_val text:='';
BEGIN
    IF NEW.hole_id IS NOT NULL THEN
        -- if mustache parameters not set use all tables
        IF length(tablelist) = 0 THEN
    	    tablelist = 'alteration,core_recovery,details,lith,minerals,oxidation,sample,sample_image,sample_quality,sample_weight,sg,vein';
        END IF;
	    FOREACH table_val IN ARRAY string_to_array(tablelist, ',')   LOOP
    		EXECUTE 'update dh.' || table_val || ' u set geom_trace = sq.geom_interval from (select s.hole_id, from_m, to_m, public.ST_LocateBetween(public.ST_CurveToLine(c.geom_trace), from_m, to_m) as geom_interval from  dh.' || table_val || ' s, dh.collar c where (c.hole_id = s.hole_id) ) as sq where (u.hole_id = sq.hole_id and u.from_m = sq.from_m and u.to_m = sq.to_m ) and u.hole_id = ' || quote_literal(NEW.hole_id) || ' ';
        END LOOP;
    END IF;
    RETURN NEW;
END;
$function$
