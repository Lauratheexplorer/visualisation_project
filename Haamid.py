import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)



####################################################
# Load and drop uwanted columns dataset
df = pd.read_csv('Datasets/balancedMH.csv')
df = df.drop(['Unnamed: 0','Timestamp'], axis=1)
####################################################



####################################################
#Dataset info
'''
RangeIndex: 101716 entries, 0 to 101715
Data columns (total 16 columns):
 #   Column                   Non-Null Count   Dtype
---  ------                   --------------   -----
 0   Gender                   101716 non-null  object
 1   Country                  101716 non-null  object
 2   Occupation               101716 non-null  object
 3   self_employed            101716 non-null  object
 4   family_history           101716 non-null  object
 5   treatment                101716 non-null  object
 6   Days_Indoors             101716 non-null  object
 7   Growing_Stress           101716 non-null  object
 8   Changes_Habits           101716 non-null  object
 9   Mental_Health_History    101716 non-null  object
 10  Mood_Swings              101716 non-null  object
 11  Coping_Struggles         101716 non-null  object
 12  Work_Interest            101716 non-null  object
 13  Social_Weakness          101716 non-null  object
 14  mental_health_interview  101716 non-null  object
 15  care_options             101716 non-null  object

shape() = (101716, 17)
'''
####################################################

# Print all distinct values for each column
def distinct_values_per_column(dataframe):
   for col in dataframe:
    print(col, dataframe[col].unique())

#######################################################################
# Uncomment function calls to display the corresponding visualisation #
#######################################################################


## Visualisation 1 - Plot the distribution of values for specified column name 
def ColumnDistribution(df, columnName):  
    counts = df[columnName].value_counts()
    print("\n", counts)

    # Bar Chart (Number of Entries by Occupation)
    plt.figure(figsize=(10, 6))

    plt.bar(counts.index, counts.values, edgecolor='grey')

    plt.title('Number of Entries by Occupation', fontsize=14)
    plt.xlabel('Occupation', fontsize=12)
    plt.ylabel('Number of Entries', fontsize=12)

    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
    plt.grid(True, linestyle='--', alpha=0.7)  # Add grid lines

    for index, value in enumerate(counts.values):
        plt.text(index, value + 0.2, str(value), horizontalalignment='center', verticalalignment='bottom')  # Add data labels

    plt.tight_layout()


    #################################################
    # Pie Chart of distribution of occupation
    plt.figure(figsize=(10, 6))

    # Plot the pie chart with specified formatting
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
    plt.title('Distribution of Occupation', fontsize=16)

    plt.tight_layout()


    plt.show()
    
#ColumnDistribution(df, 'Occupation')



## Visualisation 2 - People seeking treatment based on occupation
def Occupations_seekingTreatment(dataframe):    
    # Group the data by 'Occupation' and 'treatment' columns and count the occurrences
    occupation_treatment_counts = dataframe.groupby(['Occupation', 'treatment']).size().unstack(fill_value=0)

    # Count of individuals for each occupation
    occupation_totals = occupation_treatment_counts.sum(axis=1)

    # Percentage of individuals seeking and not seeking treatment for each occupation
    occupation_treatment_percentages = occupation_treatment_counts.div(occupation_totals, axis=0) * 100

    print('occupation_treatment_counts\n',occupation_treatment_counts)
    print('occupation_totals\n',occupation_totals)
    print('occupation_treatment_percentages\n',occupation_treatment_percentages)


    # Set up the plot
    plt.figure(figsize=(10, 6))
    
    # Plot a stacked bar chart
    occupation_treatment_percentages.plot(kind='bar', stacked=True, ax=plt.gca())
    
    # Set plot title and labels
    plt.title('Proportion of Individuals Who Have Sought Out Treatment by Occupation')
    plt.xlabel('Occupation')
    plt.ylabel('Percentage')
    plt.xticks(rotation=0, ha='center')
    plt.legend(title='Sought Treatment')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

#Occupations_seekingTreatment(df)



