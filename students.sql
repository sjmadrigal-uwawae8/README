
CREATE TABLE students(
  id TEXT PRIMARY KEY,
  first_name TEXT Not NULL,
  middle_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  gender TEXT NOT NULL,
  birthdate TEXT NOT NULL,
  place_of_birth TEXT NOT NULL,
  email_address UNIQUE NOT NULL,
  contact_number TEXT NOT NULL,
  section TEXT NOT NULL,
  league_color TEXT NOT NULL
)