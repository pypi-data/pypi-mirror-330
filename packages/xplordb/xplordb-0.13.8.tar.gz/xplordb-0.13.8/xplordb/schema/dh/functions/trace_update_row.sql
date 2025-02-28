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

CREATE OR REPLACE FUNCTION dh.trace_update_row ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $function$
BEGIN
    EXECUTE 'update dh.' || TG_TABLE_NAME || ' u 
set geom_trace = sq.geom_interval 
from 
(select s.hole_id, from_m, to_m, 
ST_CollectionExtract(public.ST_LocateBetween(public.ST_CurveToLine(c.geom_trace), from_m, to_m)) as geom_interval
from  dh.' || TG_TABLE_NAME || ' s, dh.collar c 
where (c.hole_id = s.hole_id) 
and from_m = ' || NEW.from_m || ' 
) as sq 
where 
u.hole_id = sq.hole_id 
and u.from_m = sq.from_m 
and u.to_m = sq.to_m';
    RETURN NEW;
END;
$function$
