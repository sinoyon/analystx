import pandas as pd
from analystx import analyze

# Sample user subscription data
data = {
    'user_id': [1, 2, 3, 4, 5],
    'first_name': ['John', 'Jane', 'Ali', 'Maria', 'David'],
    'last_name': ['Doe', 'Smith', 'Khan', 'Gonzalez', 'Lee'],
    'email': ['john.doe@example.com', 'jane.smith@example.com', 'ali.khan@example.com', 'maria.gonzalez@example.com', 'david.lee@example.com'],
    'signup_date': ['15/1/2023', '20/2/2023', '5/3/2023', '28/1/2023', '10/2/2023'],
    'subscription_status': ['active', 'inactive', 'active', 'active', 'canceled']
}

df = pd.DataFrame(data)

print("=" * 80)
print("TESTING ENHANCED ANALYSIS WITH USER SUBSCRIPTION DATA")
print("=" * 80)
print("\nInput Data:")
print(df)
print("\n" + "=" * 80)

# Run analysis
results = analyze(df, business_context="User Subscription Analysis")

print("\n✅ Analysis Complete!")
print(f"\nAnalysis Context: {results.business_context}")
print(f"\nData Quality Summary:")
print(f"  - Total Records: {results.insights['data_quality']['total_records']}")
print(f"  - Total Fields: {results.insights['data_quality']['total_fields']}")
print(f"  - Data Completeness: {results.insights['data_quality']['completeness']}%")

print(f"\n📊 Key Metrics:")
for field, metrics in results.insights['key_metrics']['categorical_summary'].items():
    print(f"  - {field}:")
    print(f"      Unique values: {metrics['unique_values']}")
    print(f"      Distribution: {metrics['distribution']}")

print(f"\n🔍 Identified Patterns:")
for i, pattern in enumerate(results.insights['patterns'], 1):
    print(f"  {i}. {pattern}")

print(f"\n⚠️  Issues Identified:")
for i, issue in enumerate(results.insights['issues'], 1):
    print(f"  {i}. {issue}")

print(f"\n💡 Recommendations:")
for i, rec in enumerate(results.insights['recommendations'], 1):
    print(f"  {i}. {rec}")

# Export to HTML
html_path = results.to_html('user_subscription_analysis.html')
print(f"\n✅ Report saved to: {html_path}")
print("\n" + "=" * 80)
print("Analysis complete! Open the HTML file to view the full formatted report.")
print("=" * 80)
