from django.db import migrations

SQL = """
    CREATE OR REPLACE FUNCTION public.get_all_accounts()
    RETURNS integer
    LANGUAGE plpgsql
    AS $function$
    declare
        BEGIN
            return 1;
        END;
    $function$
    ;

"""

class Migration(migrations.Migration):
    dependencies = [
        ('barber_booking', '0001_initial'),
    ]

    operations = [migrations.RunSQL(SQL)]