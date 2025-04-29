import pandas as pd

csv_file = 'open-plaques-gb-2021-05-14 partial fix.csv'  # replace with your real file path
df = pd.read_csv(csv_file)

# Drop missing colour entries
colours = df['colour'].dropna().unique()

# Clean and sort
cleaned_colours = sorted([c.strip() for c in colours if c.strip() != ''])

print("Unique plaque colours found:")
for colour in cleaned_colours:
    print("-", colour)
