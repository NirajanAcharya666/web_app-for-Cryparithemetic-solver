from flask import Flask, render_template, request

app = Flask(__name__)

def find_value(word, assigned):
    num = 0
    for char in word:
        num = num * 10 + assigned[char]
    return num

def is_valid_assignment(word1, word2, result, assigned):
    if assigned[word1[0]] == 0 or assigned[word2[0]] == 0 or assigned[result[0]] == 0:
        return False
    return True

def _solve(word1, word2, result, letters, assigned, solutions):
    if not letters:
        if is_valid_assignment(word1, word2, result, assigned):
            num1 = find_value(word1, assigned)
            num2 = find_value(word2, assigned)
            num_result = find_value(result, assigned)
            if num1 + num2 == num_result:
                solutions.append((f'{num1} + {num2} = {num_result}', assigned.copy()))
        return

    for num in range(10):
        if num not in assigned.values():
            cur_letter = letters.pop()
            assigned[cur_letter] = num
            _solve(word1, word2, result, letters, assigned, solutions)
            assigned.pop(cur_letter)
            letters.append(cur_letter)

def solve(word1, word2, result):
    letters = sorted(set(word1) | set(word2) | set(result))
    if len(result) > max(len(word1), len(word2)) + 1 or len(letters) > 10:
        return None  # Return None if there are no solutions

    solutions = []
    _solve(word1, word2, result, letters, {}, solutions)
    if solutions:
        formatted_solutions = []
        for soln in solutions:
            formatted_solutions.append(f'{soln[0]}\t{soln[1]}')
        return formatted_solutions
    else:
        return None  # Return None if there are no solutions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_puzzle():
    word1 = request.form['word1'].upper()
    word2 = request.form['word2'].upper()
    result = request.form['result'].upper()

    if not word1.isalpha() or not word2.isalpha() or not result.isalpha():
        return render_template('index.html', error='Inputs should only consist of alphabets.')

    solutions = solve(word1, word2, result)
    if solutions is not None:
        return render_template('index.html', solutions_list=solutions)
    else:
        return render_template('index.html', error='No solutions found.')

if __name__ == '__main__':
    app.run(debug=True)
