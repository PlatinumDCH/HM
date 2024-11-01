
SELECT
    students.fullname,
    ROUND(AVG(grades.grade), 2) AS average_grade
FROM students
JOIN grades ON students.id = grades.student_id
WHERE grades.subject_id = 1  -- current ID subj
GROUP BY students.id
ORDER BY average_grade DESC
LIMIT 1;