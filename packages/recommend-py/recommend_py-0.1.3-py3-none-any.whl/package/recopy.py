# This is an example Python library functionality

import pandas as pd  # Import pandas
import numpy as np  # Import numpy
from sklearn.metrics.pairwise import cosine_similarity


def is_utility(df):
    """
    Check if the input matrix is utility.
    :param matrix: The input matrix (list of lists).
    :return: If every column (except the first one, usually its column name or id) is numeric, return True; otherwise return False.
    """

    for col in df.columns[1:]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            return False

    return True

def to_utility(df, id_col_num):
    """
    Convert the input DataFrame to a utility format.
    :param df: The input DataFrame.
    :param id_col_num: The column number (0-indexed) to be used as the ID column.
    :return: A DataFrame with the ID column as the first column and only numeric columns retained.
    """
    # Extract the ID column
    id_column = df.iloc[:, id_col_num]

    # Create a new DataFrame with the ID column
    utility_df = pd.DataFrame(id_column)

    # Iterate through the DataFrame columns and retain only numeric columns
    for col in df.columns:
        if col != df.columns[id_col_num]:  # Skip the ID column
            if pd.api.types.is_numeric_dtype(df[col]):
                utility_df[col] = df[col]  # Add numeric columns to the new DataFrame

    return utility_df

def utility_normalize(df):
    """
    Normalize the utility matrix.
    :param df: The input DataFrame.
    :return: A DataFrame with normalized values, keeping NaN values unchanged.
    """
    # Create a new DataFrame to store normalized values
    normalized_df = df.copy()

    # Normalize each column
    for col in df.columns[1:]:  # Skip the first column (assumed to be the ID column)
        # Calculate mean and standard deviation
        mean = df[col].mean()
        std = df[col].std()

        # Normalize, keeping NaN values
        normalized_df[col] = (df[col] - mean) / std

    return normalized_df

def utility_standardize(df):
    """
    Standardize the utility matrix.
    :param df: The input DataFrame.
    :return: A DataFrame with standardized values, keeping NaN values unchanged.
    """
    # Create a new DataFrame to store standardized values
    standardized_df = df.copy()

    # Standardize each column
    for col in df.columns[1:]:  # Skip the first column (assumed to be the ID column)
        # Calculate mean and standard deviation
        mean = df[col].mean()
        std = df[col].std()

        # Standardize, keeping NaN values
        standardized_df[col] = (df[col] - mean) / std

    return standardized_df

def similarity_calculation(df, mean_same_item):
    """
    Calculate the similarity matrix based on user ratings.
    :param df: The input DataFrame in utility format.
    :param mean_same_item: A positive integer that should be less than the number of columns in the input matrix minus 2.
    :return: A similarity matrix with shape (number of users, number of users).
    """
    # Check if the input DataFrame is in utility format
    if not is_utility(df):
        raise ValueError("Input DataFrame is not in utility format.")

    # Check if mean_same_item is a positive integer and less than the number of columns - 2
    if not isinstance(mean_same_item, int) or mean_same_item <= 0 or mean_same_item >= df.shape[1] - 1:
        raise ValueError("mean_same_item must be a positive integer less than the number of columns in the input matrix minus 2.")

    # Calculate user ratings matrix
    user_ratings = df.iloc[:, 1:]  # Skip the ID column
    user_similarity = np.full((user_ratings.shape[0], user_ratings.shape[0]), np.nan)  # Initialize similarity matrix as NaN

    # Calculate similarity between each pair of users
    for i in range(user_ratings.shape[0]):
        for j in range(i + 1, user_ratings.shape[0]):
            # Get ratings for two users
            user_i_ratings = user_ratings.iloc[i]
            user_j_ratings = user_ratings.iloc[j]

            # Calculate common rated items
            common_ratings = user_i_ratings.notna() & user_j_ratings.notna()
            if common_ratings.sum() >= mean_same_item:  # Check the number of common rated items
                # Calculate cosine similarity
                similarity = cosine_similarity([user_i_ratings.fillna(0)], [user_j_ratings.fillna(0)])[0][0]
                user_similarity[i, j] = similarity
                user_similarity[j, i] = similarity  # Symmetry

    # Create a new DataFrame to store the similarity matrix and add the first column and row
    similarity_df = pd.DataFrame(user_similarity, index=df.iloc[:, 0], columns=df.iloc[:, 0])  # Use ID column as index and column names
    similarity_df = similarity_df.rename_axis('User ID', axis=0).rename_axis('User ID', axis=1)  # Add axis labels

    return similarity_df

