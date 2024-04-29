
######  Visualisation 1

import pandas as pd
import matplotlib.pyplot as plt
balanced_data = pd.read_csv('balancedMH.csv')
 
# Ensure 'Growing_Stress' is a categorical type with a specific order

categories = ['No', 'Maybe', 'Yes']

balanced_data['Growing_Stress'] = pd.Categorical(
    balanced_data['Growing_Stress'], 
    categories=categories, 
    ordered=True
)
 
# Group the data by 'Growing_Stress' and 'Gender' and calculate the count
grouped = balanced_data.groupby(['Growing_Stress', 'Gender']).size().unstack()
 
# Define the colours for the bars
colours = {'Male': '#1f77b4', 'Female': '#ff7f0e'}  # Darker blue for Male, Muted orange for Female
 
# Create a bar chart for each gender with the specified colors
ax = grouped.plot(kind='bar', color=[colours[gender] for gender in grouped.columns], figsize=(10, 6), edgecolor='black')
 
# Customize the plot
ax.set_title('Relationship between Growing Stress and Gender')
ax.set_xlabel('Growing Stress Response')
ax.set_ylabel('Frequency')
ax.set_ylim(bottom=12000)  # Set the y-axis to start at 10,000
plt.xticks(rotation=0)  # Horizontal x-axis labels
plt.legend(title='Gender')
 
# Show the plot
plt.tight_layout()
plt.show()
 
##### Visualisation 2 

import pandas as pd
import matplotlib.pyplot as plt
 
balanced_data = pd.read_csv('balancedMH.csv')
balanced_data['Growing_Stress'] = pd.Categorical(
    balanced_data['Growing_Stress'],
    categories=['No', 'Maybe', 'Yes'],
    ordered=True)
 
# Group the data by 'Growing_Stress' and 'Occupation' for all genders
grouped_data = balanced_data.groupby(['Growing_Stress', 'Occupation']).size().reset_index(name='Count')
 
# Pivot the data to get 'Occupation' as columns, 'Growing_Stress' as rows, and 'Count' as values
pivot_data = grouped_data.pivot(index='Growing_Stress', columns='Occupation', values='Count')
 
# Plotting the grouped bar chart
pivot_data.plot(kind='bar', figsize=(12, 8), stacked=False, edgecolor='black')
 
# Adding title and labels
plt.title('Grouped Distribution of Growing Stress Responses by Occupation')
plt.xlabel('Growing Stress Response')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.ylim(5000, None) 
plt.legend(title='Occupation', bbox_to_anchor=(1.05, 1), loc='upper left')
 
# Display the plot
plt.tight_layout()
plt.show()

####### Visualisation 3:
 
import pandas as pd
import matplotlib.pyplot as plt
 
balanced_data = pd.read_csv('balancedMH.csv')
 
# Group the data by 'Occupation' and 'Gender'
occupation_gender_counts = balanced_data.groupby(['Occupation', 'Gender']).size().unstack()
 
# Create pie charts for each gender
fig, axes = plt.subplots(1, len(occupation_gender_counts.columns), figsize=(14, 7))  
for i, gender in enumerate(occupation_gender_counts.columns):
    ax = axes[i]
    wedges, texts, autotexts = ax.pie(occupation_gender_counts[gender], autopct='%1.2f%%', startangle=90,
                                      colors=plt.cm.Paired(range(len(occupation_gender_counts))), wedgeprops={'edgecolor': 'black'})
    plt.setp(autotexts, fontsize=12)
    ax.set_ylabel('')  
    ax.set_title(f'Occupation Distribution for {gender}', fontsize=16)
 
# Create the legend outside of the last pie chart
axes[-1].legend(wedges, occupation_gender_counts.index, title="Occupations", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
 
# Customise the overall layout
plt.suptitle('Occupation Distribution by Gender', fontsize=18)
 
# Show the plot
plt.show()

##### Visualisation 4
 
import pandas as pd
import matplotlib.pyplot as plt
 
data = pd.read_csv('balancedMH.csv')
 
# Convert 'Growing_Stress' and 'Changes_Habits' to categorical types with the order 'No', 'Maybe', 'Yes'
data['Growing_Stress'] = pd.Categorical(data['Growing_Stress'], categories=['No', 'Maybe', 'Yes'], ordered=True)
data['Changes_Habits'] = pd.Categorical(data['Changes_Habits'], categories=['No', 'Maybe', 'Yes'], ordered=True)
data['Gender'] = pd.Categorical(data['Gender'], categories=['Male', 'Female'], ordered=True)
 
# Separate the data for males and females
data_male = data[data['Gender'] == 'Male']
data_female = data[data['Gender'] == 'Female']
 
# Group the data by 'Growing_Stress' and 'Changes_Habits' and count the occurrences for each gender
grouped_data_male_counts = data_male.groupby(['Growing_Stress', 'Changes_Habits']).size().unstack(fill_value=0)
grouped_data_female_counts = data_female.groupby(['Growing_Stress', 'Changes_Habits']).size().unstack(fill_value=0)
 
# Calculate the percentages for the internal stacks
male_percentages = grouped_data_male_counts.divide(grouped_data_male_counts.sum(axis=1), axis=0) * 100
female_percentages = grouped_data_female_counts.divide(grouped_data_female_counts.sum(axis=1), axis=0) * 100
 
# Define colors for each 'Changes_Habits' category
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
 
# Create the plots with bar heights and percentages
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6), sharey=True)

