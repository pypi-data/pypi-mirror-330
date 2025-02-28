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

CREATE OR REPLACE FUNCTION dem.cap_alos_example ()
    RETURNS TABLE (
        oid bigint,
        hole_id character varying,
        dem_z_geom public.geometry,
        dem_z double precision,
        z real)
    LANGUAGE sql
    AS $function$
    SELECT
        row_number() OVER ()
        oid,
        hole_id,
        public.ST_MakePoint (x, y, public.ST_Value (rast, collar.geom)) AS dem_z_geom,
        public.ST_Value (rast, collar.geom) AS dem_z,
        z
    FROM
        dh.collar
    LEFT JOIN dem.capricorn ON public.ST_Intersects (rast, collar.geom)
$function$