def recommend_calculation(df, top_n, mean_score):
    """
    Calculate recommendations for users based on similarity scores.
    :param df: The input DataFrame in utility format.
    :param top_n: The number of top items to recommend for each user.
    :param mean_score: The minimum score a similar user must give for an item to be recommended.
    :return: A DataFrame containing user IDs and their recommended items.
    """
    # Calculate similarity matrix
    user_similarity = similarity_calculation(df, 2)  # Use 2 as an example value for mean_same_item
    recommendations = {}

    for user_id in df.iloc[:, 0]:  # Iterate over each user
        user_index = df[df.iloc[:, 0] == user_id].index[0]  # Get the user's index
        similar_users = user_similarity.loc[user_id].dropna().sort_values(ascending=False)  # Get similar users and their similarity scores

        # Create a dictionary to store recommendation scores
        item_scores = {}

        for similar_user_id, similarity in similar_users.items():
            if similarity > 0:  # Only consider users with similarity greater than 0
                similar_user_index = df[df.iloc[:, 0] == similar_user_id].index[0]
                similar_user_ratings = df.iloc[similar_user_index, 1:]  # Get ratings of the similar user

                for item_index, rating in enumerate(similar_user_ratings):
                    if pd.isna(df.iloc[user_index, item_index + 1]) and rating >= mean_score:  # Check if the target user has not rated and the similar user's rating is above mean_score
                        item_name = df.columns[item_index + 1]  # Get item name
                        if item_name not in item_scores:
                            item_scores[item_name] = 0
                        item_scores[item_name] += similarity * rating  # Weighted score based on similarity

        # Sort by recommendation scores and select the top_n items
        recommended_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        recommendations[user_id] = [item[0] for item in recommended_items]  # Keep only item names

    # Create a DataFrame to store recommendation results
    recommendations_df = pd.DataFrame(list(recommendations.items()), columns=['User ID', 'Recommended Items'])
    return recommendations_df

def main():
    # Create a 5x6 matrix
    user_ids = [1, 2, 3, 4, 5]  # User IDs
    product_names = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']  # Product names
    ratings = [
        [4, 5, 3, 2, 1],  # User 1 ratings
        [3, 4, 2, 5, 1],  # User 2 ratings
        [5, 3, 4, 1, 2],  # User 3 ratings
        [2, 1, 5, 4, 3],  # User 4 ratings
        [1, 2, 4, 3, 5]   # User 5 ratings
    ]

    # Convert ratings to a DataFrame
    df = pd.DataFrame(ratings, columns=product_names)
    df.insert(0, 'User ID', user_ids)  # Insert User ID column

    # Set 1/3 of the data to NaN
    total_values = df.size - df.shape[0]  # Exclude User ID column
    num_nan = total_values // 3  # Calculate number of NaN values
    nan_indices = np.random.choice(df.index.size * (df.shape[1] - 1), num_nan, replace=False)  # Randomly select indices for NaN

    for index in nan_indices:
        row = index // (df.shape[1] - 1)
        col = index % (df.shape[1] - 1) + 1  # Offset by 1 for User ID column
        df.iat[row, col] = np.nan  # Set the selected position to NaN

    print(df)  # Print DataFrame

    df = to_utility(df, 0)
    df = utility_normalize(df)
    print(is_utility(df))
    similarity = similarity_calculation(df, 2)
    print(similarity)
    result = recommend_calculation(df, 1, 0)
    print(result)
    
if __name__ == '__main__':
    main() 