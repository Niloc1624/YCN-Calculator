CREATE TABLE testevents AS SELECT * 
FROM b
WHERE (style = 'standard' AND (dances = 'waltz' OR dances = 'tango' OR dances = 'v. waltz' OR dances = 'foxtrot' OR dances = 'quickstep')) 
    OR (style = 'smooth' AND (dances = 'waltz' OR dances = 'tango' OR dances = 'foxtrot' OR dances = 'v. waltz')) 
    OR (style = 'latin' AND (dances = 'rumba' OR  dances ='cha cha' OR dances = 'jive' OR dances = 'samba' OR dances = 'paso doble')) 
    OR (style = 'rhythm' AND (dances = 'rumba' OR dances = 'cha cha' OR dances = 'swing' OR dances = 'mambo' OR dances = 'bolero')); 

UPDATE events SET dances = 'J' WHERE dances = 'jive'; 

WITH waltz AS (
    SELECT level, style, dances 
    FROM events
    WHERE dances = "W"
)
INSERT INTO events(level, style, dances) 
CREATE VIEW waltz AS SELECT level, style, dances
FROM events
WHERE dances = "W";