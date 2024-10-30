import re

dollar = re.compile(r'\$\s*\(?\s*[0-9]+[^A-Za-z\s]*[0-9]*\s*\)?$')
print('dollars regex')
for s in ['$ (0.12)', '$1,234.56', '$(0.12)', '$(1,000.12)', '$(100,123,456.99)', '$ 256', '$256', '$ (460,483)', '$(460,483)', '$ ( 78 )', '(loss)', '$100 per', '$10 per 100', '$(100,00.00a0)', 'we use $100', '$100, 99', '100', '100%']:
    if not dollar.match(s):
        print(f'bad: {s}')
    else:
        print(f'good: {s}')

print()
print('number regex')
number = re.compile(r'\(?\s*[0-9]+[^A-Za-z\s\-%]*[0-9]*\s*\)?$')
for s in ['4', '(4)', '1', '100', '(1,000.12)', '(100,123,456.99)', '100,123,456.99', '(0.12)', '255,958', '(loss)', '100 per', '10 per 100', '100,00.00a0', 'we use 100', '100, 99', '$100', '100%', '1a', '11-1234']:
    if not number.match(s):
        print(f'bad: {s}')
    else:
        print(f'good: {s}')

print()
print('percent regex')
percent = re.compile(r'\(?\s*[0-9]+[^A-Za-z\s]*[0-9]*\s*\)?\s*%\s*\)?$')
for s in ['10%', '1,000%', '100 %', '1,000.23%', '99.99%', '99.99 %', '(23)%', '( 23 ) %', '(23%)', '( 23 % )', '99.99', 'testing at 10%', '100% of', '23 of the %', '(of 23%)', '2 of 3%', '$100', '100', '$100']:
    if not percent.match(s):
        print(f'bad: {s}')
    else:
        print(f'good: {s}')
