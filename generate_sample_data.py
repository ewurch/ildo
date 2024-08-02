import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples
n_samples = 1000

# Generate data
data = {
    'age': np.random.randint(18, 80, n_samples),
    'gender': np.random.choice(['Male', 'Female'], n_samples),
    'bmi': np.random.normal(25, 5, n_samples).round(1),
    'num_children': np.random.randint(0, 5, n_samples),
    'smoker': np.random.choice(['Yes', 'No'], n_samples),
    'region': np.random.choice(['Northeast', 'Northwest', 'Southeast', 'Southwest'], n_samples),
    'coverage_level': np.random.choice(['Basic', 'Standard', 'Premium'], n_samples),
    'credit_score': np.random.randint(300, 850, n_samples),
    'annual_mileage': np.random.randint(1000, 50000, n_samples)
}

# Create DataFrame
df = pd.DataFrame(data)

# Generate target variable (insurance price)
# This is a simplified model and doesn't reflect real-world pricing accurately
base_price = 500
df['insurance_price'] = base_price + \
                        df['age'] * 7 + \
                        (df['gender'] == 'Male') * 100 + \
                        df['bmi'] * 20 + \
                        df['num_children'] * 200 + \
                        (df['smoker'] == 'Yes') * 500 + \
                        (df['region'] == 'Northeast') * 200 + \
                        (df['region'] == 'Northwest') * 100 + \
                        (df['region'] == 'Southeast') * 150 + \
                        (df['coverage_level'] == 'Standard') * 300 + \
                        (df['coverage_level'] == 'Premium') * 800 + \
                        (850 - df['credit_score']) * 1.5 + \
                        df['annual_mileage'] * 0.02

# Add some random noise
df['insurance_price'] += np.random.normal(0, 500, n_samples)

# Ensure all prices are positive and round to 2 decimal places
df['insurance_price'] = np.maximum(0, df['insurance_price']).round(2)

# Save to CSV
df.to_csv('insurance_sample_data.csv', index=False)

print("Sample data saved to 'insurance_sample_data.csv'")