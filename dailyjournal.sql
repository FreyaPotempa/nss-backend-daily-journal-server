CREATE TABLE `Moods`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `mood` TEXT NOT NULL
);


CREATE TABLE `JournalEntries`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
    `entry` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
);

INSERT INTO `Moods` VALUES (null, "Ecstatic");
INSERT INTO `Moods` VALUES (null, "Melancholy");
INSERT INTO `Moods` VALUES (null, "Lovesick");
INSERT INTO `Moods` VALUES (null, "Maudlin");
INSERT INTO `Moods` VALUES (null, "Belabored");
INSERT INTO `Moods` VALUES (null, "Bemoaned");

INSERT INTO `JournalEntries` VALUES (null, "Late Thoughts", "Today I walked a midnight dreary", 4);
INSERT INTO `JournalEntries` VALUES (null, "Poetry", "A poem on the agony and ecstasy of solitude", 3);
INSERT INTO `JournalEntries` VALUES (null, "Le Sigh", "The beauty of existence is nearly too much a thing to bear", 1);

SELECT * FROM `JournalEntries`
WHERE `entry` LIKE "%agony%"

CREATE TABLE `Tags`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `tag` TEXT NOT NULL
);

CREATE TABLE `EntryTags`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
    FOREIGN KEY(`entry_id`) REFERENCES `JournalEntries`(`id`)
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

INSERT INTO `Tags` VALUES (null, "poetry");
INSERT INTO `Tags` VALUES (null, "introspection");
INSERT INTO `Tags` VALUES (null, "grattitude");
INSERT INTO `Tags` VALUES (null, "whinge");



