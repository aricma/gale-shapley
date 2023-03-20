#include <string>
#include <iostream>

std::map<std::string, std::string> merge (std::map<std::string, std::string> mapA, std::map<std::string, std::string> mapB) {
    return mapA.insert(mapB.begin(), mapB.end())
}

std::map<std::string, std::string> add (std::map<std::string, std::string> mapA, std::string key, std::string value) {
    return mapA.insert({key, value})
}

struct Matches {
    std::map<std::string, std::strind> hospitalToStudent;
    std::map<std::string, std::strind> studentToHospital;

    Matches match (Matches matches, std::string student, std::string hospital) {
        return Matches{
            hospitalToStudent: add(matches.hospitalToStudent, {{hospital, student}})
        }
    }
};

int main () {
    std::cout <<"Hello World\n";

}