# Function to add percentage labels within the bars
def add_percentage_labels(ax, data_counts, data_percentages):
    for i, bar_container in enumerate(ax.containers):
        for bar, count, percentage in zip(bar_container, data_counts.iloc[:, i], data_percentages.iloc[:, i]):
            ax.text(bar.get_x() + bar.get_width() / 2, 
                    bar.get_y() + bar.get_height() / 2, 
                    f'{percentage:.1f}%', 
                    ha='center', va='center', color='white', fontsize=10)
 
# Plot for males
grouped_data_male_counts.plot(kind='bar', stacked=True, color=colors, ax=axes[0], edgecolor='black', width=0.4)
axes[0].set_ylabel('Number of Respondents')
axes[0].set_title('Male')
axes[0].set_xlabel('Growing Stress')
add_percentage_labels(axes[0], grouped_data_male_counts, male_percentages)
 
# Plot for females
grouped_data_female_counts.plot(kind='bar', stacked=True, color=colors, ax=axes[1], edgecolor='black', width=0.4)
axes[1].set_title('Female')
axes[1].set_xlabel('Growing Stress')
add_percentage_labels(axes[1], grouped_data_female_counts, female_percentages)
fig.suptitle('Stacked Bar Chart of Growing Stress and Changes in Habits by Gender', fontsize=16)
 
# Adjust layout
plt.tight_layout(rect=[0.1, 0.04, 0.85, 1])
 
# Show the plot
plt.show()

##### Visualisation 5 
 
import pandas as pd
import matplotlib.pyplot as plt
 
data = pd.read_csv('balancedMH.csv')
 
# Convert 'Growing_Stress' and 'Coping_Struggles' to categorical types with the order 'No', 'Maybe', 'Yes'
data['Growing_Stress'] = pd.Categorical(data['Growing_Stress'], categories=['No', 'Maybe', 'Yes'], ordered=True)
data['Coping_Struggles'] = pd.Categorical(data['Coping_Struggles'], categories=['No', 'Yes'], ordered=True)
 
# Generate pivot table
pivot_table = data.pivot_table(index=['Gender', 'Growing_Stress'], columns='Coping_Struggles', aggfunc='size', fill_value=0)
 
# Reset the index so we can have 'Gender' and 'Growing_Stress' as normal columns
pivot_table_reset = pivot_table.reset_index()
pivot_table_sorted = pivot_table_reset.sort_values(by=['Gender', 'Growing_Stress'])
 
# Plotting the grouped bar chart
fig, ax = plt.subplots(figsize=(10, 6))
 
# Recalculate x since we sorted the pivot_table
x = range(len(pivot_table_sorted))
 
# Bar width for the grouped bar chart
bar_width = 0.35

# Colours for the bars to match other graphs
colours = ['#1f77b4', '#ff7f0e']  # Blue for "No", Orange for "Yes"
 
# Plot the bars for 'No' and 'Yes' coping struggles
no_bars = ax.bar(x, pivot_table_sorted[('No')], bar_width, label='No', color=colours[0], edgecolor='black')
yes_bars = ax.bar([p + bar_width for p in x], pivot_table_sorted[('Yes')], bar_width, label='Yes', color=colours[1], edgecolor='black')
 
# Set labels and title
ax.set_xlabel('Gender and Growing Stress')
ax.set_ylabel('Number of Respondents')
ax.set_title('Growing Stress and Coping Struggles')
 
# Set x axis labels
ax.set_xticks([p + bar_width / 2 for p in x])
ax.set_xticklabels([f'{gender}\n{stress}' for gender, stress in pivot_table_sorted[['Gender', 'Growing_Stress']].values])
 
# Set y-axis to start from 6000 and grid lines every 1000 respondents
ax.set_ylim(bottom=6000)
ax.yaxis.set_major_locator(plt.MultipleLocator(1000))
ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.7)
 
# Add legend 
ax.legend(title="Coping Struggles")
 
# Show the plot
plt.show()