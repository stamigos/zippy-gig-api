from zippy_gig.models import db 

db.execute_sql('''
	
create or replace function distance_kilometers(lat_login_user numeric,
                                               lng_login_user numeric,
                                               lat_account numeric,
                                               lng_account numeric) returns float8 as
$$
declare
    D_EARTH integer;
    d_lat float8;
    d_lng float8;
    a float8;
    c float8;
    d float8;
begin
    D_EARTH := 2 * 6371;
    d_lat := radians(lat_account - lat_login_user);
    d_lng := radians(lng_account - lng_login_user);
    lat_account := radians(lat_account);
    lat_login_user := radians(lat_login_user);

    a := pow(sin(d_lat / 2), 2) + cos(lat_login_user) * cos(lat_account) * pow(sin(d_lng / 2), 2);
    c := atan2(sqrt(a), sqrt(1 - a));
    d := D_EARTH * c;

    return d;
end;
$$ language plpgsql;
            
	''')