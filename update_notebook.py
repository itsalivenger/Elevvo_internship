import nbformat
import sys

notebook_path = r"c:\Users\aliho\Desktop\projects\datascience\internship_ELEVOO\drive-download-20260204T180558Z-3-001\Elevvo Internship Tasks\Walmart Sales Forecast\main.ipynb"

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Markdown cells to insert
    md1 = nbformat.v4.new_markdown_cell(
        "## Data Acquisition & Merging\n"
        "**What:** Loading the raw CSV files for features, train data, test data, and store information, then merging them into comprehensive training and testing dataframes.\n\n"
        "**Why:** Neural Networks require a unified dataset. By joining these tables on shared keys like `Store` and `Date`, we ensure all relevant predictors (like Markdown events and store sizes) correspond to the correct weekly sales targets."
    )

    md2 = nbformat.v4.new_markdown_cell(
        "## Feature Engineering & Categorical Encoding\n"
        "**What:** \n"
        "- Converting the `Date` string column to datetime objects and extracting the month, day, and day of the week.\n"
        "- Using `OneHotEncoder` to transform the categorical variables (`IsHoliday`, `Type`, `Dept`) into machine-readable numeric arrays.\n\n"
        "**Why:** \n"
        "- Neural Networks cannot process raw date strings; extracting datetime components allows the model to capture seasonality (e.g., holiday spikes).\n"
        "- Categorical encoding is necessary because algorithms require numerical input. One-hot encoding prevents the model from assuming a false ordinal relationship between nominal categories like Store Departments."
    )

    md3 = nbformat.v4.new_markdown_cell(
        "## Data Cleaning\n"
        "**What:** Concatenating our newly encoded columns with the rest of the dataset, dropping overlapping or redundant columns, and filling `NaN` values in the `MarkDown` columns with `0`.\n\n"
        "**Why:** \n"
        "- We filled Markdowns with 0 because a `NaN` here does not mean 'missing data'; it represents the absence of a promotional event. \n"
        "- Redundant columns (like `Date` after component extraction) are dropped to reduce dimensionality and prevent perfect collinearity."
    )

    md4 = nbformat.v4.new_markdown_cell(
        "## Feature Scaling\n"
        "**What:** Identifying continuous numerical columns (those with more than 10 unique values) and applying `StandardScaler` to standardize them to a mean of 0 and standard deviation of 1. We also split the data into train and validation slices.\n\n"
        "**Why:** We are scaling these features because raw large integers (like massive `Weekly_Sales` or `MarkDown` values) can overwhelm Neural Network weights, slowing down gradient descent or causing explosive gradients. Standardization ensures all features contribute equally to the learning process."
    )

    md5 = nbformat.v4.new_markdown_cell(
        "## Model Architecture\n"
        "**What:** Building a deep Neural Network using the Keras Functional API. The model consists of an input layer, four hidden `Dense` layers using the `relu` activation function (128, 64, 32, and 16 neurons), and a final linear output layer for regression.\n\n"
        "**Why:** \n"
        "- The `relu` (Rectified Linear Unit) activation function helps the network learn complex, non-linear relationships without suffering from the vanishing gradient problem.\n"
        "- A `linear` activation in the final node is standard for regression tasks, as it allows the model to predict unbounded continuous numerical values (like Sales)."
    )

    md6 = nbformat.v4.new_markdown_cell(
        "## Evaluation\n"
        "**What:** Generating predictions on the test slice, calculating the $R^2$ (R-squared) score, and visualizing the actual vs. predicted values using a scatter plot over a diagonal identity line.\n\n"
        "**Why:** The $R^2$ score tells us the proportion of the variance in the dependent variable (Sales) that is predictable from the independent variables. The scatter plot allows for a visual sanity check: points closer to the red diagonal line indicate more accurate predictions by the Neural Network."
    )

    # Insert cells in reverse order to not mess up indices
    # Find indices based on cell content
    idx_eval = -1
    idx_model = -1
    idx_scale = -1
    idx_clean = -1
    idx_feat = -1
    idx_data = -1

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = cell.source
            if "r2_score(scaled_Y_test_slice, Y_pred)" in source:
                idx_eval = i
            elif "input = tf.keras.layers.Input(" in source:
                idx_model = i
            elif "scaler = StandardScaler()" in source and "to_scale_cols = []" in source:
                idx_scale = i
            elif "X_train = pd.concat(" in source:
                idx_clean = i
            elif "# date formatting" in source:
                idx_feat = i
            elif "features_df = pd.read_csv" in source:
                idx_data = i

    if all(idx != -1 for idx in [idx_eval, idx_model, idx_scale, idx_clean, idx_feat, idx_data]):
        nb.cells.insert(idx_eval, md6)
        nb.cells.insert(idx_model, md5)
        nb.cells.insert(idx_scale, md4)
        nb.cells.insert(idx_clean, md3)
        nb.cells.insert(idx_feat, md2)
        nb.cells.insert(idx_data, md1)

        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("Successfully updated the notebook.")
    else:
        print(f"Failed to find all injection points: {[idx_eval, idx_model, idx_scale, idx_clean, idx_feat, idx_data]}")

except Exception as e:
    print(f"Error: {e}")
