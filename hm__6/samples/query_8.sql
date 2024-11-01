SELECT
    AVG(grades.grade) AS average_grade
FROM grades
JOIN subjects ON grades.subject_id = subjects.id
WHERE subjects.teacher_id = 1; 