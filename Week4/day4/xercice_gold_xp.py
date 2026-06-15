#  STUDENT PERFORMANCE ANALYSIS 
# Hypothesis Testing: Gender Differences & Multiple Group Comparisons

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, f_oneway, levene, shapiro
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings
warnings.filterwarnings('ignore')

#  1. DATA LOADING & WRANGLING 
print("="*60)
print("STEP 1: DATA LOADING & WRANGLING")
print("="*60)

# Load the dataset
url = "https://raw.githubusercontent.com/tisage/students-performance/master/StudentsPerformance.csv"
df = pd.read_csv(url)

print(f"Dataset shape: {df.shape}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nDataset info:")
print(df.info())
print(f"\nMissing values:")
print(df.isnull().sum())
print(f"\nBasic statistics:")
print(df.describe())

# Check column names (they might have spaces)
print(f"\nColumn names: {df.columns.tolist()}")

# Rename columns for easier access (remove spaces)
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.replace('/', '_per_')
print(f"\nRenamed columns: {df.columns.tolist()}")

#  2. DATA VISUALIZATION 
print("\n" + "="*60)
print("STEP 2: DATA VISUALIZATION")
print("="*60)

# Create figure for multiple plots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Distribution of scores
axes[0, 0].hist(df['math_score'], bins=20, alpha=0.7, color='blue', edgecolor='black')
axes[0, 0].set_title('Math Score Distribution')
axes[0, 0].set_xlabel('Score')
axes[0, 0].set_ylabel('Frequency')

axes[0, 1].hist(df['reading_score'], bins=20, alpha=0.7, color='green', edgecolor='black')
axes[0, 1].set_title('Reading Score Distribution')
axes[0, 1].set_xlabel('Score')
axes[0, 1].set_ylabel('Frequency')

axes[0, 2].hist(df['writing_score'], bins=20, alpha=0.7, color='red', edgecolor='black')
axes[0, 2].set_title('Writing Score Distribution')
axes[0, 2].set_xlabel('Score')
axes[0, 2].set_ylabel('Frequency')

# Box plots by gender
sns.boxplot(data=df, x='gender', y='math_score', ax=axes[1, 0])
axes[1, 0].set_title('Math Scores by Gender')

sns.boxplot(data=df, x='gender', y='reading_score', ax=axes[1, 1])
axes[1, 1].set_title('Reading Scores by Gender')

sns.boxplot(data=df, x='gender', y='writing_score', ax=axes[1, 2])
axes[1, 2].set_title('Writing Scores by Gender')

plt.tight_layout()
plt.show()

# Additional visualizations
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Scores by test preparation course
prep_data = df.groupby('test_preparation_course')[['math_score', 'reading_score', 'writing_score']].mean()
prep_data.plot(kind='bar', ax=axes[0])
axes[0].set_title('Average Scores by Test Preparation')
axes[0].set_ylabel('Average Score')
axes[0].legend(loc='upper right')

# Scores by lunch type
lunch_data = df.groupby('lunch')[['math_score', 'reading_score', 'writing_score']].mean()
lunch_data.plot(kind='bar', ax=axes[1])
axes[1].set_title('Average Scores by Lunch Type')
axes[1].set_ylabel('Average Score')
axes[1].legend(loc='upper right')

plt.tight_layout()
plt.show()

#  3. T-TEST: GENDER DIFFERENCES IN MATH SCORES 
print("\n" + "="*60)
print("STEP 3: INDEPENDENT TWO-SAMPLE T-TEST")
print("Gender Differences in Math Scores")
print("="*60)

# Separate data by gender
male_math = df[df['gender'] == 'male']['math_score']
female_math = df[df['gender'] == 'female']['math_score']

print(f"Male students count: {len(male_math)}")
print(f"Female students count: {len(female_math)}")
print(f"Male math score mean: {male_math.mean():.2f} (±{male_math.std():.2f})")
print(f"Female math score mean: {female_math.mean():.2f} (±{female_math.std():.2f})")
print(f"Mean difference: {male_math.mean() - female_math.mean():.2f}")

