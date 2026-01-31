You are writing a weekly summary chapter for a Python textbook.

## INPUTS
- **Week Number**: {{week}}
- **Days Covered**: {{start_day}} - {{end_day}}
- **Topics This Week**:
```json
{{topics}}
```
- **Key Concepts Introduced**:
```
{{key_concepts}}
```

## TASK
Write a "Think Like a Developer" summary that connects this week's lessons to real-world software development.

## OUTPUT STRUCTURE

### Week {{week}} Summary: [Creative Title]

**What We Covered:**
- Day X: Topic 1
- Day Y: Topic 2
- ...

**The Big Picture:**
[2-3 paragraphs connecting all the topics together. How do they relate? Why did we learn them in this order?]

### Thinking Like a Developer

**This Week's Mental Models:**
[What frameworks for thinking should the reader have developed?]

**How Professionals Use This:**
[Concrete examples of how working developers use these concepts daily]

**Code Smell to Avoid:**
```python
# Bad pattern (explain why)
```

**The Clean Way:**
```python
# Good pattern (explain why)
```

### Interview Prep Corner

**Likely Questions About This Week's Topics:**
1. Question 1 + Brief answer approach
2. Question 2 + Brief answer approach

**System Design Tie-in:**
[How might these concepts appear in a system design interview?]

### Reflection Questions

Ask the reader to think:
1. "How would you explain [concept] to a non-technical person?"
2. "What's one thing you could refactor in your own code using [technique]?"
3. "When would you NOT use [approach]?"

### Looking Ahead

[Tease what's coming next week and how it builds on this foundation]

## TONE
Encouraging, synthesizing. Like a professor summarizing the week's lectures.

## FORMAT
Return as Markdown.
