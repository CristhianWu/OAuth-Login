# OAuth-Login

docker compose exec backend alembic upgrade head && \
docker exec -i postgres_db psql -U user -d mydatabase -c "
  insert into roles(role) values
    ('admin'),
    ('employee'),
    ('user'),
  insert into role_permissions(role, permission) values
    ('admin', '*'),
    ('employee', 'login'),
    ('user', 'login'),
"