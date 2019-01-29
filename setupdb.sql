create table if not exists rendered_code (
  id serial,
  name text not null,
  syntax text not null,
  content bytea not null,
  created_at timestamp with time zone not null default current_timestamp,
  unique (name, syntax)
);

create table if not exists raw_code (
  id serial,
  name text unique,
  sha1sum bytea unique not null,
  content text not null,
  created_at timestamp with time zone not null default current_timestamp
);
