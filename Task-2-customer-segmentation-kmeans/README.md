# Customer Segmentation using K-Means Clustering

## Project Overview

This project performs customer segmentation using unsupervised machine learning techniques.  
The goal is to group customers based on their spending behavior and annual income to help businesses create targeted marketing strategies.

The project uses the Mall Customers dataset and applies K-Means clustering along with PCA visualization.

---

## Dataset

Dataset Used: Mall Customers Dataset

Main Features:
- CustomerID
- Gender
- Age
- Annual Income (k$)
- Spending Score (1-100)

---

## Objectives

- Perform Exploratory Data Analysis (EDA)
- Identify customer patterns and behavior
- Apply K-Means clustering
- Determine optimal number of clusters using Elbow Method
- Visualize clusters using PCA
- Suggest business marketing strategies for each segment

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

---

## Machine Learning Techniques

### K-Means Clustering
Used to segment customers into different groups based on:
- Annual Income
- Spending Score

### PCA (Principal Component Analysis)
Used to visualize customer clusters in reduced dimensions.

---

## Key Insights

- Customers can be grouped into multiple spending behavior categories.
- High-income customers do not always spend more.
- Some customers have high spending behavior despite moderate income.
- Different customer groups require different marketing strategies.

---

## Suggested Marketing Strategies

### High Income - High Spending
- Premium memberships
- VIP offers
- Exclusive launches

### High Income - Low Spending
- Personalized campaigns
- Re-engagement offers

### Low Income - High Spending
- Discounts and bundles
- Seasonal promotions

### Low Income - Low Spending
- Budget-friendly products
- Awareness campaigns

### Average Customers
- General loyalty programs
- Cross-selling offers

---

## Project Structure

```text
customer-segmentation-kmeans/
│
├── data/
│   └── Mall_Customers.csv
│
├── images/
│
├── notebook/
│   └── customer-segmentation.ipynb
│
├── README.md
├── requirements.txt
```

---

## Results

The project successfully segmented customers into meaningful groups using K-Means clustering.  
The generated visualizations and PCA plots clearly show customer separation and behavior patterns.

---

## Author

Muneeb Ur Rehman