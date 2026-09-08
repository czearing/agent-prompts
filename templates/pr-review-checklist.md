# PR Review Checklist

## Behavior

### Purpose
What is the code for explain

### Testing
#### Interactions
1. Example: Click on the button using chrome dev tools etc

Results: All tests passed successfully etc

#### Performance
1. Example: Measure rerenders, first load, etc

Results: All tests passed successfully and performance is as optimal as it can get etc

#### Accessibility
1. Example: Does the button have the proper aria content

Results: Everything is accessible etc

### Code
[] Is each file cleanly abstracted and using existing functions to do the job
[] Do files cleanly stay under 200 lines or should they be split apart
[] Is core functionality being tested
[] Do props of components have doc comments
[] Edge cases
[] Is everything localized
[] etc add more

## PR Feedback Candidate List
Validation Status - Description
Pass - Line 100 in so in so file could be faster if they called this function.
Fail - Using this function could be faster.
