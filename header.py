from flask import Flask, request, render_template_string, send_file
import io

app = Flask(__name__)

# HTML template for the form with dropdowns for positions
form_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QP Header Authoring Template</title>
    <style>
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        select, input, textarea { width: 200px; padding: 5px; }
    </style>
</head>
<body>
    <h1>Create Question Paper Header</h1>
    <form method="POST">
        <div class="form-group">
            <h2>Logo Details</h2>
            <label>Logo File Path:</label><br>
            <input type="text" name="logo_path" value="./downloads/faps.jpeg" required><br><br>
            <label>Width (px):</label><br>
            <select name="logo_width">
                <option value="100px">100px (Default)</option>
                <option value="80px">80px</option>
                <option value="120px">120px</option>
            </select><br><br>
            <label>Margin Right (px):</label><br>
            <select name="logo_margin_right">
                <option value="20px">20px (Default)</option>
                <option value="10px">10px</option>
                <option value="30px">30px</option>
            </select><br><br>
            <label>Position:</label><br>
            <select name="logo_position">
                <option value="left">left (Default)</option>
                <option value="top-center">top-center</option>
                <option value="right">right</option>
            </select>
        </div>

        <div class="form-group">
            <h2>Title Details (3 Lines)</h2>
            <label>Line 1 Text (e.g., School Name):</label><br>
            <input type="text" name="title_line1" value="THE FRANK ANTHONY PUBLIC SCHOOL, BENGALURU" required><br>
            <label>Font Size:</label><br>
            <select name="title_font_size1">
                <option value="24px">24px (Default)</option>
                <option value="20px">20px</option>
                <option value="28px">28px</option>
            </select><br>
            <label>Font Weight:</label><br>
            <select name="title_font_weight1">
                <option value="bold">bold (Default)</option>
                <option value="normal">normal</option>
                <option value="600">600</option>
            </select><br><br>

            <label>Line 2 Text (e.g., Examination Name):</label><br>
            <input type="text" name="title_line2" value="FIRST TERM EXAMINATION – 2025" required><br>
            <label>Font Size:</label><br>
            <select name="title_font_size2">
                <option value="20px">20px (Default)</option>
                <option value="18px">18px</option>
                <option value="22px">22px</option>
            </select><br><br>

            <label>Line 3 Text (e.g., Subject):</label><br>
            <input type="text" name="title_line3" value="BUSINESS STUDIES" required><br>
            <label>Font Size:</label><br>
            <select name="title_font_size3">
                <option value="20px">20px (Default)</option>
                <option value="18px">18px</option>
                <option value="22px">22px</option>
            </select><br>
            <label>Text Decoration:</label><br>
            <select name="title_text_decoration3">
                <option value="underline">underline (Default)</option>
                <option value="none">none</option>
                <option value="overline">overline</option>
            </select><br><br>
            <label>Position:</label><br>
            <select name="title_position">
                <option value="right">right (Default)</option>
                <option value="top-center">top-center</option>
                <option value="left">left</option>
            </select>
        </div>

        <div class="form-group">
            <h2>Exam Details</h2>
            <label>Grade:</label><br>
            <input type="text" name="grade" value="11" required><br><br>
            <label>Date:</label><br>
            <input type="text" name="date" value="18-09-2025" required><br><br>
            <label>Time:</label><br>
            <input type="text" name="time" value="3 hours" required><br><br>
            <label>Max Marks:</label><br>
            <input type="text" name="max_marks" value="80" required><br><br>
            <label>Table Border Style:</label><br>
            <select name="table_border_style">
                <option value="none">none (Default)</option>
                <option value="1px solid black">1px solid black</option>
                <option value="2px dashed black">2px dashed black</option>
            </select><br>
            <label>Padding (px):</label><br>
            <select name="table_padding">
                <option value="8px">8px (Default)</option>
                <option value="5px">5px</option>
                <option value="10px">10px</option>
            </select><br><br>
            <label>Position:</label><br>
            <select name="exam_position">
                <option value="below-title">below-title (Default)</option>
                <option value="top-center">top-center</option>
                <option value="below-instructions">below-instructions</option>
            </select>
        </div>

        <div class="form-group">
            <h2>Instructions</h2>
            <label>Instructions (bulleted, one per line):</label><br>
            <textarea name="instructions" rows="10" required>- • The answers to this paper must be written on the BOOKLET provided separately.
