![Platform Dashboard Preview](./School%20Data.png)




# Independent Research & Multi-Year Data Analysis (2022–2026)

## Project Overview

I built this project to analyze how public school funding actually gets spent across the state of Arkansas. When looking at public sector budgets, it is easy to get lost in massive spreadsheets, so I wanted to create a data pipeline and dashboard that could answer two basic, real-world questions:

    Which school districts are spending a disproportionate amount of money on administrative overhead instead of the actual classroom?

    Are these school districts adjusting their fixed costs when student populations shift, or are they holding onto bloated administrative structures while enrollment drops?

To solve this, I engineered a Python ETL pipeline to process 75 distinct historical records tracking 15 major Arkansas school districts over a five-year period (2022 to 2026). I then mapped the clean data into an interactive Power BI dashboard to expose anomalies that would normally stay hidden in raw CSV rows.
My Key Analytics Findings
1. The Administrative Overhead Anomalies

When you look at the baseline data across the state, most school districts operate pretty efficiently. Eleven out of the fifteen schools I tracked keep their administrative-to-instructional overhead ratio locked tightly between 6% and 7%. This includes big districts like Little Rock and Bentonville.

However, four specific districts immediately jumped out with double the overhead of everyone else:

    Heber Springs School District (Cleburne County)

    Fayetteville School District (Washington County)

    Jonesboro School District (Craighead County)

    Hot Springs School District (Garland County)

These four outliers have persistent administrative overhead ratios ranging from 12.8% to a peak of 14.5%. They are effectively spending double the percentage on administrative functions compared to their direct peers.
2. The Enrollment Attrition Trap

The real insight comes when you stop looking at spending in a vacuum and map it directly against a 5-year student enrollment trend line. This reveals a serious operational issue in how certain local budgets are handled:

    The Fayetteville & Heber Springs Problem: * In 2022, Heber Springs had 1,969 students and a 13.81% admin ratio. By 2026, enrollment dropped down to 1,864. But even though they were educating over 100 fewer kids, their administrative spending barely moved (only dropping from $1.44M to $1.42M), pushing their overhead ratio up to 14.12%.

        Fayetteville is even more extreme in this specific dataset. Its enrollment cut in half, dropping from 8,582 down to 3,900 over the five years. Naturally, their total revenue dropped along with the student count. But instead of cutting back on administrative costs to match the new size of the district, their admin overhead ratio spiked to its highest point of 14.23% in 2026.

This tells us that these institutions struggle to scale down fixed administrative structures when communities change and student volume decreases. Funding is systematically getting stuck at the top instead of adjusting down to protect classroom resources.
3. Per-Student Spending vs. Real Classroom Value

Looking at the numbers, total spending per student stays fairly consistent across the state—usually bounding between $5,588 and $6,500. But the internal distribution of those dollars is completely unequal.

For example, in 2026, Little Rock allocated $6,275 per student with a lean 7.63% admin ratio, meaning the vast majority of that money went toward direct student instruction. In the exact same year, Hot Springs spent a nearly identical $6,268 per student, but locked 13.57% of that allocation into administrative overhead.
How I Built the Technical Architecture

I designed this platform to be lightweight for local development but structured it to be completely ready for an enterprise cloud deployment:

    The Pipeline (etl_pipeline.py): I wrote a Python script utilizing pandas for cleaning and transforming the data, along with SQLAlchemy to manage data types and database mappings. The script automatically handles the math to generate the per-student spending metrics and the administrative overhead index.

    The Local Data Layer (arkansas_analytics.db): Instead of introducing heavy database server overhead on my local machine, I routed the pipeline into a serverless SQLite instance. It runs instantly, populates without network or password barriers, and generates a portable database file directly inside the repository directory.

    Azure Cloud Target: To make this easily deployable, I used environment-variable routing (os.getenv('AZURE_POSTGRES_CONN')). When I run this script locally, it defaults to the lightweight SQLite file. But when it is deployed to Microsoft Azure (App Services or Serverless Functions), the code detects the environment variable and automatically hooks into a production-grade cloud database without requiring any structural changes to my Python logic.

## Concluding Thoughts & Next Steps

If this were being handed off as an actual legislative audit review, the next step would be straightforward: initiate an immediate, line-item operational review of Heber Springs, Fayetteville, Jonesboro, and Hot Springs. The data clearly shows that these four districts have a rigid, top-heavy cost structure that is failing to adapt to student population shifts.