# Check normality assumption (for large samples, Central Limit Theorem applies)
# But let's check anyway
shapiro_male = shapiro(male_math.sample(min(5000, len(male_math))))
shapiro_female = shapiro(female_math.sample(min(5000, len(female_math))))

print(f"\nNormality test (Shapiro-Wilk):")
print(f"Male math scores p-value: {shapiro_male.pvalue:.4f}")
print(f"Female math scores p-value: {shapiro_female.pvalue:.4f}")

# Check homogeneity of variance (Levene's test)
levene_stat, levene_p = levene(male_math, female_math)
print(f"\nLevene's test for equal variances:")
print(f"Statistic: {levene_stat:.4f}, p-value: {levene_p:.4f}")

# Perform t-test (Welch's t-test if variances are unequal)
if levene_p < 0.05:
    print("\nVariances are significantly different → Using Welch's t-test")
    t_stat, p_value = ttest_ind(male_math, female_math, equal_var=False)
else:
    print("\nVariances are equal → Using standard t-test")
    t_stat, p_value = ttest_ind(male_math, female_math, equal_var=True)

print(f"\nT-test results:")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.6f}")

alpha = 0.05
if p_value < alpha:
    print(f"\n✓ Reject null hypothesis: Significant difference between male and female math scores (p < {alpha})")
else:
    print(f"\n✗ Fail to reject null hypothesis: No significant difference (p > {alpha})")

#  4. T-TEST: GENDER DIFFERENCES IN READING SCORES 
print("\n" + "="*60)
print("STEP 4: T-TEST - Gender Differences in Reading Scores")
print("="*60)

male_reading = df[df['gender'] == 'male']['reading_score']
female_reading = df[df['gender'] == 'female']['reading_score']

print(f"Male reading mean: {male_reading.mean():.2f}")
print(f"Female reading mean: {female_reading.mean():.2f}")
print(f"Mean difference: {female_reading.mean() - male_reading.mean():.2f}")

# Levene's test
levene_stat_read, levene_p_read = levene(male_reading, female_reading)
print(f"Levene's test p-value: {levene_p_read:.4f}")

# T-test
t_stat_read, p_value_read = ttest_ind(male_reading, female_reading, equal_var=(levene_p_read >= 0.05))
print(f"\nT-test results - Reading:")
print(f"t-statistic: {t_stat_read:.4f}")
print(f"p-value: {p_value_read:.6f}")

if p_value_read < alpha:
    print(f"\n✓ Significant difference: Females score higher in reading (p < {alpha})")
else:
    print(f"\n✗ No significant difference in reading scores (p > {alpha})")

#  5. T-TEST: GENDER DIFFERENCES IN WRITING SCORES 
print("\n" + "="*60)
print("STEP 5: T-TEST - Gender Differences in Writing Scores")
print("="*60)

male_writing = df[df['gender'] == 'male']['writing_score']
female_writing = df[df['gender'] == 'female']['writing_score']

print(f"Male writing mean: {male_writing.mean():.2f}")
print(f"Female writing mean: {female_writing.mean():.2f}")
print(f"Mean difference: {female_writing.mean() - male_writing.mean():.2f}")

# T-test
t_stat_write, p_value_write = ttest_ind(male_writing, female_writing, equal_var=False)
print(f"\nT-test results - Writing:")
print(f"t-statistic: {t_stat_write:.4f}")
print(f"p-value: {p_value_write:.6f}")

if p_value_write < alpha:
    print(f"\n✓ Significant difference: Females score higher in writing (p < {alpha})")
else:
    print(f"\n✗ No significant difference in writing scores (p > {alpha})")

#  6. ONE-WAY ANOVA: TEST PREPARATION COURSE IMPACT 
print("\n" + "="*60)
print("STEP 6: ONE-WAY ANOVA - Test Preparation Course Impact on Math Scores")
print("="*60)

# Group data by test preparation course
prep_groups = [group['math_score'].values for name, group in df.groupby('test_preparation_course')]
prep_labels = df['test_preparation_course'].unique()

print("Groups:")
for i, label in enumerate(prep_labels):
    print(f"  {label}: n={len(prep_groups[i])}, mean={np.mean(prep_groups[i]):.2f}")

