# shrinkage-tracker
This is an anonymised version of a shrinkage tracker I was involved in building as part of my internship as a data analyst. The data sources provided include extracts obtained from a data lake retrieved and modified using SQL and then exported to a CSV file. Here is a breakdown of these files:
* _AbsenceData.csv_: This includes absence data for employees. (N.B.: Absence refers to any time spent by the employee not carrying out their official role, hence the inclusion of vehicle checks). Interestingly, an entire shift absence is denoted as starting and ending at 00:00:00. Power BI recognised this as 0 hours, so logic was put in place to recognise this as the employee's total working hours on that day. Further cleaning was carried out on the absence types, to categorise absences into 5 distinguishable categories.
* _PT63.csv_: This file sets out the core shift hours and shift type per day. Cleaning this data included replacing the 0 values _PT63DailyWorkingHrs_ with _null_ to follow best data handling practices.
* _TeamList.csv_: This file (pretty self-explanatory) lists the team members and their details (with GDPR protocols followed of course!). In order to allow this file to "speak to" the _PT63.csv_ file, the valid date range was expanded to new rows of daily dates per employee. However, as these employees were permanent and as a result, their end dates were set to 31/12/9999. So instead of creating tens of millions of new rows, a proxy date in the future was used.

## Back-end (Power Query M) methodology
After cleaning the data, _PT63.csv_ was merged onto _TeamList.csv_ to establish a consolidated 'timetable' for all employees. A custom ID key was created for both queries to allow a relationship between this and the absence data. 

## Front-end (DAX) methodology
A many-to-one relationship was created between the Absence data and the consolidated team shift data. Measures were then created for:
* Shift Hours
* Annual Leave
* Training
* Sickness
* Vehicle Checks
* Other
* Total Shrinkage
  
Similar Measures were then created for their respective percentages the latter 6 of these measures. Due to the nature of the data, shrinkage hours were not necessarily set to be equal to the shift hours, so logic was put in place to correct this using another Measure. This ensures visuals show accurate values for shrinkage.

## Page breakdown
* **Headline View**: This tab shows a high-level overview of shrinkage over the time range the data covers
* **County/Region View**: This tab shows a matrix of shrinkage and county, which uses conditional formatting to highlight days when shrinkage is particularly high for any region
* **Gantt**: This tab gives a Gantt chart of shift type and shrinkage, allowing planners to view availability for any day
* **Short Notice Shrinkage**: This tab shows the number of occurrences and hours lost for short notice shrinkage. This allows planners and managers to pinpoint why short-notice shrinkages are occurring and whether there are any 'repeat offenders
* **Sickness Occurences**: This tab allows managers to see if there are any patterns in illnesses occurring over the year. Due to the size of this dataset, this graph isn't very telling, but in the original project, this tab was used for planning ahead for a potential incoming rise in illnesses (e.g. the December period)
* **Team List**: This showed the overall team list. Again, this isn't as helpful here given the size of the dataset sample

>[!NOTE]
> Each tab has filters that allow you to adjust your view of the page, which can be accessed by ctrl + clicking on the filters button on the top left of a pane and closing likewise
