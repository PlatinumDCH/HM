
SELECT
    subjects.name AS course_name
FROM subjects
JOIN grades ON subjects.id = grades.subject_id
WHERE grades.student_id = 10 AND subjects.teacher_id = 3;