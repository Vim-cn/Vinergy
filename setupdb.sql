create table if not exists rendered_code (
  id serial primary key,
  name text not null,
  syntax text not null,
  content bytea not null,
  created_at timestamp with time zone not null default current_timestamp,
  visited_at timestamp with time zone not null default current_timestamp,
  unique (name, syntax)
);

create index idx_rendered_code_visited_at on rendered_code (visited_at);

create table if not exists raw_code (
  id serial primary key,
  name text unique,
  sha1sum bytea unique not null,
  content text not null,
  created_at timestamp with time zone not null default current_timestamp,
  visited_at timestamp with time zone
);

create index idx_raw_code_visited_at on raw_code (visited_at);
