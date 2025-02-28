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
-- __authors__ = ["jmkerloch"]
-- __contact__ = "geology@oslandia.com"
-- __date__ = "2022/03/18"
-- __license__ = "AGPLv3"
----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION dh.geom_update_xyz ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $function$
DECLARE
  	collar_srid_geom geometry;
BEGIN
	collar_srid_geom := public.ST_Transform(NEW.geom, NEW.srid);
    UPDATE
        ONLY dh.collar
    SET
        x = public.ST_X(collar_srid_geom),
        y = public.ST_Y(collar_srid_geom),
        z = public.ST_Z(collar_srid_geom)
    WHERE
        NEW.hole_id = dh.collar.hole_id;
    RETURN NEW;
END;
$function$
