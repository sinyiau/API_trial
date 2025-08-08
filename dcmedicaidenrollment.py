import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import squarify

# --- 1. Data Preparation (Consistent with previous steps) ---
# Data based on the user's provided image (using 2025-06 prelim numbers)
data = {
    'Category': [
        'Childless adult (0%-133% FPL)', 'Childless adult (134%-210% FPL)',
        'Child (non-CHIP)', 'Parent/caretaker', 'Child (CHIP)',
        'Elderly and Persons with Physical Disabilities',
        'Long term services and supports non-waiver',
        'Long term services and supports developmental disabilities',
        'Aged, blind or disabled (Supplemental Security)',
        'Qualified Medicare Beneficiary Program', 'Aged, blind or disabled (others)',
        'Incarcerated', 'Pregnant woman', 'Others'
    ],
    'Enrollment': [
        128578, 16099, 73725, 35060, 17486, 6203, 3026, 1919,
        71756, 12066, 7381, 1011, 823, 219
    ]
}
df = pd.DataFrame(data)

# Assign risk levels
risk_map = {
    'Childless adult (0%-133% FPL)': 'High Risk',
    'Childless adult (134%-210% FPL)': 'Medium Risk', 'Child (non-CHIP)': 'Medium Risk', 'Parent/caretaker': 'Medium Risk',
    'Child (CHIP)': 'Medium Risk', 'Elderly and Persons with Physical Disabilities': 'Medium Risk',
    'Long term services and supports non-waiver': 'Medium Risk', 'Long term services and supports developmental disabilities': 'Medium Risk',
    'Aged, blind or disabled (Supplemental Security)': 'Low Risk / Exempt', 'Qualified Medicare Beneficiary Program': 'Low Risk / Exempt',
    'Aged, blind or disabled (others)': 'Low Risk / Exempt', 'Incarcerated': 'Low Risk / Exempt',
    'Pregnant woman': 'Low Risk / Exempt', 'Others': 'Low Risk / Exempt'
}
df['Risk Level'] = df['Category'].map(risk_map)

# Summarize data
risk_summary = df.groupby('Risk Level')['Enrollment'].sum().reindex(['High Risk', 'Medium Risk', 'Low Risk / Exempt'])
total_enrollment = risk_summary.sum()

colors = {'High Risk': '#d62728', 'Medium Risk': '#ff7f0e', 'Low Risk / Exempt': '#2ca02c'}

# --- 2. Generate Chart 1: Treemap ---
plt.figure(figsize=(12, 8))
squarify.plot(sizes=risk_summary.values, 
              label=[f"{name}\n{val:,.0f} people\n({val/total_enrollment:.0%})" for name, val in risk_summary.items()],
              color=[colors[name] for name in risk_summary.index],
              text_kwargs={'fontsize': 14, 'color': 'white', 'fontweight': 'bold'})
plt.title('方案一：樹狀圖 (Treemap) - 「衝擊的剖析」\nOption 1: The Treemap - "Anatomy of Impact"', fontsize=16, pad=20)
plt.axis('off')
plt.tight_layout()
plt.savefig('treemap.png')
plt.close()

# --- 3. Generate Chart 2: Deconstructed Bar Chart ---
fig, ax = plt.subplots(figsize=(10, 8))

# Data for the two bars
affected_high = risk_summary['High Risk']
affected_medium = risk_summary['Medium Risk']
low_risk = risk_summary['Low Risk / Exempt']
total_affected = affected_high + affected_medium

# Plotting the "Affected" bar (stacked)
ax.bar('Potentially Affected\n(受潛在影響群體)', affected_high, color=colors['High Risk'], label='High Risk (高風險)')
ax.bar('Potentially Affected\n(受潛在影響群體)', affected_medium, bottom=affected_high, color=colors['Medium Risk'], label='Medium Risk (中度風險)')

# Plotting the "Low Risk" bar
ax.bar('Low Risk / Exempt\n(低風險/豁免群體)', low_risk, color=colors['Low Risk / Exempt'], label='Low Risk / Exempt (低風險)')

# Annotations and formatting
ax.set_ylabel('Number of Enrollees (受益人數)')
ax.set_title('方案二：解構式條形圖 - 「一個被分割的城市」\nOption 2: The Deconstructed Bar - "A City Divided"', fontsize=16, pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Prominent number annotation
ax.text(0, total_affected, f'{total_affected:,.0f}\nPeople', ha='center', va='bottom', fontsize=18, fontweight='bold')
ax.text(0, affected_high / 2, f'{affected_high:,.0f}\nHigh Risk', ha='center', va='center', color='white', fontweight='bold')
ax.text(0, affected_high + affected_medium / 2, f'{affected_medium:,.0f}\nMedium Risk', ha='center', va='center', color='white', fontweight='bold')
ax.text(1, low_risk / 2, f'{low_risk:,.0f}\nLow Risk', ha='center', va='center', color='white', fontweight='bold')

ax.legend(frameon=False, loc='upper right')
plt.tight_layout()
plt.savefig('deconstructed_bar.png')
plt.close()

# --- 4. Generate Chart 3: Annotated Number Block ---
fig_num, ax_num = plt.subplots(figsize=(10, 8), facecolor='white')
ax_num.axis('off')

# The main number and text
total_affected = risk_summary['High Risk'] + risk_summary['Medium Risk']
ax_num.text(0.5, 0.6, f'{total_affected:,.0f}', ha='center', va='center', fontsize=100, fontweight='bold')
ax_num.text(0.5, 0.5, '是在H.R. 1法案下面臨醫療保障風險的華盛頓特區居民人數\nDC residents facing healthcare coverage risks under H.R. 1', 
            ha='center', va='top', fontsize=16, wrap=True)

# Mini donut chart for context
risk_proportions = risk_summary.values
risk_labels = risk_summary.index
risk_colors = [colors[name] for name in risk_labels]

ax_donut = fig_num.add_axes([0.4, 0.2, 0.2, 0.2])
ax_donut.pie(risk_proportions, colors=risk_colors, startangle=90, counterclock=False,
             wedgeprops={'width': 0.4, 'edgecolor': 'white'})

# Legend for donut
legend_text = [
    f'High Risk (高風險): {risk_summary["High Risk"]/total_enrollment:.0%}',
    f'Medium Risk (中度風險): {risk_summary["Medium Risk"]/total_enrollment:.0%}',
    f'Low Risk (低風險): {risk_summary["Low Risk / Exempt"]/total_enrollment:.0%}'
]
ax_num.text(0.5, 0.1, '\n'.join(legend_text), ha='center', va='center', fontsize=12)

fig_num.suptitle('方案三：重點數據註解 - 「最純粹的震撼」\nOption 3: The Annotated Number - "The Headline Figure"', fontsize=16, y=0.95)

plt.savefig('annotated_number.png')
plt.close()