# Customer Survey Insights: Why Shoppers Leave Without Buying

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Power Query](https://img.shields.io/badge/Power_Query-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![SQL](https://img.shields.io/badge/SQL-336791?style=for-the-badge)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)
![Industry](https://img.shields.io/badge/Industry-Retail-blueviolet?style=for-the-badge)
![Customer Insights](https://img.shields.io/badge/Analysis-Survey_Analytics-blueviolet?style=for-the-badge)

**Sales data shows who bought. This survey asked the customers who walked out why they didn't.**

| | |
|---|---|
| **Industry** | Retail (electronics) |
| **Role** | Retail Data Analyst |
| **Tools** | Power BI (DAX, Power Query), SQL, Google Sheets |
| **Deliverables** | In-store survey dashboard (the "Goal Keeper" survey) with a planning follow-up view |
| **Data & Privacy** | Logos, names, and figures are masked or replaced with sample data. The Power BI file is not included. |

---

## 1. The Business Problem

A retailer knew how many customers bought, but not why the others left empty-handed. To improve the in-store experience, the retail and planning teams needed the reasons, store by store.

The approach was simple: in each store, a staff member called the **Goal Keeper** asked customers who left **without buying** a few short questions and logged the answers. Answers were collected in Google Sheets and analyzed in Power BI, so retail and planning could act on them.

![Goal Keeper Dashboard](images/01goalkeeper.png)

## 2. The Short Answer

**Most walkouts are an availability problem, not a price or staff problem, and recovering those customers rarely works once stock returns.**

| Signal | What the data shows (sample data) |
|---|---|
| Scale | 4,551 responses from 130 stores in 5 regions over 44 days (26 February to 10 April 2023) |
| Conversion | 13.2% of surveyed customers bought (596), and 86.8% did not (3,916) |
| Main reason | The product wasn't available: about 73% of detailed reasons |
| What they wanted | TVs (about 45%), then small appliances (22%), large appliances (15%), mobiles (9%), and air conditioners (5%) |
| After restocking | Only 20.8% of customers who left because of availability bought once the product was replenished |

## 3. The Dashboard

1. **Headline numbers:** responses, stores, days, and regions, with conversion to purchase.
2. **Required category** for customers who did not buy.
3. **Conversion by store type and region,** so each branch can see its own picture.
4. **Reasons for leaving:** a main reason class and a detailed list.
5. **Required category by region and cluster.**
6. **Planning follow-up:** whether the customer bought after replenishment, the planning action taken for unavailable products, and planning comments on why products were unavailable.

It can be filtered by date, store, region, and planning comment.

## 4. Key Insights

- **Availability dominates.** About 73% of detailed reasons were product availability. Among the rest, installment-financing (MiniCash) issues are the largest group (430 responses), ahead of "other" (212), questions about offers (136), delivery (27), and system problems (17). Branch and staff issues are almost absent (3 and 1).
- **Big-ticket categories lose the most.** TVs account for about 45% of what non-buyers wanted.
- **Why products weren't there:** the top planning comments were no stock across the main warehouse (316), invalid SKUs (203), no stock at any location (174), and low stock that could not be replenished (113).
- **Restocking doesn't bring them back.** Only about one in five customers (124 of 596) bought after replenishment, and for 71% of unavailable products planning noted that the product would not be available at all.
- **Financing friction is real.** Reasons include program requirements, high interest and administration fees, incomplete paperwork, and rejected requests.
- **Stores differ widely.** Conversion varies a lot by region and store type, so each branch needs its own follow-up.

## 5. Recommendations

1. **Fix availability first.** Give planning the top missing products and categories each week, starting with TVs and small appliances.
2. **Clean up invalid SKUs,** since they are the second most common reason planning gave.
3. **Follow up with customers when stock returns,** because few come back on their own.
4. **Reduce financing friction** with clearer guidance on requirements, fees, and paperwork at the till.
5. **Make the survey routine:** a short form, a weekly review, and a planning reply to each comment.

## 6. Approach

1. **Collected the responses** in Google Sheets as store staff logged them.
2. **Cleaned the answers,** which came in Arabic and English with many free-text variations, and grouped them into a small set of reason classes (availability, financing, inquiry, delivery, system, branch, staff).
3. **Built the dashboard** in Power BI, with SQL and Power Query for the data and DAX for the measures.
4. **Added the planning follow-up view** so reasons turn into actions by category, region, and cluster.

## 7. Challenges

- **Messy survey data.** Answers came in two languages and many variations, so I grouped them into clear classes before analysis.
- **A one-sided sample.** Only customers who did not buy were asked, so the survey explains walkouts but not overall satisfaction.
- **Uneven coverage.** Surveys depend on a person asking, so response counts differ by store, and every result is shown with its sample size.
- **Turning answers into action.** A reason is only useful if someone owns it, which is why the dashboard links reasons to planning comments and actions.

## 8. Files

| File | What it is |
|---|---|
| [`Goal_Keeper_Survey_Dashboard.pdf`](reports/Goal_Keeper_Survey_Dashboard.pdf) | In-store survey dashboard |

## 9. What to Know Before Using This

- All figures are masked or sample data. The project shows the method and the thinking.
- The survey covers only customers who did not buy, so it shows reasons for walkouts, not overall satisfaction.
- The Power BI file and SQL are not included in this repo.
