import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = 0
for index, row in df.iterrows():
    if((row['weight']/(row['height']*0.01)**2)>25):
        df.at[index,'overweight'] = 1
    else:
        df.at[index,'overweight'] = 0
# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
for index, row in df.iterrows():
    if(row['cholesterol'] > 1):
        df.at[index,'cholesterol'] = 1
    else:
        df.at[index,'cholesterol'] = 0
    if(row['gluc'] > 1):
        df.at[index,'gluc'] = 1
    else:
        df.at[index,'gluc'] = 0

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,id_vars=['cardio'],value_vars=['cholesterol','gluc','smoke','alco','active','overweight'])
    df_cat['total'] = 1


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat =  df_cat.groupby(['cardio','variable','value'],as_index=False).count()

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x='variable',y='total',kind='bar',data=df_cat,hue='value',col='cardio').fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[
        (df['ap_lo']<= df['ap_hi']) & 
        (df['height']>=df['height'].quantile(0.025)) & 
        (df['height']<=df['height'].quantile(0.975)) & 
        (df['weight']>=df['weight'].quantile(0.025)) & 
        (df['weight']<=df['weight'].quantile(0.975))]
    # Calculate the correlation matrix
    corr = df_heat.corr(method="pearson")

    # Generate a mask for the upper triangle
    mask = np.triu(corr)



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12,12))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr,linewidths=1,annot=True,mask=mask,square=True,fmt=".1f",center=0.08,cbar_kws={"shrink":0.5})


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
