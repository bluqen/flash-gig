student={"name":"Emmanuel",
         "age":"17",
         "grade":"A"}
INPUT=input("ENTER A KEY : ")
found = False
for key in student.keys():
    if key==INPUT:
        print(student[key])
        found = True
        break
    else:
        continue

if found == False:
    print("KEY NOT FOUND")