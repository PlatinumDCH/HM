SELECT 
    groups.name AS group_name, 
    ROUND(AVG(grades.grade), 2) AS average_grade
FROM groups
JOIN students ON groups.id = students.group_id
JOIN grades ON students.id = grades.student_id
WHERE grades.subject_id = 1  -- current ID subj
GROUP BY groups.id;