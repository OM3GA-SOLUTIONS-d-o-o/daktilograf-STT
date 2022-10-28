import re
import num2words


with open('input.txt') as f_input:
    text = f_input.read()

text = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), -l sr , text)

with open('output.txt', 'w') as f_output:
    f_output.write(text)