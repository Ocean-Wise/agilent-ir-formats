import pandas as pd
import numpy as np

# Load results
df = pd.read_csv('simplified_particle_results.csv')

# Basic statistics
total_particles = len(df)
small_particles = len(df[df['polymer'] == 'small particle'])
identified_particles = total_particles - small_particles

print(f'Total particles found: {total_particles}')
print(f'Small particles filtered: {small_particles} ({small_particles/total_particles*100:.1f}%)')
print(f'Particles analyzed: {identified_particles} ({identified_particles/total_particles*100:.1f}%)')
print()

# Confidence analysis
high_conf = len(df[df['best_pr'] >= 0.3])
low_conf = len(df[(df['best_pr'] > 0) & (df['best_pr'] < 0.3)])
no_conf = len(df[df['best_pr'] == 0.0])

print('Confidence levels:')
print(f'High confidence (≥0.3): {high_conf} particles')
print(f'Low confidence (0-0.3): {low_conf} particles')
print(f'No confidence (=0.0): {no_conf} particles')
print()

# Top polymers (excluding small particles)
top_polymers = df[df['polymer'] != 'small particle'].copy()
top_polymers['polymer_clean'] = top_polymers['polymer'].str.replace(' \\(low confidence\\)', '', regex=True)
polymer_counts = top_polymers['polymer_clean'].value_counts().head(10)

print('Top 10 polymers identified:')
for polymer, count in polymer_counts.items():
    high_conf_count = len(top_polymers[(top_polymers['polymer_clean'] == polymer) & (top_polymers['best_pr'] >= 0.3)])
    print(f'{polymer}: {count} total ({high_conf_count} high confidence)')

print()
print('Particle size distribution:')
sizes = df[df['polymer'] != 'small particle']['pixel_count']
if len(sizes) > 0:
    print(f'Average particle size: {sizes.mean():.0f} pixels')
    print(f'Median particle size: {sizes.median():.0f} pixels')
    print(f'Largest particle: {sizes.max()} pixels')
    print(f'Smallest analyzed particle: {sizes.min()} pixels')
else:
    print('No particle size data available')