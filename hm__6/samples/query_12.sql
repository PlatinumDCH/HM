SELECT
    s.fullname AS student_name,
    g.grade,
    g.grade_date
FROM
    students s
JOIN
    grades g ON s.id = g.student_id
WHERE
    s.group_id = %s
    AND g.subject_id = %s
    AND g.grade_date = (
        SELECT MAX(grade_date)
        FROM grades
        WHERE student_id = s.id AND subject_id = g.subject_id
    );