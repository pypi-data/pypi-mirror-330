CREATE OR REPLACE FUNCTION dh.update_gis_planned_loc_dh_collar_ll ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $function$
BEGIN
    UPDATE
        ONLY dh.collar
    SET
        planned_loc = public.ST_Transform (public.ST_GeomFromEWKT ('SRID=' || srid || ';POINT(' || planned_x || ' ' || planned_y || ' ' || planned_z || ')'), 4326),
        proj_planned_loc = public.ST_Transform (public.ST_GeomFromEWKT ('SRID=' || srid || ';POINT(' || planned_x || ' ' || planned_y || ' ' || planned_z || ')'), dh.get_planar_srid(srid))
    WHERE
        NEW.hole_id = dh.collar.hole_id;
    RETURN NEW;
END;
$function$