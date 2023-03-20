package main

import (
	"fmt"
)

type Ranks struct {
	hospitals map[string][]string
	students  map[string][]string
}

func (ranks Ranks) New() Ranks {
	return Ranks{
		hospitals: map[string][]string{},
		students:  map[string][]string{},
	}
}

func (ranks Ranks) Students() (students []string) {
	for student := range ranks.students {
		students = append(students, student)
	}
	return students
}

func (ranks Ranks) AddHospital(hospitalName string, hospital []string) (Ranks, error) {
	if len(hospital) < len(ranks.students) {
		return ranks, fmt.Errorf("given hospital is not ranking all students(%s)", ranks.Students())
	} else {
		ranks.hospitals[hospitalName] = hospital
		return ranks, nil
	}
}

func (ranks Ranks) RemoveFirstFromHospitalRank(hospitalName string) (Ranks, error) {
	ranksForHospital, foundRanksForHospital := ranks.hospitals[hospitalName]
	if !foundRanksForHospital {
		return ranks, fmt.Errorf("found no ranks for hospitalName: %s", hospitalName)
	}
	if len(ranksForHospital) == 0 {
		return ranks, fmt.Errorf("ranks for hospitalName: %s, are of length 0", hospitalName)
	}
	ranks.hospitals[hospitalName] = ranksForHospital[1:]
	return ranks, nil
}

func (ranks Ranks) GetRankingFromStudentForHospital(studentName string, hospitalName string) int {
	for index, each := range ranks.students[studentName] {
		if each == hospitalName {
			return index
		}
	}
	return -1
}

type Matches struct {
	studentToHospital map[string]string
	hospitalToStudent map[string]string
}

func (matches Matches) New() Matches {
	return Matches{
		studentToHospital: map[string]string{},
		hospitalToStudent: map[string]string{},
	}
}

func (matches Matches) hospitalsIsMatched(hospitalName string) bool {
	_, isMatched := matches.hospitalToStudent[hospitalName]
	return isMatched
}

func (matches Matches) studentIsMatched(studentName string) bool {
	_, isMatched := matches.studentToHospital[studentName]
	return isMatched
}

func (matches Matches) pairHospitalAndStudent(hospitalName string, studentName string) Matches {
	matches.studentToHospital[studentName] = hospitalName
	matches.hospitalToStudent[hospitalName] = studentName
	return matches
}

func (matches Matches) unpairHospitalAndStudent(hospitalName string, studentName string) Matches {
	delete(matches.studentToHospital, studentName)
	delete(matches.hospitalToStudent, hospitalName)
	return matches
}

func (matches Matches) Print() {
	fmt.Println("matches:")
	for studentName, hospitalName := range matches.studentToHospital {
		fmt.Println(studentName, " is matched with ", hospitalName)
	}
}

func main() {
	ranks := Ranks{
		students: map[string][]string{
			"Steve":  {"Seattle", "Boston", "Chicago"},
			"Dave":   {"Chicago", "Seattle", "Boston"},
			"Nadine": {"Boston", "Chicago", "Seattle"},
		},
		hospitals: map[string][]string{
			"Chicago": {"Steve", "Nadine", "Dave"},
			"Boston":  {"Steve", "Dave", "Nadine"},
			"Seattle": {"Nadine", "Dave", "Steve"},
		},
	}
	//ranks, err = ranks.AddHospital("Chicago", []string{"Steve", "Nadine", "Dave"})
	matches, err := matchHospitalsWithStudents(ranks, Matches{}.New())
	if err != nil {
		fmt.Println(err)
	} else {
		matches.Print()
	}
}

func matchHospitalsWithStudents(ranks Ranks, matches Matches) (Matches, error) {
	// find hospital with no match
	// find next student on the list
	// check if student is already tentatively matched
	// get the hospital information about the last match
	// update the student to keep the best offer
	// update the hospitals
	var err error
	hospitalName, foundEmptyHospital := findEmptyHospital(ranks, matches)
	if !foundEmptyHospital {
		return matches, err
	}
	studentName := ranks.hospitals[hospitalName][0]
	ranks, err = ranks.RemoveFirstFromHospitalRank(hospitalName)
	if err != nil {
		return matches, err
	}
	if matches.studentIsMatched(studentName) {
		currentHospitalRank := ranks.GetRankingFromStudentForHospital(studentName, hospitalName)
		previouslyMatchedHospital := matches.studentToHospital[studentName]
		previousHospitalRank := ranks.GetRankingFromStudentForHospital(studentName, previouslyMatchedHospital)
		if previousHospitalRank > currentHospitalRank {
			matches = matches.unpairHospitalAndStudent(previouslyMatchedHospital, studentName)
		} else {
			return matchHospitalsWithStudents(ranks, matches)
		}
	}
	matches = matches.pairHospitalAndStudent(hospitalName, studentName)
	return matchHospitalsWithStudents(ranks, matches)
}

func findEmptyHospital(ranks Ranks, matches Matches) (hospitalName string, foundEmptyHospital bool) {
	for hospitalName = range ranks.hospitals {
		hospitalIsUnmatched := !matches.hospitalsIsMatched(hospitalName)
		if hospitalIsUnmatched {
			return hospitalName, true
		}
	}
	return "", false
}
