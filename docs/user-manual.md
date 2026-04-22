# User Manual (Non-Technical)

## What this tool does
This tool estimates diabetes risk from health input values and shows a risk category.

## Important disclaimer
This tool is **not** a medical diagnosis. Always consult a qualified clinician for diagnosis and treatment decisions.

## How to enter values
1. Open the app at `http://localhost:3000`.
2. Go to **Predict**.
3. Enter each requested value (pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, diabetes pedigree function, age).
4. Submit the form.

Tips:
- Use numeric values only.
- Keep values within allowed ranges shown by the form.

## How to interpret results
After submission, the app shows:
- **Risk probability** (0 to 1): higher means higher estimated risk.
- **Risk band**: low, moderate, or high.
- **Interpretation text**: short explanation for easy reading.
- **Top factors**: which inputs influenced the result most.

## Risk bands meaning
- **Low**: lower estimated risk based on entered values.
- **Moderate**: elevated estimated risk; follow-up may be appropriate.
- **High**: high estimated risk; prompt clinical follow-up recommended.

## Clinician feedback labels
Clinicians can submit confirmed outcomes to improve future model monitoring:
1. Capture the `request_id` from the prediction result.
2. Send feedback with:
   - `request_id`
   - `ground_truth_label` (true/false)
   - `label_source` (for example: clinician_review)
   - optional notes
3. Feedback endpoint: `POST /api/v1/feedback`.

## If something goes wrong
- If the page does not load, check the app URL and container status.
- If submission fails, verify numeric values and internet/network access to backend.
- If errors persist, contact your technical support team with the timestamp and request ID.
