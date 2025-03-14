SELECT name, chemical_form, COUNT(*) AS occurence_count
FROM dietarycomponent
GROUP BY name
ORDER BY occurence_count DESC;