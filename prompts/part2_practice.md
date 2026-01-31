You are writing practice exercises for a Python textbook.

## INPUTS
- **Topic**: {{topic}}
- **Day Number**: {{day}}
- **Quiz Questions**: 
```json
{{quiz_questions}}
```
- **Boss Battle Challenge**: 
```
{{boss_challenge}}
```

## TASK
Write practice content that bridges theory to hands-on application.

## OUTPUT STRUCTURE

### Real-World Use Case

Start with a concrete, relatable scenario:
> "Imagine you're building a [specific application]..."

Then provide:
1. The problem statement (2-3 sentences)
2. Complete code solution with detailed comments
3. Line-by-line walkthrough explaining WHY each decision was made

Keep the scenario practical:
- Playlist manager
- Todo app
- Bank transaction system
- Social media feed
- E-commerce cart

### From the Quiz

Select 3-4 questions from the quiz data. For each:

**Question [N]:** [Show the original question]

**Correct Answer:** [The answer]

**Why This Is Correct:**
[2-3 sentences explaining the underlying concept]

**Common Mistakes:**
- Mistake 1: Why students pick wrong answer A
- Mistake 2: Why students pick wrong answer B

### Boss Challenge Walkthrough

**The Challenge:**
[Copy the boss battle challenge]

**Approach:**
1. Step 1: How to think about this
2. Step 2: Breaking it down
3. Step 3: Building the solution

**Solution:**
```python
# Complete solution with comments
```

**Alternative Approaches:**
- Approach 2: Brief description + key code
- Approach 3: When you might use this instead

## TONE
Practical, hands-on. Like a workshop instructor walking you through exercises.

## FORMAT
Return as Markdown. Use numbered lists for steps, code blocks for code.
