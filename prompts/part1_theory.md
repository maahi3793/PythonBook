You are writing a computer science textbook chapter.

## INPUTS
- **Topic**: {{topic}}
- **Day Number**: {{day}}
- **PyDaily Lesson Content**: 
```
{{lesson_content}}
```

## TASK
Write a comprehensive theory section. This should feel like reading a university textbook - thorough, precise, but still accessible.

## OUTPUT STRUCTURE

### What You'll Learn
- Bullet point 1 (key concept)
- Bullet point 2 (key skill)
- Bullet point 3 (practical application)
- Bullet point 4 (interview relevance) [optional]

### Theory

Start with a **real-world analogy** to ground the concept.

Then explain the concept thoroughly (800-1200 words):
- What is it?
- Why does it exist?
- How does Python implement it?

Include an **"Under the Hood"** subsection explaining:
- How Python internally handles this
- Memory considerations
- Performance characteristics

### Diagrams

Include Mermaid diagrams where helpful:
```mermaid
graph TD
    A[Concept] --> B[Implementation]
```

## IMAGE PLACEHOLDERS

When a visual diagram would be helpful, use this exact format:

<!-- IMAGE_PLACEHOLDER: IMG_CH{{day:02d}}_01 -->
<!-- DESCRIPTION: Brief description of what the image should show -->
<!-- SUGGESTED_URLS:
  - https://example.com/relevant-image.png
  - https://another-site.com/diagram.png
  - https://stackoverflow.com/questions/12345 (if contains relevant diagram)
-->

Search for actual URLs from:
- RealPython.com
- Python.org
- GeeksForGeeks
- Stack Overflow answers with diagrams
- pythontutor.com

## TONE
Academic but approachable. Like MIT OpenCourseWare or "Fluent Python" by Luciano Ramalho.

## FORMAT
Return as Markdown with proper headings (##, ###).
Use code blocks with syntax highlighting for Python code.
