import pandas as pd
from analystx import analyze

df = pd.DataFrame({
    'price': [10, 20],
    'quantity': [1, 2],
    'customer_id': [101, 102]
})

print('Testing analyze function...')
result = analyze(df, business_context='Sales analysis')

print(f'\n✓ Type: {type(result).__name__}')
print(f'✓ Has to_html: {hasattr(result, "to_html")}')
print(f'✓ Has profile: {hasattr(result, "profile")}')
print(f'✓ Has kpis: {hasattr(result, "kpis")}')
print(f'✓ Has insights: {hasattr(result, "insights")}')
print(f'✓ Has report: {hasattr(result, "report")}')

print(f'\n{result}')

# Test to_html method
html_path = result.to_html('test_report.html')
print(f'\n✓ HTML exported to: {html_path}')
