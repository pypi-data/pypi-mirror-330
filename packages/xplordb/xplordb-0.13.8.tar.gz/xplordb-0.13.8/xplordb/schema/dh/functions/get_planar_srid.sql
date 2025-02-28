-- custom function returning 3857 if srid_input is not planar, else return srid_input
CREATE OR REPLACE FUNCTION dh.get_planar_srid(srid_input INTEGER) RETURNS INTEGER AS $$
DECLARE
    planar_srid INTEGER;
BEGIN
	select 
	case 
	when proj4text ILIKE '%units=%' THEN srid_input
	else 3857
	end
	into planar_srid
	from spatial_ref_sys
	where srid = srid_input;

	return planar_srid;
END;
$$ LANGUAGE plpgsql;