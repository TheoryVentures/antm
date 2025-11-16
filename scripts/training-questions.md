# Validation Evaluations - Round 1

Questions 1-10 (10 questions)

Use the **Observations** block below as the answer key reference: the `question` field shows the prompt as players see it, the remaining keys (e.g. `warehouse_sk`, `category`, `revenue_impact`, etc.) correspond to the correct answers, and `difficulty` denotes the relative challenge of the question.

---

## the warehouse that causes revenue drops

**Question:** Store #5's November 2022 revenue dropped from $500K in October to $300K. Investigate which warehouse experienced an inventory shortage that affected Store #5, and identify which product category was most impacted by this shortage. What was the revenue impact in dollars for this specific warehouse-category combination?

**Observations:**

```json
{
  "question": "Store #5's operations team noticed inventory shortages from one warehouse in November 2022. Despite overall revenue growth, investigate which warehouse experienced an inventory shortage that affected Store #5, and identify which product category was most impacted by this shortage. What was the revenue change in dollars for Store #5 in this specific warehouse-category combination from October to November 2022?",
  "warehouse_sk": 3,
  "category": "Jewelry",
  "revenue_impact": -32798.3
}
```

---

## the state that has return spikes

**Question:** January 2023 saw a spike in item returns in one state. What percentage of December revenue in the biggest returns category should be discounted due to those returns?

**Observations:**

```json
{
  "question": "January 2023 saw a spike in item returns in one state. What percentage of December revenue in the biggest returns category should be discounted due to those returns?",
  "state": "CA",
  "category": "Jewelry",
  "return_count": 2500,
  "return_value": 691182.47,
  "difficulty": 1
}
```

---

## the item that loses revenue

**Question:** Sales for an item spiked for a few weeks, but revenue is down. Figure out which item, what the error was, and calculate the lost revenue.

**Observations:**

```json
{
  "question": "Sales for an item spiked for a few weeks, but revenue is down. Figure out which item, what the error was, and calculate the lost revenue.",
  "item_sk": 2,
  "lost_revenue": 45770.69,
  "difficulty": 1
}
```

---

## the product that sells most

**Question:** Which product had the highest sales in 2019? Give the name and total quantity.

**Observations:**

```json
{
  "question": "Which product had the highest sales in 2019? Give the name and total quantity.",
  "item_sk": 8888,
  "total_quantity": 661,
  "difficulty": 1
}
```

---

## the profit that increases year over year

**Question:** How much did our net profit increase from 2021 to 2022?

**Observations:**

```json
{
  "question": "How much did our net profit increase from 2021 to 2022?",
  "profit_increase": 7934200.86,
  "difficulty": 1
}
```

---

## the category that sells most

**Question:** What was our most popular category in 2023 (by total quantity of items sold)?

**Observations:**

```json
{
  "question": "What was our most popular category in 2023 (by total quantity of items sold)?",
  "category": "Shoes",
  "difficulty": 1
}
```

---

## the year that needs validation

**Question:** In which year did we have the lowest net profit from sales?

**Observations:**

```json
{
  "question": "In which year did we have the lowest net profit from sales?",
  "year": 2021,
  "difficulty": 1
}
```

---

## the store that has highest profit in 2022

**Question:** In 2022, which store had the highest net profit in sales? Give the name of the store.

**Observations:**

```json
{
  "question": "In 2022, which store had the highest net profit in sales? Give the name of the store.",
  "store_name": "Store 3",
  "difficulty": 1
}
```

---

## the city that sells most items in 2022

**Question:** In 2022, which city had the highest number of items sold? How many items?

**Observations:**

```json
{
  "question": "In 2022, which city had the highest number of items sold? How many items?",
  "city": "Homestead",
  "items_sold": 133797,
  "difficulty": 1
}
```

---

## the product that sells most in 2022 holidays

**Question:** What is the name of our best-selling product during the 2022 holiday season?

**Observations:**

```json
{
  "question": "What is the name of our best-selling product during the 2022 holiday season?",
  "item_sk": 3434,
  "difficulty": 1
}
```

---
