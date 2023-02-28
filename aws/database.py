# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools
from pyignite import Client


COURSE_CREATE_TABLE_QUERY = '''CREATE TABLE COURSE (
    CODE INT(11) PRIMARY KEY,
    CID CHAR(10) NOT NULL,
    Name CHAR(35) NOT NULL,
    Instructor CHAR(35) NOT NULL,
    Limits INT(11) NOT NULL,
);'''



STUDENT_CREATE_TABLE_QUERY = '''CREATE TABLE STUDENT (
    ID INT(11) PRIMARY KEY,
    Name CHAR(35) NOT NULL,
);'''


ENROLLMENT_CREATE_TABLE_QUERY = '''CREATE TABLE ENROLLMENT (
    ID INT(11) DEFAULT 0,
    COURSECODE INT(11) NOT NULL,
    STUDENTID INT(11) NOT NULL,
    PRIMARY KEY(COURSECODE, STUDENTID)
)WITH "affinityKey=COURSECODE";'''


COURSE_INSERT_QUERY = '''INSERT INTO COURSE(
    CODE, CID, Name, Instructor, Limits
) VALUES (?, ?, ?, ?, ?);'''


STUDENT_INSERT_QUERY = '''INSERT INTO STUDENT(
    ID, Name
) VALUES (?, ?);'''


ENROLLMENT_INSERT_QUERY = '''INSERT INTO ENROLLMENT(
 COURSECODE, STUDENTID
) VALUES (?, ?);'''



def read_data_file(path):
    data = [];
    with open(path, 'r') as file:
        for line in file:
            content = line.strip('\n').split(",")
            content = [int(i.strip()) if i.strip().isnumeric() else i.strip() for i in content]
            data.append(content)
    return data

def establish_connection(ip="127.0.0.1"):
    client = Client()
    client.connect(ip, 10800)   # query to itself
    return client


def initialize_db(client):
    # client = establish_connection()
    
    client.sql('DROP TABLE COURSE IF EXISTS;')
    client.sql(COURSE_CREATE_TABLE_QUERY)
    client.sql('DROP TABLE STUDENT IF EXISTS;')
    client.sql(STUDENT_CREATE_TABLE_QUERY)
    client.sql('DROP TABLE ENROLLMENT IF EXISTS;')
    client.sql(ENROLLMENT_CREATE_TABLE_QUERY)

    COURSE_DATA = read_data_file('/home/ubuntu/distr-course-web/data/Course.txt')
    STUDENT_DATA = read_data_file('/home/ubuntu/distr-course-web/data/Student.txt')
    ENROLLMENT_DATA = read_data_file('/home/ubuntu/distr-course-web/data/Enrollment.txt')

    for row in COURSE_DATA:
        try:
            client.sql(COURSE_INSERT_QUERY, query_args=row)
        except:
            print('Existed!')

    for row in STUDENT_DATA:
        try:
            client.sql(STUDENT_INSERT_QUERY, query_args=row)
        except:
            print('Existed!')

    for row in ENROLLMENT_DATA:
        try:
            client.sql(ENROLLMENT_INSERT_QUERY, query_args=row)
        except:
            print('Existed!')
    
    return client


## Select
# How many students in this course
def number_students_in_course(client, COURSECODE):
    QUERY = f'''
            SELECT COUNT(DISTINCT ID)
            FROM ENROLLMENT
            WHERE COURSECODE = {int(COURSECODE)};
            '''
    return client.sql(QUERY)


# Select all the students' name in this course
def students_in_course(client, COURSECODE):
    QUERY = f'''
            SELECT s.NAME 
            FROM STUDENT s 
            INNER JOIN ENROLLMENT e ON s.ID = e.STUDENTID 
            Where e.COURSECODE = {int(COURSECODE)};
            '''

    return client.sql(QUERY, distributed_joins = True)

# Select all the students' name in this course
def students_info_in_course(client, COURSECODE):
    QUERY = f'''
            SELECT s.ID, s.NAME
            FROM STUDENT s
            INNER JOIN ENROLLMENT e ON s.ID = e.STUDENTID
            Where e.COURSECODE = {int(COURSECODE)};
            '''

    return client.sql(QUERY, distributed_joins = True)

# Whether the student is in the course
def if_students_in_course(client, COURSECODE, STUDENTID):
    QUERY = f'''
            SELECT * FROM ENROLLMENT
            WHERE STUDENTID = {int(STUDENTID)}
            AND COURSECODE = {int(COURSECODE)};
            '''
    return  client.sql(QUERY)

# Whether the student is in the course
def is_student(client, STUDENTID, NAME):
    QUERY = f'''
            SELECT * FROM STUDENT
            WHERE ID = {int(STUDENTID)}
            AND Name = '{NAME}';
            '''
    return  client.sql(QUERY)


def is_student_id(client, STUDENTID):
    QUERY = f'''
            SELECT * FROM STUDENT
            WHERE ID = {int(STUDENTID)};
            '''
    return  client.sql(QUERY)


def create_student(client, STUDENTID, NAME):
    
    return client.sql(STUDENT_INSERT_QUERY, query_args=[int(STUDENTID), NAME])


# Display all courses the student select
def student_select_course(client, STUDENTID):
    QUERY = f'''SELECT *
                FROM Course c
                INNER JOIN Enrollment e ON c.CODE = e.COURSECODE
                INNER JOIN Student s ON e.STUDENTID = s.ID
                WHERE s.ID = {int(STUDENTID)};'''

    return client.sql(QUERY, distributed_joins = True)


