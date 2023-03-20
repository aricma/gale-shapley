import dataclasses
from typing import List, Optional


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DISABLED = "\033[0;90m"

    @classmethod
    def fail(cls, *text: str) -> str:
        return f"{cls.FAIL}{''.join(text)}{cls.ENDC}"

    @classmethod
    def warning(cls, *text: str) -> str:
        return f"{cls.WARNING}{''.join(text)}{cls.ENDC}"

    @classmethod
    def ok_green(cls, *text: str) -> str:
        return f"{cls.OKGREEN}{''.join(text)}{cls.ENDC}"

    @classmethod
    def ok_blue(cls, *text: str) -> str:
        return f"{cls.OKBLUE}{''.join(text)}{cls.ENDC}"

    @classmethod
    def disabled(cls, *text: str) -> str:
        return f"{cls.DISABLED}{''.join(text)}{cls.ENDC}"


@dataclasses.dataclass
class Option:
    name: str
    list: List[str]
    stable_match: Optional[str] = None


class Hospital(Option):
    current_offer: Optional[str] = None


class Student(Option):
    tentative_offer: Optional[str] = None

    def keep_highest_offer(self, current_offer: str) -> str:  # returns offer
        if self.tentative_offer is not None and self.tentative_offer != current_offer:
            index_of_tentative_match = safe_index(list=self.list, value=self.tentative_offer)
            index_of_current_offer = safe_index(list=self.list, value=current_offer)
            if index_of_tentative_match < index_of_current_offer:
                self.list.pop(index_of_current_offer)
                return self.tentative_offer
        else:
            # if tentative_offer is None
            # if tentative_offer == current_offer
            # if index_of_tentative_match > index_of_current_offer
            self.tentative_offer = current_offer
            return current_offer


class OfferService:

    def __init__(self, students: List[Student], hospitals: List[Hospital]):
        self.validate_data(students=students, hospitals=hospitals)
        self.students = students
        self.hospitals = hospitals

    @classmethod
    def validate_data(cls, students: List[Student], hospitals: List[Hospital]) -> None:
        number_of_students = len(students)
        number_of_hospitals = len(hospitals)
        if number_of_hospitals != number_of_students:
            raise Exception(Color.fail(f"OfferService: number of hospitals is not equal to the number of students"))
        for hospital, student in zip(hospitals, students):
            length_of_hospital_list = len(hospital.list)
            if length_of_hospital_list != number_of_students:
                raise Exception(
                    Color.fail(
                        f"OfferService: Hospital({hospital.name}).list[{length_of_hospital_list}] "
                        f"is not equal to the number of students[{number_of_students}]"
                    )
                )
            length_of_student_list = len(student.list)
            if length_of_student_list != number_of_hospitals:
                raise Exception(
                    Color.fail(
                        f"OfferService: Student({student.name}).list[{length_of_student_list}] "
                        f"is not equal to the number of hospitals[{number_of_hospitals}]"
                    )
                )
        return None

    def find_next_hospital_without_offer(self) -> Optional[str]:
        for hospital in self.hospitals:
            if hospital.current_offer is None:
                return hospital.name
        return None

    def send_next_offer(self, hospital_name: str) -> None:
        hospital = self.get_hospital_for_name(hospital_name=hospital_name)
        hospital.current_offer = hospital.list.pop(0)
        student = self.get_student_for_name(student_name=hospital.current_offer)
        print(Color.disabled(f"    Hospital({hospital_name}) send offer to Student({student.name})"))
        kept_offer = student.keep_highest_offer(current_offer=hospital.name)
        if kept_offer != hospital.name:
            print(Color.disabled(f"    Student({student.name}) rejects offer from Hospital({hospital_name})"))
            hospital.current_offer = None
        else:
            print(
                Color.disabled(f"    Student({student.name}) tentatively accepts offer from Hospital({hospital_name})")
            )

    def get_hospital_for_name(self, hospital_name: str) -> Hospital:
        for hospital in self.hospitals:
            if hospital.name == hospital_name:
                return hospital
        raise KeyError(Color.fail(f"OfferService: no hospital found for name: {hospital_name}"))

    def get_student_for_name(self, student_name: str) -> Student:
        for student in self.students:
            if student.name == student_name:
                return student
        raise KeyError(Color.fail(f"OfferService: no hospital found for name: {student_name}"))

    def stabilize_matches(self):
        for student, hospital in zip(self.students, self.hospitals):
            student.stable_match = student.tentative_offer
            hospital.stable_match = hospital.current_offer


def safe_index(list: List[str], value: str) -> int:
    try:
        return list.index(value)
    except ValueError:
        return -1


def main():
    students = [
        Student(name="John", list=["Chicago", "Boston", "Washington", "LA"]),
        Student(name="Mona", list=["Washington", "LA", "Boston", "Chicago"]),
        Student(name="Steve", list=["Washington", "LA", "Boston", "Chicago"]),
        Student(name="Navid", list=["LA", "Washington", "Chicago", "Boston"]),
    ]
    hospitals = [
        Hospital(name="Chicago", list=["John", "Mona", "Steve", "Navid"]),
        Hospital(name="Washington", list=["Mona", "Steve", "John", "Navid"]),
        Hospital(name="Boston", list=["Mona", "John", "Navid", "Steve"]),
        Hospital(name="LA", list=["Mona", "John", "Navid", "Steve"]),
    ]
    os = OfferService(students=students, hospitals=hospitals)
    while True:
        next_hospital_without_pending_offer = os.find_next_hospital_without_offer()
        if next_hospital_without_pending_offer is None:
            break
        os.send_next_offer(hospital_name=next_hospital_without_pending_offer)
    os.stabilize_matches()

    for hospital in hospitals:
        print(Color.ok_green(hospital.name, " has a stable match with ", hospital.stable_match))


if __name__ == '__main__':
    main()
