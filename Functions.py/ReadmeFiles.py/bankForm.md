A/B Testing (AM Testing)
What is A/B Testing?
A/B testing is a statistical method used to compare two versions of a product, webpage, or process to determine which one performs better.

Steps in A/B Testing
Define the Hypothesis → Decide what you want to test (e.g., "Does a new loan application form increase approvals?").
Split the Sample → Randomly divide users into two groups:
Group A (Control) → Uses the old version.
Group B (Variant) → Uses the new version.
Collect Data → Measure key metrics (e.g., approval rates, conversion rates).
Analyze Results → Use statistical methods (like the Chi-Square Test) to determine if the difference is real or random.
Make a Decision → If the new version performs significantly better, implement it!
Example: Bank Loan Approvals
A bank wants to see if a new loan form improves approval rates:

Form A (Old) → 200 approvals, 300 rejections.
Form B (New) → 260 approvals, 240 rejections.
A Chi-Square Test is used to check if the difference is statistically significant.
📌 Chi-Square Testing
What is a Chi-Square Test?
A Chi-Square Test is a statistical test used to determine whether there is a significant association between two categorical variables.
 Where:

O = Observed values (actual data).
E = Expected values (if there was no real difference).
Types of Chi-Square Tests
Chi-Square Goodness of Fit → Tests if a sample follows an expected distribution.
Chi-Square Test for Independence → Tests if two categorical variables are related (used in A/B testing).
Example: Loan Approval Study
Form Type	Approved ✅	Rejected ❌	Total
Old Form (A)	200	300	500
New Form (B)	260	240	500
Hypothesis:

Null Hypothesis (H₀): The loan form does not affect approval rates.
Alternative Hypothesis (H₁): The new loan form does affect approval rates.
📊 If p-value < 0.05 → Reject H₀ → The new form actually improves approvals!

🔑 Key Differences Between A/B Testing & Chi-Square Testing
Concept	A/B Testing	Chi-Square Testing
Purpose	Compares two versions of something (e.g., old vs. new loan form).	Checks if two categorical variables are related.
Data Type	Works with categorical or numerical data.	Works with categorical data only.
Example Use	Testing website button colors, ad campaigns, loan approval forms.	Checking if approval rate depends on loan form type.
Key Output	Conversion rate, success rate, statistical significance.	Chi-Square value, p-value.
🎯 Final Takeaway
A/B Testing helps compare two versions of a system.
Chi-Square Testing determines if the observed differences are real or random.
A/B Testing often uses Chi-Square Tests when comparing categorical data like approvals vs. rejections.