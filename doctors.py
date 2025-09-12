doctors = []


def create_doctor():
    while True:
        name = input("Enter the doctor's name: ")
        age = input("Enter the doctor's age: ")
        specialty = input("Enter the doctor's specialty: ")
        document = input("Enter the doctor's document: ")

        # Finish when name is empty or DNI is already in the list
        if name == "":
            break

        if any(doctor["document"] == document for doctor in doctors):
            print("Doctor already exists")
            break
        else:
            doctor = {
                "id": len(doctors) + 1,
                "name": name,
                "age": age,
                "specialty": specialty,
                "document": document,
            }
            doctors.append(doctor)
