# queries.py
QUERIES = {
    "1. Artifacts from 11th Century Byzantine": 
        "SELECT * FROM artifact_metadata WHERE century='11th century' AND culture='Byzantine'",

    "2. Unique Cultures": 
        "SELECT DISTINCT culture FROM artifact_metadata",

    "3. Archaic Period Artifacts": 
        f"SELECT * FROM artifact_metadata WHERE period LIKE '%%Archaic%%';",

    "4. Titles by Accession Year (Desc)": 
        "SELECT title FROM artifact_metadata ORDER BY accessionyear DESC",

    "5. Artifact Count per Department": 
        "SELECT department, COUNT(*) FROM artifact_metadata GROUP BY department",

    "6. Artifacts with >3 Images": 
        "SELECT objectid FROM artifact_media WHERE imagecount > 3",

    "7. Average Rank": 
        "SELECT AVG(`rank_value`) FROM artifact_media",

    "8. Media > Color Count": 
        """
        SELECT am.objectid
        FROM artifact_media am
        JOIN (
            SELECT objectid, COUNT(*) AS colorcount
            FROM artifact_colors
            GROUP BY objectid
        ) ac ON am.objectid = ac.objectid
        WHERE ac.colorcount > am.mediacount;
        """,

    "9. Artifacts Between 1500–1600": 
        "SELECT objectid FROM artifact_media WHERE datebegin >= 1500 AND dateend <= 1600",

    "10. No Media Files": 
        "SELECT objectid FROM artifact_media WHERE mediacount = 0",

    "11. Distinct Hues": 
        "SELECT DISTINCT hue FROM artifact_colors",

    "12. Top 5 Colors by Frequency": 
        "SELECT color, COUNT(*) AS freq FROM artifact_colors GROUP BY color ORDER BY freq DESC LIMIT 5",

    "13. Average Coverage % per Hue": 
        "SELECT hue, AVG(percent) FROM artifact_colors GROUP BY hue",

    "14. Colors by Artifact ID":
        """
        SELECT color, spectrum, hue, percent, css3
        FROM artifact_colors
        WHERE objectid = 141671;
        """,

    "15. Total Color Entries":
        "SELECT COUNT(*) FROM artifact_colors",

    "16. Byzantine Artifacts Titles and Hues":
        """
        SELECT m.title, c.hue
        FROM artifact_metadata m
        JOIN artifact_colors c ON m.id = c.objectid
        WHERE m.culture = 'Byzantine'
        """,

    "17. Artifact Titles with Associated Hues":
        """
        SELECT m.title, c.hue
        FROM artifact_metadata m
        JOIN artifact_colors c ON m.id = c.objectid
        """,

    "18. Artifact Titles, Cultures, Media Ranks with Non-null Period":
        """
        SELECT m.title, m.culture, md.rank_value
        FROM artifact_metadata m
        JOIN artifact_media md ON m.id = md.objectid
        WHERE m.period IS NOT NULL
        """,

    "19. Top 10 Ranked Artifacts with Hue 'Grey'":
        """
        SELECT m.title
        FROM artifact_metadata m
        JOIN artifact_colors c ON m.id = c.objectid
        JOIN artifact_media md ON m.id = md.objectid
        WHERE c.hue = 'Grey'
        ORDER BY md.rank_value
        LIMIT 10
        """,

    "20. Artifact Count and Average Media Count Per Classification":
        """
        SELECT m.classification, COUNT(*) AS artifact_count, AVG(md.mediacount) AS avg_media_count
        FROM artifact_metadata m
        JOIN artifact_media md ON m.id = md.objectid
        GROUP BY m.classification
        ORDER BY artifact_count DESC
        """,

    "21. Artifacts Created in 4th Century CE":
        """
        SELECT *
        FROM artifact_metadata
        WHERE century = '4th century CE'
        """,

    "22. Artifacts with Medium Containing 'Bronze'": 
          "SELECT * FROM artifact_metadata WHERE LOWER(medium) LIKE '%%bronze%%';",


    "23. Top 10 Departments by Number of Artifacts":
        """
        SELECT department, COUNT(*) AS total
        FROM artifact_metadata
        GROUP BY department
        ORDER BY total DESC
        LIMIT 10
        """,

    "24. Artifacts Without Any Description":
        """
        SELECT *
        FROM artifact_metadata
        WHERE description IS NULL OR description = ''
        """,

    "25. Average Image Count Per Classification":
        """
        SELECT m.classification, AVG(md.imagecount) AS avg_imagecount
        FROM artifact_metadata m
        JOIN artifact_media md ON m.id = md.objectid
        GROUP BY m.classification
        ORDER BY avg_imagecount DESC
        """,

    "26. List Titles and Colors of Artifacts with More than 5 Images":
        """
        SELECT m.title, c.color
        FROM artifact_metadata m
        JOIN artifact_media md ON m.id = md.objectid
        JOIN artifact_colors c ON m.id = c.objectid
        WHERE md.imagecount > 5
        ORDER BY m.title
        """,

    "27. Preview 20 Artifacts: ID, color and percent":
        """
        SELECT objectid, color, percent
        FROM artifact_colors
        LIMIT 20;
        """,

    "28. Colors and Their Frequencies for Artifacts from 'Greek' Culture":
        """
        SELECT c.color, COUNT(*) AS frequency
        FROM artifact_metadata m
        JOIN artifact_colors c ON m.id = c.objectid
        WHERE m.culture = 'Greek'
        GROUP BY c.color
        ORDER BY frequency DESC
        """,

    "29. Artifacts with a Rank Higher than 50 and Their Classification":
        """
        SELECT m.title, m.classification, md.rank_value
        FROM artifact_metadata m
        JOIN artifact_media md ON m.id = md.objectid
        WHERE md.rank_value > 50
        ORDER BY md.rank_value DESC
        """,

    "30. Summary of Average Color Coverage Percent":
        """
        SELECT AVG(percent) AS avg_color_percent
        FROM artifact_colors;
        """
    
}

