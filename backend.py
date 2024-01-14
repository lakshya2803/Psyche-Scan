import pandas as pd
import re

def data_cleaning():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('Mental-Health-Twitter.csv')

    # Columns to drop
    to_drop = ['index', 'post_id', 'followers', 'friends', 'favourites', 'statuses', 'retweets', 'label']
    # Remove leading and trailing spaces from column names
    to_drop = [column.strip() for column in to_drop]
    # Check if the columns exist in the DataFrame before dropping them
    for column in to_drop:
        if column in df.columns:
            df.drop(column, axis=1, inplace=True)
        else:
            print(f"Column '{column}' does not exist in the DataFrame.")

    # Apply the clean_text function to the 'post_text' column
    df['post_text'] = df['post_text'].apply(clean_text)
    # Save the cleaned DataFrame to a new CSV file
    df.to_csv('cleanedData1.csv', index=False)
    print("URLs, words starting with '@', and specified characters have been removed. The cleaned data has been saved to 'cleanedData1.csv'.")

# Function to remove URLs, words starting with '@', and specified characters from text
def clean_text(text):
    # Use regular expressions to match and remove URLs, words starting with '@', 
    # and specified characters jese ke :-- 
    cleaned_text = re.sub(r'http[s]?://\S+|\@\w+|:|"|\'|―|#', '', text)
    return cleaned_text

data_cleaning()