## Delete
# delete the student if in the course
def delete_student_in_course(client, COURSECODE , STUDENTID):
    QUERY = f'''DELETE FROM ENROLLMENT 
                WHERE COURSECODE = {int(COURSECODE)} AND STUDENTID = {int(STUDENTID)};'''

    return client.sql(QUERY)

## Update
# Enroll the student if not in the course
def enroll_student_into_course(client, COURSECODE , STUDENTID):
    QUERY = f'''INSERT INTO ENROLLMENT (COURSECODE, STUDENTID)
            SELECT c.CODE, s.ID 
            FROM STUDENT s 
            INNER JOIN COURSE c 
            ON s.ID = {int(STUDENTID)} AND c.CODE = {int(COURSECODE)}
            AND s.ID NOT IN (SELECT STUDENTID FROM ENROLLMENT e WHERE {int(COURSECODE)} = c.CODE)
            AND c.LIMITS > (SELECT COUNT(*) FROM ENROLLMENT e WHERE e.COURSECODE = c.CODE);'''
    
    return client.sql(QUERY, distributed_joins = True)

def direct_enroll_student_into_course(client, COURSECODE , STUDENTID):

    return client.sql(ENROLLMENT_INSERT_QUERY, query_args=[int(COURSECODE), int(STUDENTID)])

def get_all_course_info(client):
    QUERY = f'''SELECT *
                FROM COURSE
                ORDER BY CODE ASC;
            '''
    return client.sql(QUERY, distributed_joins = True)


def display(result):
    try:
        while True:
            item = next(result)
            if item is not None:
                print(item)
    except StopIteration:
        pass

def is_successful(result):
    # Delete and Insert
    try:
        if (next(result)[0] == 1):
            print('Success')
            return True
        return False
    except:
        print("Fail")
        return False


def is_iterator_empty(result):
    try:
        if result == None:
            return True
        item = next(itertools.chain([result], []))
        if next(item) is not None:
            #print(next(item))
            return False
        else:
            return True
    except StopIteration:
        return True


def display_course(result):
    results = []
    try:
        while True:
            item = next(result)
            print(item)
            if item is not None:
                content = {
                    "CourseCode": item[0],
                    "CourseID": item[1],
                    "CourseName": item[2],
                    "Instructor": item[3]
                }
                results.append(content)
    except StopIteration:
        pass
    return results

import json
def get_course_info(client):
    info = {}
    courses = get_all_course_info(client);
    try:
        while True:
            course = {}
            item = next(courses)
            # print(item)
            if item is not None:
                students = students_info_in_course(client, item[0]);
                # print(item[0])
                course['ID'] = item[1]
                course['name'] = item[2]
                course['Instructor'] = item[3]
                course['Max'] = item[4]
                temp = []
                for i in list(students):
                    temp.append({"id": i[0], "name": i[1]})
                # print(temp)
                course['student'] = temp
            info[item[0]] = course
    except StopIteration:
        pass
    return json.dumps(info)



### Test
#
#client = establish_connection()
#client = initialize_db(client)

#results = create_student(client, 1234,'song')
#print(next(results)[0]==1)
#is_successful(results)
# select * from student where ID = 1234 AND NAME='song'
#results = is_student(client, 12345, 'song')
#display(results)
#print(is_iterator_empty(results))


#q = "Insert into ENROLLMENT values (1, 34660, 1);"
#results = client.sql(q)
#is_successful(results)



#q = '''         SELECT *
#                FROM Course c
#                INNER JOIN Enrollment e ON c.CODE = e.COURSECODE
#                INNER JOIN Student s ON e.STUDENTID = s.ID
#                WHERE s.ID = 1;'''
#results = client.sql(q, distributed_joins = True)
#print(next(results))


#results = student_select_course(client, 1)
#print(display_course(results))
#print("****"*10)



#create_student(client, 12345, 'song')
#results = client.sql('Select * from Course;', distributed_joins = True)
#display(results)


# print('*****'*5)
#results = enroll_student_into_course(client, 34610, 1)
#display(results)
#results = enroll_student_into_course(client, 34660, 1)
#display(results)
#results = client.sql('Select * from ENROLLMENT;', distributed_joins = True)
#display(results)
#results = student_select_course(client, 1)
#print(display_course(results))

# q = "Insert into ENROLLMENT values (1, 34660, 1);"
# results = client.sql(q);
# for i in results:
#     print(*i)
#
# q = "Insert into ENROLLMENT values (2, 34610, 1);"
# results = client.sql(q);
# for i in results:
#     print(*i)
#
# results = client.sql("Select * from ENROLLMENT;")
# for i in results:
#     print(*i)
#
# results = client.sql("Select * from Student;")
# for i in results:
#     print(*i)
#
# results = client.sql("Select * from COURSE;")
# for i in results:
#     print(*i)
#
# QUERY = 'SELECT * FROM ENROLLMENT e JOIN COURSE c on e.COURSECODE = c.CODE;'
# with client.sql(QUERY, distributed_joins = True) as results:
#     print('*' * 50)
#     for i in results:
#         print(i)
#
# enroll_student_into_course(client, 34660, 2)
#
# students_in_course(client, 34660)
#
# if_students_in_course(client, 34660, 1)
#
# student_select_course(client, 1)
#
# delete_student_in_course(client, 34660, 1)
#
#
