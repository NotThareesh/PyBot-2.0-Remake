CREATE TABLE IF NOT EXISTS guilds (
	GuildID integer PRIMARY KEY,
	Prefix text DEFAULT "!",
    WelcomeChannel text NULL,
    LeaveChannel text NULL
);

CREATE TABLE IF NOT EXISTS exp(
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
 );