- • You will not be allowed to write in the first 15 minutes. This time is to be spent in
- reading the question paper.
- • The intended marks for the questions or parts of the question are given in ().
- • Time given at the head of the paper is the time allowed for writing the paper.
- • Question paper is divided into three sections: Section A, Section B and Section C.
- • All questions are compulsory. Internal choices have been provided in two questions
- in Section B and in one question in Section C.
- • This paper consists of 6 printed sides</textarea><br><br>
            <label>Border Bottom Style:</label><br>
            <select name="instructions_border_bottom">
                <option value="1px solid black">1px solid black (Default)</option>
                <option value="none">none</option>
                <option value="2px dotted black">2px dotted black</option>
            </select><br>
            <label>Padding (px):</label><br>
            <select name="instructions_padding">
                <option value="10px">10px (Default)</option>
                <option value="5px">5px</option>
                <option value="15px">15px</option>
            </select><br><br>
            <label>Position:</label><br>
            <select name="instructions_position">
                <option value="below-exam">below-exam (Default)</option>
                <option value="top-center">top-center</option>
                <option value="below-title">below-title</option>
            </select>
        </div>

        <input type="submit" value="Generate HTML">
    </form>
</body>
</html>
'''

# Template for generated HTML with dynamic positioning
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Question Paper Header</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            text-align: center;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            border: none;
        }}
        {header_style}
        .logo {{
            width: {logo_width};
            height: auto;
            margin-right: {logo_margin_right};
        }}
        .title {{
            font-size: {title_font_size1};
            font-weight: {title_font_weight1};
            margin: 0;
        }}
        .subtitle {{
            font-size: {title_font_size2};
            margin: 5px 0;
        }}
        .subject {{
            font-size: {title_font_size3};
            margin: 5px 0;
            text-decoration: {title_text_decoration3};
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            border: none;
            padding: {table_padding};
            text-align: center;
            border-bottom: {table_border_style};
        }}
        .instructions {{
            border-bottom: {instructions_border_bottom};
            text-align: left;
            padding: {instructions_padding};
        }}
        ul {{
            padding-left: 20px;
            margin: 0;
        }}
        li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        {logo_html}
        {title_html}
        {exam_html}
        {instructions_html}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract form data
        logo_path = request.form['logo_path']
        logo_width = request.form['logo_width']
        logo_margin_right = request.form['logo_margin_right']
        logo_position = request.form['logo_position']
        title_line1 = request.form['title_line1']
        title_font_size1 = request.form['title_font_size1']
        title_font_weight1 = request.form['title_font_weight1']
        title_line2 = request.form['title_line2']
        title_font_size2 = request.form['title_font_size2']
        title_line3 = request.form['title_line3']
        title_font_size3 = request.form['title_font_size3']
        title_text_decoration3 = request.form['title_text_decoration3']
        title_position = request.form['title_position']
        grade = request.form['grade']
        date = request.form['date']
        time = request.form['time']
        max_marks = request.form['max_marks']
        table_border_style = request.form['table_border_style']
        table_padding = request.form['table_padding']
        exam_position = request.form['exam_position']
        instructions = request.form['instructions']
        instructions_border_bottom = request.form['instructions_border_bottom']
        instructions_padding = request.form['instructions_padding']
        instructions_position = request.form['instructions_position']

        # Convert instructions to HTML list items
        instructions_lines = instructions.split('\n')
        instructions_html_content = ''.join(f'<li>{line.strip()}</li>' for line in instructions_lines if line.strip())

        # Generate HTML based on positions
        header_style = ''
        logo_html = ''
        title_html = ''
        exam_html = ''
        instructions_html = ''

        if logo_position == 'left' and title_position == 'right':
            header_style = '''
                .header-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 10px;
                }
                .logo-cell {
                    width: 100px;
                    vertical-align: top;
                    border: none;
                }
                .title-cell {
                    vertical-align: top;
                    border: none;
                    text-align: center;
                }
            '''
            logo_html = '<table class="header-table"><tr><td class="logo-cell"><img src="{logo_path}" alt="School Logo" class="logo"></td>'.format(logo_path=logo_path)
            title_html = '<td class="title-cell"><div class="title">{title_line1}</div><div class="subtitle">{title_line2}</div><div class="subject">{title_line3}</div></td></tr></table>'.format(
                title_line1=title_line1, title_line2=title_line2, title_line3=title_line3)
        elif logo_position == 'top-center' and title_position == 'top-center':
            header_style = '''
                .header {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 10px;
                    border-bottom: 1px solid black;
                }
            '''
            logo_html = '<div class="header"><img src="{logo_path}" alt="School Logo" class="logo"></div>'.format(logo_path=logo_path)
            title_html = '<div class="header"><div class="title">{title_line1}</div><div class="subtitle">{title_line2}</div><div class="subject">{title_line3}</div></div>'.format(
                title_line1=title_line1, title_line2=title_line2, title_line3=title_line3)
        # Add more position combinations as needed (e.g., logo right/title left)

        if exam_position == 'below-title':
            exam_html = '<table>{exam_table}</table>'.format(exam_table='<tr><td>Grade: {grade}<br>Date: {date}</td><td>Time: {time}<br>Max Marks: {max_marks}</td></tr>'.format(
                grade=grade, date=date, time=time, max_marks=max_marks))
        elif exam_position == 'below-instructions':
            instructions_html = '<div class="instructions"><ul>{instructions_html}</ul></div>'.format(instructions_html=instructions_html_content) + \
                              '<table>{exam_table}</table>'.format(exam_table='<tr><td>Grade: {grade}<br>Date: {date}</td><td>Time: {time}<br>Max Marks: {max_marks}</td></tr>'.format(
                                  grade=grade, date=date, time=time, max_marks=max_marks))
        else:  # top-center
            exam_html = '<table style="margin-top: 0;">{exam_table}</table>'.format(exam_table='<tr><td>Grade: {grade}<br>Date: {date}</td><td>Time: {time}<br>Max Marks: {max_marks}</td></tr>'.format(
                grade=grade, date=date, time=time, max_marks=max_marks))

        if instructions_position == 'below-exam':
            instructions_html = '<div class="instructions"><ul>{instructions_html}</ul></div>'.format(instructions_html=instructions_html_content)
        elif instructions_position == 'below-title':
            instructions_html = '<div class="instructions"><ul>{instructions_html}</ul></div>'.format(instructions_html=instructions_html_content) + exam_html
            exam_html = ''
        else:  # top-center
            instructions_html = '<div class="instructions" style="margin-top: 0;"><ul>{instructions_html}</ul></div>'.format(instructions_html=instructions_html_content)

        # Generate final HTML
        generated_html = html_template.format(
            header_style=header_style,
            logo_path=logo_path,
            logo_width=logo_width,
            logo_margin_right=logo_margin_right,
            title_line1=title_line1,
            title_font_size1=title_font_size1,
            title_font_weight1=title_font_weight1,
            title_line2=title_line2,
            title_font_size2=title_font_size2,
            title_line3=title_line3,
            title_font_size3=title_font_size3,
            title_text_decoration3=title_text_decoration3,
            grade=grade,
            date=date,
            time=time,
            max_marks=max_marks,
            table_border_style=table_border_style,
            table_padding=table_padding,
            instructions_border_bottom=instructions_border_bottom,
            instructions_padding=instructions_padding,
            logo_html=logo_html,
            title_html=title_html,
            exam_html=exam_html,
            instructions_html=instructions_html  # Corrected to use once
        )

        # Save to a BytesIO object and send as file
        html_file = io.BytesIO(generated_html.encode('utf-8'))
        html_file.seek(0)
        return send_file(html_file, as_attachment=True, download_name='qp_header.html', mimetype='text/html')

    return render_template_string(form_template)

if __name__ == '__main__':
    app.run(debug=True)
