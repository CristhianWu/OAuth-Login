from django.db import migrations

def insertar_roles_sql(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        # Insertar roles
        cursor.execute("""
            INSERT INTO roles (role) VALUES
            ('admin'),
            ('employee'),
            ('user')
            ON CONFLICT DO NOTHING;
        """)

        # Insertar permisos
        cursor.execute("""
            INSERT INTO role_permissions (role, permission) VALUES
            ('admin', '*'),
            ('employee', 'login'),
            ('user', 'login')
            ON CONFLICT DO NOTHING;
        """)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # Cambia "core" si tu app se llama distinto
    ]

    operations = [
        migrations.RunPython(insertar_roles_sql),
    ]