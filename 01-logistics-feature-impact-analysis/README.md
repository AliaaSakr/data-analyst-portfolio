# Product Feature Impact Analysis: Bulk Upload & Delivery Window

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![PowerPoint](https://img.shields.io/badge/PowerPoint-B7472A?style=for-the-badge&logo=microsoft-powerpoint&logoColor=white)
![Industry](https://img.shields.io/badge/Industry-Logistics-blueviolet?style=for-the-badge)

**Did two new features actually work, and who are they working for?**

| | |
|---|---|
| **Industry** | Logistics & last-mile delivery (B2B2C platform) |
| **Role** | Product / Data Analyst |
| **Tools** | Python (pandas, SciPy, seaborn), Chi-square test, segmentation, matched comparison |
| **Deliverables** | Analysis notebook, insights deck (PDF) |
---

## 1. The Business Problem

A delivery platform launched two features in the same quarter:

- **Bulk Shipment Upload:** merchants upload a CSV to create up to 500 shipments at once. The product team believed it would **reduce churn** among merchants most at risk of leaving.
- **Delivery Window Selection:** after pickup, customers get an SMS to choose a 4-hour delivery window. The team believed it would **reduce failed first-attempt deliveries** and lower re-delivery costs.

The team needed to know: **did each feature work, and should they keep investing?** Event tracking was not live on launch day, so early-adopter data was incomplete.

![Summary](images/summary.png)

## 2. The Short Answer

| Feature | What the data shows | Verdict |
|---|---|---|
| **Bulk Upload** | Adopters churn at 9.2% vs 28.0% for non-adopters, but adopters are also much bigger merchants (4.2x the monthly volume). The gap is mostly selection, not proof the feature retains merchants. | Invest for growth and engagement. Do **not** claim it reduces churn. Analyst's causal confidence: low (20-30%). |
| **Delivery Window** | Customers who chose a window had a 79.8% first-attempt delivery rate vs 70.2% (+9.6 pp). The overall lift looked small (+3.8 pp) only because 44% of customers use it. | Keep the feature. The problem is **adoption**, not the feature. Analyst's causal confidence: moderate (40-50%). |

## 3. Key Insights

**Bulk Upload**
- 40% of merchants tried it, but only 11% became heavy users (11+ uploads).
- Churn falls as usage rises: 28.0% (none) → 7.8% (light) → 11.3% (medium) → 5.6% (heavy). Statistically very unlikely to be chance (χ² = 51.17, p < 0.0001).
- But adoption is skewed toward healthy merchants: 77% of Enterprise merchants adopted vs only 20% of SMB, the segment that churns most (28.7%).
- Within SMB the gap is still real (32.0% vs 15.4%), but growing merchants likely adopt the feature *and* stay, so the cause could be growth rather than the feature.
- Merchants who hit upload errors churned *less* (7.8% vs 25.0%), a sign that errors reflect engagement, not failure.

**Delivery Window**
- Overall first-attempt rate: 70.6% before launch → 74.4% after (+3.8 pp), which looks underwhelming.
- Splitting by adoption shows the true effect: +9.6 pp for customers who chose a window. 9.6 pp x 44% adoption ≈ the observed overall lift, so the numbers reconcile.
- The effect appears in every city (+8.1 to +11.5 pp), and adoption is flat across cities (43-46%). The bottleneck is awareness/SMS, not geography.
- When compared against similar customers (same merchant tier and city), the gap shrinks, so selection on those factors is not the whole story. Unmeasured factors (address quality, customer reliability) could still bias the result.

## 4. Recommendations

1. **Bulk Upload:** survey SMB non-adopters to learn why they don't use it (discovery, UX, or value); target SMBs with a prompt when their volume grows; run a matched-cohort or A/B study before claiming any retention effect.
2. **Delivery Window:** pull SMS delivery and click logs, survey non-adopting customers, then A/B test the SMS message to lift adoption from 44% toward 60%+ (impact = effect size x adoption rate, about 5.8 pp at 60%).
3. **Measurement:** always segment results, report adoption rate alongside effect size, and state confidence honestly.

## 5. Approach

1. Cleaned and parsed three tables: merchants (1,000 rows), shipments (~29,000), events (~38,000); identified launch dates from the data.
2. Defined adoption by **usage depth** (none / light / medium / heavy) instead of a yes/no flag, to handle the tracking gap.
3. Compared churn across buckets and tiers; tested significance with a Chi-square test.
4. Checked for selection bias: adoption by tier, within-tier comparison, retention by adoption cohort.
5. For Delivery Window: pre/post comparison, adopter vs non-adopter split, city and tier breakdowns, and a matched comparison on tier + city.
6. Wrote a causal-evidence assessment (evidence for vs against) for each feature.

## 6. Challenges

- **Incomplete event data:** tracking started after launch, so early adopters are under-counted. Solved with usage buckets and by being explicit about the limits.
- **Selection bias:** adopters differed from non-adopters from the start, so a raw comparison would have overstated the feature's impact.
- **A misleading aggregate:** the overall Delivery Window lift hid a strong effect among adopters. Splitting by adoption exposed it.

## 7. Files

| File | What it is |
|---|---|
| [`analysis_notebook.ipynb`](code/analysis_notebook.ipynb) | Full Python analysis with comments |
| [`insights_deck.pdf`](reports/insights_deck.pdf) | Presentation of findings and recommendations |

## 8. What to Know Before Using This

- Results are observational, not from a controlled experiment. Both features need an A/B test to prove causation.
