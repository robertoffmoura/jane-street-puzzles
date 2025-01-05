solution = """
1 1 1 2 2 2 3 3 4 4 4
1 3 3 3 2   3 4 4 4  
1 3 3 1   7 3 4 4 4 9
1 3 3   1 0 0 4 1 1  
1 3   1 4 4   4 1 8 1
1 4 4 4   4 4 4 8 8 9
7 4 4 4 4   7 4 8 8 8
7 7 1 4 1 7 7   9 8 9
7 7 1 1 1 7 7 9 9 9 9
  1 1 4 4   7 9 9 9 2
4 4 4 4 4 3   3 9 9 2
"""
result = 0
lines = [line for line in solution.split("\n") if line != ""]
for line in lines:
	strings = [s.replace(" ", "") for s in line.split("   ")]
	numbers = [int(s) for s in strings]
	result += sum(numbers)
print(result)