# Check homogeneity of variance
levene_stat_prep, levene_p_prep = levene(*prep_groups)
print(f"\nLevene's test p-value: {levene_p_prep:.4f}")

# Perform One-Way ANOVA
f_stat, p_value_anova = f_oneway(*prep_groups)
print(f"\nANOVA results:")
print(f"F-statistic: {f_stat:.4f}")
print(f"p-value: {p_value_anova:.6f}")

if p_value_anova < alpha:
    print(f"\n✓ Significant differences exist among test preparation groups (p < {alpha})")
    
    # Post-hoc test (Tukey HSD)
    print("\nPerforming Tukey HSD post-hoc test:")
    tukey_result = pairwise_tukeyhsd(df['math_score'], df['test_preparation_course'], alpha=0.05)
    print(tukey_result)
else:
    print(f"\n✗ No significant differences among groups (p > {alpha})")

#  7. ONE-WAY ANOVA: LUNCH TYPE IMPACT 
print("\n" + "="*60)
print("STEP 7: ONE-WAY ANOVA - Lunch Type Impact on Math Scores")
print("="*60)

lunch_groups = [group['math_score'].values for name, group in df.groupby('lunch')]
lunch_labels = df['lunch'].unique()

print("Groups:")
for i, label in enumerate(lunch_labels):
    print(f"  {label}: n={len(lunch_groups[i])}, mean={np.mean(lunch_groups[i]):.2f}")

# One-Way ANOVA
f_stat_lunch, p_value_lunch = f_oneway(*lunch_groups)
print(f"\nANOVA results:")
print(f"F-statistic: {f_stat_lunch:.4f}")
print(f"p-value: {p_value_lunch:.6f}")

if p_value_lunch < alpha:
    print(f"\n✓ Significant differences exist among lunch groups (p < {alpha})")
    
    # Post-hoc test
    print("\nPerforming Tukey HSD post-hoc test:")
    tukey_lunch = pairwise_tukeyhsd(df['math_score'], df['lunch'], alpha=0.05)
    print(tukey_lunch)
else:
    print(f"\n✗ No significant differences among lunch groups (p > {alpha})")

#  8. COMPREHENSIVE ANALYSIS - ALL SUBJECTS 
print("\n" + "="*60)
print("STEP 8: COMPREHENSIVE ANALYSIS - All Subjects by Gender")
print("="*60)

subjects = ['math_score', 'reading_score', 'writing_score']
results = []

for subject in subjects:
    male_scores = df[df['gender'] == 'male'][subject]
    female_scores = df[df['gender'] == 'female'][subject]
    
    t_stat, p_val = ttest_ind(male_scores, female_scores, equal_var=False)
    effect_size = (female_scores.mean() - male_scores.mean()) / male_scores.std()
    
    results.append({
        'Subject': subject.replace('_score', '').capitalize(),
        'Male_Mean': male_scores.mean(),
        'Female_Mean': female_scores.mean(),
        'Difference': female_scores.mean() - male_scores.mean(),
        't_statistic': t_stat,
        'p_value': p_val,
        'Significant': p_val < alpha,
        'Effect_Size': effect_size
    })

results_df = pd.DataFrame(results)
print("\nComprehensive Results:")
print(results_df.to_string(index=False))

#  9. EFFECT OF TEST PREPARATION ON ALL SUBJECTS 
print("\n" + "="*60)
print("STEP 9: Test Preparation Impact on All Subjects")
print("="*60)

prep_impact = df.groupby('test_preparation_course')[['math_score', 'reading_score', 'writing_score']].mean()
print("\nAverage scores by test preparation:")
print(prep_impact)

prep_diff = prep_impact.loc['completed'] - prep_impact.loc['none']
print(f"\nImprovement from test preparation:")
print(f"Math: +{prep_diff['math_score']:.2f} points")
print(f"Reading: +{prep_diff['reading_score']:.2f} points")
print(f"Writing: +{prep_diff['writing_score']:.2f} points")

