SELECT name, COUNT(*) AS occurrence_count
FROM analyticalcomponent
GROUP BY name
ORDER BY occurrence_count DESC;
