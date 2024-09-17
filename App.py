from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_required_grades(prelim_grade):
    passing_grade = 75
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    grade_range = (0, 100)

    if not (grade_range[0] <= prelim_grade <= grade_range[1]):
        return "Error: Preliminary grade must be between 0 to 100.", None, None, None
    
    current_total = prelim_grade * prelim_weight
    required_total = passing_grade - current_total
    midterm_final_weight = midterm_weight + final_weight
    min_required_average = required_total / midterm_final_weight

    if min_required_average > 100:
        return "Error: It is not possible to achieve the passing grade with this preliminary score.", None, None, None
    
    if min_required_average < grade_range[0]:
        min_required_average = grade_range[0]

    # Determine if the student is qualified for Dean's Lister
    dean_lister_message = ""
    if prelim_grade > 90:
        dean_lister_message = "You are qualified as Dean's Lister, CONGRATULATIONS!"

    # Determine if the student has a chance to pass
    chance_to_pass_message = ""
    if min_required_average <= 100:
        chance_to_pass_message = "You have a chance to pass the course."
    else:
        chance_to_pass_message = "Unfortunately, you do not have a chance to pass the course."

    return round(min_required_average, 2), dean_lister_message, chance_to_pass_message

@app.route('/', methods=['GET', 'POST'])
def index():
    required_grade = None
    dean_lister_message = None
    chance_to_pass_message = None

    if request.method == 'POST':
        try:
            prelim_grade = float(request.form['prelim_grade'])
            required_grade, dean_lister_message, chance_to_pass_message = calculate_required_grades(prelim_grade)
        except ValueError:
            required_grade = "Error: Please enter a valid number."
            dean_lister_message = None
            chance_to_pass_message = None

    return render_template('index.html', required_grade=required_grade,
                           dean_lister_message=dean_lister_message,
                           chance_to_pass_message=chance_to_pass_message)

if __name__ == '__main__':
    app.run(debug=True)
