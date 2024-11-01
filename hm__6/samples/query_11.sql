SELECT
    ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN subjects s ON g.subject_id = s.id
WHERE g.student_id = %s AND s.teacher_id = %s;