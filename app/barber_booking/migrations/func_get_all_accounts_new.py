from django.db import migrations

SQL = """
    CREATE OR REPLACE FUNCTION public.get_all_accounts_new()
    RETURNS integer
    LANGUAGE plpgsql
    AS $function$
    declare
        BEGIN
            return 2;
        END;
    $function$
    ;

"""

class Migration(migrations.Migration):
    dependencies = [
        ('barber_booking', '0001_alter_hairstyle_is_active'),
    ]

    operations = [migrations.RunSQL(SQL)]