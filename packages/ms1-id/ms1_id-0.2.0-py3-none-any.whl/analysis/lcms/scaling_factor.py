import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

def exp_scaling(normalized_mz, growth_rate=10.0):
    return np.exp(growth_rate * normalized_mz)

# Generate normalized m/z values
normalized_mz = np.linspace(0, 1, 1000)

# Calculate scaling factors
exp_factors = exp_scaling(normalized_mz, 10.0)

# Set the font to Arial
plt.rcParams['font.family'] = 'Arial'

# Create the plot
fig, ax = plt.subplots(figsize=(2.85, 2))
ax.plot(normalized_mz, exp_factors)

# Set italic 'm/z' in x-label
ax.set_xlabel(r'Normalized $\mathit{m/z}$')
ax.set_ylabel('Scaling factor')

# Use scientific notation for y-axis
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

# Adjust tick length and pad
ax.tick_params(axis='both', which='major', length=2.5, pad=3)

# Set frame color
for spine in ax.spines.values():
    spine.set_edgecolor('0.4')

ax.grid(True, alpha=0.3)  # Make the grid lighter

# Adjust layout to show all elements
plt.tight_layout()

# Save as SVG with transparent background
plt.savefig('plot.svg', format='svg', transparent=True)

plt.show()