"""Explicit co-teaching identities; no name-based joins or inferred teachers."""
def teachers_of(row):
 return ([row['teacher']] if row.get('teacher') is not None else [])+list(row.get('co_teacher_ids',[]))
