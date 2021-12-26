CREATE TABLE IF NOT EXISTS guilds (
	GuildID integer PRIMARY KEY,
	Prefix text DEFAULT "!",
    WelcomeChannel integer,
    LeaveChannel integer,
    Profanity integer DEFAULT 1
);

CREATE TABLE IF NOT EXISTS exp(
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 1,
    XPLock text DEFAULT CURRENT_TIMESTAMP
 );