## Visualisation 3 - Growing_Stress by Occupation
def Occupations_growingStress(dataframe):
    # Group the DataFrame by 'Occupation' and 'Growing_Stress' and count the occurrences of each combination
    occupation_stress_counts = dataframe.groupby(['Occupation', 'Growing_Stress']).size().unstack()
    print('Frequency of Growing Stress Responses by Occupation:\n',occupation_stress_counts)    # Print frequency values

    # Plot bar chart with frequencies
    occupation_stress_counts.plot(kind='bar', stacked=False, zorder = 3)
    plt.title('Frequency of Growing Stress Responses by Occupation')
    plt.xlabel('Occupation')
    plt.ylabel('Frequency')
    plt.xticks(rotation = 0)
    plt.legend(title='Growing Stress')
    plt.grid(alpha=0.6, zorder = 0)

    plt.tight_layout()

    # Divide each value in the unstacked DataFrame by the sum of the row to get normalized values
    occupation_stress_norm = occupation_stress_counts.div(occupation_stress_counts.sum(axis=1), axis=0)
    print('Normalized Distribution of Growing Stress by Occupation:\n', occupation_stress_norm)    # Print normalized values

    # Plot bar chart with normalized values
    occupation_stress_norm.plot(kind='bar', stacked=False, zorder = 3)
    plt.title('Distribution of Growing Stress by Occupation (Normalised)')
    plt.xlabel('Occupation')
    plt.ylabel('Proportion')
    plt.xticks(rotation = 0)
    plt.legend(title='Growing Stress')
    plt.grid(alpha=0.6, zorder = 0)


    plt.tight_layout()

    plt.show()

#Occupations_growingStress(df)



# Visualisation 4 - History of Mental health based on days spend indoors, per occupation 
def mentalHealthHistory_grouped(dataframe):  
    # Filter Data by 'Occupation', 'Days_Indoors', and 'Mental_Health_History', then counting the number of respondents for each category
    grouped = dataframe.groupby(['Occupation', 'Days_Indoors', 'Mental_Health_History']).size().reset_index(name='Count')
    pivoted = grouped.pivot_table(index=['Occupation', 'Days_Indoors'], columns='Mental_Health_History', values='Count', fill_value=0)    # 'Days_Indoors' as columns

    proportions = pivoted.div(pivoted.sum(axis=1), axis=0)      # Calculate proportions
    proportions = proportions.reset_index()                     # Reset index to make it flat

    proportions.columns.name = None
    print(proportions)


    ## Plot data
    # Return a list of all unique occupations for each graph to be made for
    occupations_list = dataframe['Occupation'].unique()
    print("Occupations: ", occupations_list)

    # Create a new graph for each occupation stored in the the occupations list.
    for val in occupations_list:
        df_occupation = proportions[proportions['Occupation'] == val]                                               # filter from the large dataframe to a specific occupation given in the occupations_list
        df_occupation = pd.concat([df_occupation.iloc[3:4], df_occupation.iloc[:3], df_occupation.iloc[4:]])        # Move the fourth row to be the first row to reorder the dataframe in days spent indoors
        print(df_occupation)

        x = range(len(df_occupation))               # Calculate the positions for the bars, spacing then out evenly
        fig, ax = plt.subplots(figsize=(10, 6))     # Create the figure and axis objects


        # Plot the stacked bar chart for Yes, No and Maybe
        df_occupation.plot(x='Days_Indoors', kind='bar', stacked=True, width = 0.5, ax = ax, color=['#ffe196', '#ff9696', '#96ffa1'], zorder = 3)

        # Add text elements: Bar names, Axis names, title, legend
        ax.set_xticks(x)
        ax.set_xticklabels(df_occupation['Days_Indoors'])
        ax.set_xlabel('Days Indoors')
        ax.set_ylabel('Proportion')
        ax.set_title(f'Proportion of Mental Health History by Days Indoors - {val}')
        ax.legend(title='Mental Health History')
        ax.grid(alpha=0.6, zorder = 0)

        # Show plot
        plt.xticks(horizontalalignment ='center', rotation = 0)
        plt.tight_layout()

    plt.show()

#mentalHealthHistory_grouped(df)
