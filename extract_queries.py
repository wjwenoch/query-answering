q1 = 'x rdf type ub GraduateStudent . x ub takesCourse url Department0 University0 GraduateCourse0'
q2 = ''
q3 = 'x rdf type ub Publication . x ub publicationAuthor url AssistantProfessor0'
q4 = ''
q5 = 'x rdf type ub Person . x ub memberOf Department0 University0'
q6 = 'x rdf type ub Student'
q7 = ''
q8 = ''
q9 = ''
q10 = 'x rdf type ub Student . x ub takesCourse url Department0 University0 GraduateCourse0'
q11 = 'x rdf type ub ResearchGroup . x ub subOrganizationOf url University0'
q12 = ''
q13 = 'x rdf type ub Person . url University0 ub hasAlumnus x'
q14 = 'x rdf type ub UndergraduateStudent'
qs = [q1, q3, q5, q6, q10, q11, q13, q14]

for q in qs:
    print(q.split(' . '))
