<CRITICAL_REQUIREMENT>
You are an expert Python developer.

Implement an Exercise Tracker feature.

The system MUST:
- Allow user to add repetitions, sets, and weight
- Store workout history
- Validate input before saving
</CRITICAL_REQUIREMENT>

<CONTEXT>
From SRS:
- User logs workout details
- Adds reps, sets, weight
- System validates input
- System saves workout data

Errors:
- Missing fields → prompt user
- Save failure → error message
</CONTEXT>

<REITERATION>
REMEMBER:
- Store data in database
- Include validation and error handling
</REITERATION>