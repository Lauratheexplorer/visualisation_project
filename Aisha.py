import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('balancedMH.csv')

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Count values for each category
treatment_counts = data['treatment'].value_counts()

# PIE CHART
# Choosing colours for the pie chart
new_colors = ['#ff9999','#66b3ff']

# Picking what first angle the pie chart will start at
start_angle = 90

# Create a pie chart
plt.figure(figsize=(8, 5))
plt.pie(treatment_counts, labels=treatment_counts.index, autopct='%1.1f%%', 
        colors=new_colors, startangle=start_angle)
plt.title('Pie Chart of Treatment Distribution')
plt.show()

# SORTED BAR CHART
# Calculate the proportion of individuals getting treatment from each country
country_treatment_data = data[['Country', 'treatment']]
country_counts = country_treatment_data['Country'].value_counts()
treatment_counts = country_treatment_data[country_treatment_data['treatment'] == 'Yes']['Country'].value_counts()
treatment_proportion = (treatment_counts / country_counts * 100).dropna()

# Sort the data by proportion for the bar chart
treatment_proportion_sorted = treatment_proportion.sort_values(ascending=False)

# Pick the colour for the bar chart
bar_chart_color = '#aaf0d1'

# Create the plot
plt.figure(figsize=(10, 8))  # Set the figure size
bars = plt.bar(treatment_proportion_sorted.index, treatment_proportion_sorted.values, color=bar_chart_color)
plt.xlabel('Country')  # Label for the x-axis
plt.ylabel('Proportion of Treatment (%)')  # Label for the y-axis
plt.title('Proportion of Individuals Receiving Treatment by Country')  # Title of the chart
plt.xticks(rotation=90)  # Rotate country names for better visibility

# Adding the text annotations on the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')  # Adjust the position as needed

plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
plt.show()

# CLUSTERED BAR CHART
# Convert the 'treatment' column to binary format for calculation (1 for 'Yes', 0 for 'No')
data['Treatment_Binary'] = data['treatment'].apply(lambda x: 1 if x == 'Yes' else 0)

# Pivot the data to get the treatment rates for each gender in each country
treatment_rates_by_gender = data.pivot_table(values='Treatment_Binary', index='Country', columns='Gender', aggfunc='mean')

# Filter out countries with 0 treatment rate for both male and female
filtered_treatment_rates = treatment_rates_by_gender.dropna(how='all', subset=['Male', 'Female'])
filtered_treatment_rates = filtered_treatment_rates[(filtered_treatment_rates['Male'] > 0) | (filtered_treatment_rates['Female'] > 0)]

# Plotting the filtered clustered bar chart with specified colors for Male and Female
ax = filtered_treatment_rates.plot(kind='bar', 
                                   figsize=(15, 8), 
                                   color={'Male': '#0000FF', 'Female': '#FFC0CB'}, 
                                   alpha=0.75, 
                                   legend=True)

# Adding data labels to each bar in the clustered bar chart
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f', label_type='edge')

# Set chart title and labels
plt.title('Treatment Rates by Gender in Each Country (Countries with Zero Treatment Excluded)')
plt.xlabel('Country')
plt.ylabel('Treatment Rate (%)')
plt.xticks(rotation=45)  # Rotate the x labels to show the country names clearly
plt.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left')  # Move the legend out of the plot
plt.tight_layout()  # Adjust layout to fit the rotated x labels and legend
plt.show()

# STACKED BAR CHART
# Preprocessing to focus on relevant columns and create a crosstab
treatment_data = data[['Country', 'treatment', 'family_history']]
treatment_cross_tab = pd.crosstab(index=[treatment_data['Country'], treatment_data['treatment']], 
                                  columns=treatment_data['family_history'], 
                                  margins=False).reset_index()

# Pivot the table for easier plotting
pivot_table = treatment_cross_tab.pivot_table(values=['Yes', 'No'], index='Country', columns='treatment', aggfunc='sum', fill_value=0)

# Filtering out countries with zero total counts across all categories
non_zero_countries = pivot_table.loc[(pivot_table.sum(axis=1) > 0), :]

# Calculating proportions within each country
proportional_data = non_zero_countries.div(non_zero_countries.sum(axis=1), axis=0)

# Plotting
fig, ax = plt.subplots(figsize=(14, 8))
proportional_data.plot(kind='bar', stacked=True, color=['#FFD700', '#FFA500', '#FF4500', '#800080'], figsize=(14, 8), ax=ax)

# Adding percentage labels to each bar
for bars in ax.containers:
    ax.bar_label(bars, fmt='%.1f%%', label_type='center')

plt.title('Proportion of Treatment Rates by Country and Family History of Mental Health (Excluding Zero Count Countries)')
plt.xlabel('Country')
plt.ylabel('Proportion of Individuals')
plt.legend(title='Family History', labels=['No History - No Treatment', 'No History - Treatment', 'History - No Treatment', 'History - Treatment'])
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()