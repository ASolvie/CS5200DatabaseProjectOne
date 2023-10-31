def parse_functional_dependencies(fd_input):
    fd_dict = {}
    for fd in fd_input:
        left, right = fd.split("->")
        left = left.strip()
        right = [r.strip() for r in right.split(",")]
        fd_dict[left] = right
    return fd_dict

def find_transitive_dependencies(fd_dict):
    transitive_dependencies = []
    for left, rights in fd_dict.items():
        for right in rights:
            if right in fd_dict and left != right:
                transitive_dependencies.append((left, right, fd_dict[right]))
    return transitive_dependencies

def reorganize_for_3NF(fd_dict, primary_keys, transitive_deps):
    new_tables = {}
    for left, middle, rights in transitive_deps:
        # Move the transitive attributes to a new table
        new_table_name = middle + "Details"
        new_tables[new_table_name] = rights + [middle]
        
        # Adjust the original table by removing transitive attributes
        fd_dict[left] = list(set(fd_dict[left]) - set(rights))

        # Update primary key if needed
        if middle in primary_keys:
            primary_keys.remove(middle)
            primary_keys.append(new_table_name)

    return new_tables

# Example usage
fd_input = [
    "StudentID -> FirstName, LastName",
    "Course -> CourseStart, CourseEnd, Professor",
    "Professor -> ProfessorEmail"
]

primary_keys = ["StudentID", "Course"]

fd_dict = parse_functional_dependencies(fd_input)
transitive_deps = find_transitive_dependencies(fd_dict)
new_tables = reorganize_for_3NF(fd_dict, primary_keys, transitive_deps)

print("Revised Functional Dependencies:", fd_dict)
print("transitive dependency", transitive_deps)
print("New Tables for 3NF:", new_tables)
print("Updated Primary Keys:", primary_keys)