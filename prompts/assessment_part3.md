## INPUTS
- **Day**: {{day}}
- **Topic**: {{topic}}
- **Scope**: {{context}}

## TASK
Generate Part 3 of the Assessment: **The Interview**.
This replaces the standard "Mentor" section.

**CRITICAL INSTRUCTION:**
Start your response with EXACTLY this line:
`# {{topic}} - Part 3: The Interview`

## SCOPE CONSTRAINT
You must ONLY ask questions based on the provided **Scope**:
> {{context}}

Do NOT ask about lists, strings, loose typing, etc. if they are not in the Scope.

## OUTPUT STRUCTURE
Provide 5-10 specific interview questions related to recent topics.
Focus on "Why", "How", and "Under the hood".

Format:
`### Interview Q{N}: [Question]`
`**Model Answer:** [STAR format or technical explanation]`

## TONE
Professional, career-focused.
