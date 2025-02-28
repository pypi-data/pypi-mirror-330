import matplotlib.pyplot as plt
import numpy as np
import pickle
from matplotlib.colors import to_rgba, to_hex


def blend_color(color, alpha, bg_color='#ffffff'):
    """Blend a color with a background color based on alpha."""
    c = np.array(to_rgba(color))
    bg = np.array(to_rgba(bg_color))
    return to_hex((1 - alpha) * bg[:3] + alpha * c[:3])


def plot_combined_ce():
    # Load data
    ms2_ce = pickle.load(open('ms2_ce.pkl', 'rb'))
    ms1_ce_0ev = pickle.load(open('ms1_ce_0ev.pkl', 'rb'))
    ms1_ce_10ev = pickle.load(open('ms1_ce_10ev.pkl', 'rb'))

    # Set up colors
    # colors = ['#56648a', '#6280a5', '#8ca5c0', '#8d7e95', '#ca9a96', '#facaa9']
    base_colors = ['#8d7e95', '#ca9a96', '#56648a']
    alphas = [0.3, 0.7, 0.6]

    # Blend colors
    colors = [blend_color(color, alpha) for color, alpha in zip(base_colors, alphas)]

    # Create plot
    plt.figure(figsize=(4.5, 3))

    # Plot histograms
    plt.hist(ms2_ce, bins=np.arange(0, 75, 10), color=colors[0], label='MS/MS')

    plt.hist(ms1_ce_10ev, bins=np.arange(0, 75, 10), color=colors[2], label='MS1 (10 eV)')
    plt.hist(ms1_ce_0ev, bins=np.arange(0, 75, 10), color=colors[1], label='MS1 (0 eV)')

    # Calculate histograms
    bins = np.arange(0, 75, 10)
    hist_ms2, _ = np.histogram(ms2_ce, bins=bins)
    hist_ms1_0ev, _ = np.histogram(ms1_ce_0ev, bins=bins)
    hist_ms1_10ev, _ = np.histogram(ms1_ce_10ev, bins=bins)

    # Plot upper edges of histograms
    # plt.plot(bins[:-1] + 5, hist_ms2, color=base_colors[0], alpha=1, label='MS/MS', linewidth=1.75)
    # plt.plot(bins[:-1] + 5, hist_ms1_0ev, color=base_colors[1], alpha=1, label='MS1 (0 eV)', linewidth=1.75)
    # plt.plot(bins[:-1] + 5, hist_ms1_10ev, color=base_colors[2], alpha=1, label='MS1 (10 eV)', linewidth=1.75)

    # Plot upper edges of histograms with horizontal and vertical lines
    for i, (hist, color, label) in enumerate(zip([hist_ms2, hist_ms1_0ev, hist_ms1_10ev],
                                                 base_colors,
                                                 ['MS/MS', 'MS1 (0 eV)', 'MS1 (10 eV)'])):
        for j in range(len(bins) - 1):
            plt.plot([bins[j], bins[j + 1]], [hist[j], hist[j]], color=color, linewidth=1.5)
            if j < len(bins) - 2:
                plt.plot([bins[j + 1], bins[j + 1]], [hist[j], hist[j + 1]], color=color, linewidth=1.75)

        # Add a label for the legend
        plt.plot([], [], color=color, linewidth=1.75, label=f'{label} (upper edge)')

    # Set title and labels
    plt.title('Normalized collision energies of annotations', fontname='Arial', fontsize=14, pad=10)
    plt.xlabel('NCE (%)', fontname='Arial', fontsize=12, labelpad=5)
    plt.ylabel('Frequency', fontname='Arial', fontsize=12, labelpad=8)

    # Set limits
    plt.xlim(-2, 70)
    plt.ylim(-3, 65)

    # Adjust frame and ticks
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color('0.4')

    ax.tick_params(axis='both', which='major', labelsize=10, color='0.4', length=2, width=1, pad=4)

    # Set tick label font
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontname('Arial')

    # Add legend for only the histogram bars
    legend_elements = [plt.Rectangle((0, 0), 1, 1, color=colors[i], label=label)
                       for i, label in enumerate(['MS/MS', 'MS1 (0 eV)', 'MS1 (10 eV)'])]
    plt.legend(handles=legend_elements, prop={'family': 'Arial', 'size': 10})

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('combined_ce_histogram.svg', transparent=True)
    plt.show()


if __name__ == '__main__':
    plot_combined_ce()