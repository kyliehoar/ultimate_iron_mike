CREATE TABLE IF NOT EXISTS fighters (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL,
  age INT NOT NULL,
  height INT NOT NULL,
  weight INT NOT NULL,
  reach INT NOT NULL,
  wins INT NOT NULL,
  losses INT NOT NULL,
  currentwinstreak INT NOT NULL,
  currentlosestreak INT NOT NULL,
  longestwinstreak INT NOT NULL
);