#  10. VISUALIZATION OF RESULTS 
print("\n" + "="*60)
print("STEP 10: FINAL VISUALIZATIONS")
print("="*60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Gender comparison bar plot
subjects_plot = ['Math', 'Reading', 'Writing']
male_means = [male_math.mean(), male_reading.mean(), male_writing.mean()]
female_means = [female_math.mean(), female_reading.mean(), female_writing.mean()]

x = np.arange(len(subjects_plot))
width = 0.35
axes[0, 0].bar(x - width/2, male_means, width, label='Male', alpha=0.8)
axes[0, 0].bar(x + width/2, female_means, width, label='Female', alpha=0.8)
axes[0, 0].set_xlabel('Subject')
axes[0, 0].set_ylabel('Average Score')
axes[0, 0].set_title('Average Scores by Gender')
axes[0, 0].set_xticks(x)
axes[0, 0].set_xticklabels(subjects_plot)
axes[0, 0].legend()
axes[0, 0].set_ylim(60, 80)

# Effect size visualization
effect_sizes = results_df['Effect_Size'].values
colors_bar = ['red' if es < 0 else 'green' for es in effect_sizes]
axes[0, 1].bar(subjects_plot, effect_sizes, color=colors_bar, alpha=0.7)
axes[0, 1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
axes[0, 1].set_xlabel('Subject')
axes[0, 1].set_ylabel("Cohen's d (Effect Size)")
axes[0, 1].set_title("Effect Size: Female vs Male (Positive = Female Higher)")
axes[0, 1].axhline(y=0.2, color='gray', linestyle='--', alpha=0.5, label='Small effect')
axes[0, 1].axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Medium effect')
axes[0, 1].axhline(y=0.8, color='gray', linestyle='--', alpha=0.5, label='Large effect')
axes[0, 1].legend()

# Heatmap of correlations
corr_matrix = df[['math_score', 'reading_score', 'writing_score']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[1, 0])
axes[1, 0].set_title('Correlation Between Subjects')

# Parental education level impact
parent_edu_scores = df.groupby('parental_level_of_education')[['math_score', 'reading_score', 'writing_score']].mean()
parent_edu_scores.plot(kind='bar', ax=axes[1, 1])
axes[1, 1].set_title('Scores by Parental Education Level')
axes[1, 1].set_xlabel('Parental Education Level')
axes[1, 1].set_ylabel('Average Score')
axes[1, 1].legend(loc='lower right')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

#  11. SUMMARY REPORT 
print("\n" + "="*60)
print("FINAL SUMMARY REPORT")
print("="*60)

summary = f"""
 STUDENT PERFORMANCE ANALYSIS REPORT 

1. DATA OVERVIEW:
   - Total students: {len(df)}
   - Male: {len(male_math)} ({len(male_math)/len(df)*100:.1f}%)
   - Female: {len(female_math)} ({len(female_math)/len(df)*100:.1f}%)

2. GENDER DIFFERENCES (T-TEST RESULTS):
   - Math: {'SIGNIFICANT' if p_value < alpha else 'NOT SIGNIFICANT'} (p={p_value:.4f})
     Male: {male_math.mean():.2f} | Female: {female_math.mean():.2f}
   - Reading: {'SIGNIFICANT' if p_value_read < alpha else 'NOT SIGNIFICANT'} (p={p_value_read:.4f})
     Male: {male_reading.mean():.2f} | Female: {female_reading.mean():.2f}
   - Writing: {'SIGNIFICANT' if p_value_write < alpha else 'NOT SIGNIFICANT'} (p={p_value_write:.4f})
     Male: {male_writing.mean():.2f} | Female: {female_writing.mean():.2f}

3. KEY FINDINGS:
   - Females perform significantly better in Reading and Writing
   - Males perform slightly better in Math (but difference may not be significant)
   - Test preparation course improves scores across all subjects
   - Students with standard lunch outperform those with free/reduced lunch

4. RECOMMENDATIONS:
   - Implement targeted support for male students in Reading/Writing
   - Encourage test preparation course enrollment for all students
   - Investigate and address factors related to lunch status disparities
"""

print(summary)

print("\n" + "="*60)
print("XP NINJA - EXERCISE COMPLETE!")
print("="*60)