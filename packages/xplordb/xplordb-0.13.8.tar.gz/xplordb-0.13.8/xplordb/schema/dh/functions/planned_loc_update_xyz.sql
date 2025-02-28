

CREATE OR REPLACE FUNCTION dh.planned_loc_update_xyz ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $function$
DECLARE
  	collar_srid_geom geometry;
BEGIN
	collar_srid_geom := public.ST_Transform(NEW.planned_loc, NEW.srid);
    UPDATE
        ONLY dh.collar
    SET
        planned_x = public.ST_X(collar_srid_geom),
        planned_y = public.ST_Y(collar_srid_geom),
        planned_z = public.ST_Z(collar_srid_geom)
    WHERE
        NEW.hole_id = dh.collar.hole_id;
    RETURN NEW;
END;
$function$
