from execute_11 import execute_query


if __name__ == '__main__':
    student_group_id = 1
    subject_id = 2

    results = execute_query('query_12.sql', (student_group_id, subject_id))

    for row in results:
        print(f"Student: {row[0]}, Grade: {row[1]}, Date: {row[2]}")