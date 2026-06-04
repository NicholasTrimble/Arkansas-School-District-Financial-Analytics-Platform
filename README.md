![Dashboard Screenshot](./Schooldata.png)

![Dashboard Screenshot](./Schoolinfo.png)

# Arkansas Public School Financial Analytics: An Independent Spending Report

I built this project to look at how public education funds are actually split up across Arkansas. When you look at statewide education data, it's easy to get overwhelmed by thousands of rows of numbers. I wanted to build an automated system that handles the heavy lifting, gathering the data, cleaning it up, and turning it into clear charts that show exactly which schools are running highly efficient classrooms and which ones are burning too much money on central office administration.

The project uses a Python pipeline (etl_pipeline.py) to fetch data from the live federal education database. It strips out missing data codes, pairs the numbers with actual local school names, and streams everything into a local SQL database warehouse that I named arkansas_analytics.db and a clean spreadsheet file for easier access called arkansas_school_finance.csv. From there, I built a two page interactive Power BI dashboard to map out the different trends.

Direct Action Items: Where School Spending Needs to Improve

The biggest takeaway from this data is that we have a massive gap in how efficiently money is used across different towns. If we want to improve public school funding in Arkansas, there are three specific spending bottlenecks that need to be addressed immediately:

1. We need to fix the administrative bloat in mid-sized districts.

It is one thing for a tiny school to have high overhead because they don't have enough students to balance out a superintendent's salary. But it is a massive red flag when a mid sized district with thousands of students spends more on offices than on teachers.

Pine Bluff School District is the prime example here. They have a healthy population of 3,059 students and bring in over $43.9 Million in total revenue. Yet, they spend $19.63 Million on administration and only $18.11 Million on direct classroom instruction. That leaves them with a top heavy administrative overhead ratio of 108.40%. There is absolutely no reason a district of this size should be trapping more capital in central operations than it gives to its teaching staff. Administrative workflows here need a serious audit to redirect millions of dollars back into local classrooms.

KIPP Delta Public Schools faces a similar structural bottleneck. Managing ,1337 students, their administrative costs $8.99 Million significantly outpace what goes to the classroom $6.52 Million, landing them at a 137.98% overhead ratio. For a district with over a thousand kids, these funds are being heavily misallocated.

2. Consolidate and Share Administration for Micro Districts

When you look at the scatter plot on Page 2 of the dashboard, you can see a dramatic curve showing that our smallest schools are being absolutely crushed by fixed executive costs.

ResponsiveEd Premier High School in Little Rock is the most severe anomaly in the state. They have an enrollment of just 95 students, but they are paying $667,000 for administration against a tiny classroom footprint of just $308,000. That means they spend an extreme 216.56% on administrative support for every single dollar that reaches a teacher.

We see the exact same thing happening at Graduate Arkansas School with a 119 students / 167.12% admin ratio and ScholarMade Achievement Place with a 333 students / 165.86% admin ratio.

My proposed solution is that these small districts don't need to shut down their schools, but they desperately need to share administrative staff. By creating regional administrative hubs where multiple small schools share a single central office, accounting team, and superintendent footprint, we could free up hundreds of thousands of dollars per school to hire better teachers and upgrade classroom technology.

3. Rebalance Spending in Funding-Heavy Districts

Some districts get an absolute flood of resources but still fail to prioritize the classroom as much as they should. Earle School District has a small footprint of 540 kids but manages an intense $16,457.41 of spending per student. Despite having all that capital to work with, their administrative overhead ratio sits at a top heavy 103.35% which is $3.24M on admin vs $3.13M on teachers. When a school is blessed with high per student funding, leadership needs to ensure that funding directly elevates the student experience rather than padding support services.

## Examples of Excellence: The Efficient Models

To prove that high overhead isn't inevitable, we can look at a few local school systems that are executing wonderfully:

    Arkansas Virtual Academy: This program manages 2,474 students while maintaining a highly optimized administrative ratio of just 26.96%. They keep their per student spending at a lean $7,847.62, showing exactly how to scale a student body without letting executive costs balloon and get our of control.

    Palestine-Wheatley School District: This is a fascinating model because they spend a massive $21,567.63 per student on a smaller footprint of 828 kids. Usually, lower enrollment numbers cause overhead to spike, but Palestine-Wheatley manages to keep its administrative ratio down to an efficient 57.78%. This proves that a district can receive massive funding and successfully route the vast majority of it straight to the classroom.

## Technical Architecture: How the Platform Works

I designed this project using a clean, separate structure so that the data gathering, storage, and visual chart layers don't interfere with each other:

    Data Collection & Cleaning (etl_pipeline.py): Written in Python 3.13 using the pandas library, this script queries the live REST API gateway. It checks for rows where local reporting entities left fields blank which the federal government codes as -1 placeholders and cleanly purges them to keep our metrics true.

    Network resilient backup mirror: Because federal public sector servers are notoriously slow and prone to timing out, I built an automated network handler. If the live API fails to respond or hits a connection issue, the script automatically switches tracks and runs its processing data through a local, unedited copy of the raw data file i named raw_api_backup.json. This ensures the warehouse can always refresh smoothly without crashing.

    SQL Storage Warehouse (arkansas_analytics.db): Database connections are handled using SQLAlchemy. The script automatically checks its environment; it defaults to a portable local SQLite database file for easy local development.
    
## A Deep Dive Into My Local District: Heber Springs School District

Since my kids go to school here, I wanted to run our local Heber Springs data through this pipeline to see exactly how our town handles its public education budget. Local school spending is a topic everyone has an opinion on, so I wanted to look past the rumors and see what the data actually says. 

The pipeline pulled a very clean, stable financial footprint for Heber Springs:
*   **Total Enrollment:** 1,536 students
*   **Total Revenue:** $18,149,000.00
*   **Classroom/Teacher Spending:** $8,794,000.00
*   **Administrative/Support Spending:** $5,608,000.00
*   **Calculated Spending Per Student:** $10,555.99
*   **Administrative Overhead Ratio:** **63.77%**

## My Takeaway on Heber Springs:
The good news is that the local administration is doing a solid job of keeping its budget well balanced. An administrative overhead ratio of 63.77% means that for every dollar spent inside a classroom on teachers and supplies, only about 64 cents is being used to run the central offices and support infrastructure. 

With roughly 1,500 kids, Heber Springs sits right in a healthy "sweet spot" for public school scaling. It has enough students to easily absorb fixed executive costs like superintendent salaries and school board operations so that those costs don't eat up a massive percentage of the budget which is the exact structural trap we see crushing the smaller districts in the state. 

At $10,555.99, our spending per student lands right on the healthy state baseline average for Arkansas. More importantly, because total revenue outpaces total spending by nearly two million dollars, the district is living comfortably within its means rather than running a deficit. It serves as a great example of a stable, properly scaled public school system on the dashboard.
