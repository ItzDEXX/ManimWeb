import os
from openai import OpenAI
import importlib.util
import sys
import subprocess

def get_solution_code(prompt):
    """
    First step: Get a Python solution with explanation for the given prompt
    """
    try:
        client = OpenAI(
            base_url="https://api.sree.shop/v1",
            api_key="ddc-txA9OuSECZ8Qufxr1BM8BE33ofIhvssZoT5KQ8PWSVg0bdBEGx"  # Replace with your API key
        )

        solution_prompt = f"""
        Please solve the following problem and provide:
        1. A clear explanation of the solution approach
        2. Python code implementing the solution
        3. An example demonstrating how the solution works
        
        Problem: {prompt}
        
        Your response should be well-structured with the explanation first, 
        followed by the code, and then the example.
        """

        response = client.chat.completions.create(
            model="claude-3-5-sonnet",
            messages=[
                {"role": "user", "content": solution_prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Error generating solution code: {str(e)}")

def get_manim_code(solution_content):
    """
    Second step: Generate Manim visualization code based on the solution
    """
    try:
        client = OpenAI(
            base_url="https://api.sree.shop/v1",
            api_key="ddc-txA9OuSECZ8Qufxr1BM8BE33ofIhvssZoT5KQ8PWSVg0bdBEGx"  # Replace with your API key
        )

        manim_prompt = f"""
        Create a full Manim visualization video (1–2 minutes long) that explains the following Python solution.
        Your generated code must follow these detailed guidelines and produce a video that fully explains 
        the concept with clear, NON-OVERLAPPING visuals and structured sections.

        Here's the solution to visualize:
        {solution_content}

        Guidelines:

        1. **Scene Layout and Positioning:**
           - Use explicit positioning with specific coordinates.
           - Center main text either at the CENTER or at `UP * 2`.
           - Arrange elements vertically using multipliers (e.g., UP or DOWN by 1, 2, or 3 units).
           - Ensure long text fits the screen by using `Text()` and then applying `.scale(0.7)` or smaller if needed.
           - Keep all content within the coordinate ranges: x-axis between -7 and 7, and y-axis between -4 and 4.
           - CRITICAL: Ensure a minimum spacing of 1 unit between all elements to prevent overlap.

        2. **Animation Structure (Total Video Duration: 1–2 Minutes):**
           - **Start (15–20 seconds):**
             - Display a title/introduction with a centered title (use `Text("Title").scale(0.8)` at `UP * 2`).
             - Include an introductory paragraph beneath the title, ensuring at least a 1-unit vertical gap.
           - **Middle (45–60 seconds):**
             - Present the main concepts with clear visualizations.
             - For equations, use `Text()` instead of `MathTex()` to avoid LaTeX dependency.
             - Add visual elements (e.g., shapes like squares, circles) with contrasting standard colors (BLUE, RED, GREEN, YELLOW).
             - Use connecting lines or arrows to relate elements, ensuring clarity and no overlapping.
             - Insert explanation texts near the visual elements with proper spacing (at least 0.5 units apart).
           - **End (15–30 seconds):**
             - Provide a summary or comparison section with a final summary title (again at `UP * 2` using `Text().scale(0.8)`).
             - Display concluding text below the summary header.
             - Include smooth transitions (using `FadeIn`, `FadeOut`, or `Transform`) with explicit `run_time` values (minimum 0.5 seconds).

        3. **Text and Font Management:**
           - Use `Text()` for all text including mathematical expressions (DO NOT use MathTex).
           - CRITICAL: For Manim 0.17.3 compatibility, NEVER use scale parameter in the Text constructor. Always use the scale method after creating the Text object.
           - EXAMPLE: Use `Text("Your text").scale(0.7)` instead of `Text("Your text", scale=0.7)`.
           - Scale text appropriately: `.scale(0.7)` for normal text and `.scale(0.8)` for titles.
           - For long text, use an even smaller scale (0.5 or 0.6) to ensure it fits.
           - Center all text with `.center()` or `.move_to()` and ensure a minimum spacing of 1 unit between elements.
           - Break long paragraphs into multiple lines using line breaks for clarity.
           - For complex algorithms, break down explanations into smaller chunks with clear transitions between them.

        4. **Color and Visibility:**
           - Apply standard Manim colors (BLUE, RED, GREEN, YELLOW) for different elements.
           - Set opacities for overlapping elements (preferably 0.8 or less) to maintain clarity.
           - Use contrasting colors to distinguish related elements.
           - Ensure all fade transitions (FadeIn, FadeOut) have a `run_time` of at least 0.5 seconds.
           - CRITICAL: Always fade out or remove previous elements before introducing new ones in the same area.
           - When transitioning between sections, use FadeOut for all existing elements before introducing new ones.

        5. **Mathematical Elements:**
           - For mathematical expressions, use `Text()` with simple formatting instead of `MathTex()`.
           - For example, use `Text("3 + 2 = 5")` instead of `MathTex("3 + 2 = 5")`.
           - Position text at specific coordinates.
           - Attach labels to equations with `.next_to()` using explicit directions (UP, DOWN, LEFT, RIGHT) and a buffer of at least 0.5.

        6. **Required Code Structure:**
           - Begin with:
             from manim import *

             class ConceptVisualization(Scene):
                 def construct(self):
                     # Scene setup
                     self.camera.background_color = BLACK
           - Structure the code into three clear sections (Start, Middle, End) with explicit `run_time` parameters for all animations.
           - Use appropriate `wait()` calls between transitions to allow viewers to absorb each part of the explanation.
           - CRITICAL: Ensure that no text overlaps and every element is clearly visible throughout the video.
           - CRITICAL: Properly manage transitions by fading out old elements before introducing new ones.
           - For complex algorithms, consider breaking the visualization into multiple scenes or subsections.
           - Add a render method at the end of the file:
             if __name__ == "__main__":
                 scene = ConceptVisualization()
                 scene.render()
           
        7. **Important Technical Requirements:**
           - The code MUST be compatible with manim==0.17.3
           - Avoid any features or syntax that are not supported in this version
           - DO NOT use MathTex or any LaTeX-dependent features
           - CRITICAL: For Text objects, NEVER use scale parameter in the constructor. Always use the scale method after creating the object.
           - Ensure all text elements remain within the visible window at all times
           - CRITICAL: Prevent any text or visual elements from overlapping by using proper spacing and positioning
           - CRITICAL: Always use proper fade transitions (FadeOut) for old elements before introducing new ones
           - For complex algorithms like flood fill, use a step-by-step approach to explain the algorithm clearly

        8. **Handling Complex Problems:**
           - For algorithms like flood fill, break down the explanation into clear steps:
             1. Explain the problem statement with a simple example
             2. Visualize the input data structure (e.g., grid for flood fill)
             3. Demonstrate the algorithm step by step with clear visual cues
             4. Show the final result and summarize the approach
           - Use animations to show how the algorithm progresses (e.g., color changes in flood fill)
           - For recursive algorithms, clearly show the recursion tree or stack
           - Simplify complex examples if needed, but ensure they still demonstrate the key concepts

        IMPORTANT: Do NOT include any markdown code block markers (like ```python or ```) in your response. 
        Just provide the raw Python code that can be directly executed.

        Generate the complete Manim code following the above guidelines that produces a 1–2 minute video 
        with a full explanation of the provided solution.
        """

        response = client.chat.completions.create(
            model="claude-3-5-sonnet",
            messages=[
                {"role": "system", "content": """You are a Manim expert who creates precise, error-free visualizations.
                Always use explicit positioning, proper scaling, and specific timing for animations.
                Follow these rules:
                1. Never position elements without specific coordinates
                2. CRITICAL: For Text objects, NEVER use scale parameter in the constructor. Always use the scale method after creating the object.
                3. Include specific run_time for all animations
                4. Add wait() calls between transitions
                5. Keep all elements within visible screen bounds
                6. CRITICAL: Maintain proper spacing between elements (at least 0.5 units)
                7. Handle text wrapping for long strings using line breaks
                8. Implement smooth transitions between scenes
                9. Ensure compatibility with manim==0.17.3
                10. Include a render method at the end of the file
                11. DO NOT use MathTex or any LaTeX-dependent features
                12. DO NOT include markdown code block markers (```python or ```) in your response
                13. CRITICAL: Prevent ANY text overlap by using proper spacing and positioning
                14. Use smaller text scales (0.5-0.6) for longer explanations
                15. Position elements with at least 1 unit of vertical space between them
                16. CRITICAL: Always fade out old elements before introducing new ones in the same area
                17. Use proper transitions between sections with FadeOut for all existing elements
                18. For complex algorithms, break down the explanation into clear, manageable steps
                19. Use animations to show algorithm progression (e.g., color changes in flood fill)
                20. Simplify complex examples if needed while preserving key concepts"""}, 
                {"role": "user", "content": manim_prompt}
            ]
        )

        # Get the raw content
        manim_code = response.choices[0].message.content
        
        # Clean up the code by removing any markdown code block markers if they exist
        manim_code = manim_code.replace("```python", "").replace("```", "").strip()
        
        return manim_code

    except Exception as e:
        raise Exception(f"Error generating Manim code: {str(e)}")

def render_manim_code(file_path):
    """
    Render the generated Manim code
    """
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist.")
            return False
            
        # Check if manim is installed
        try:
            import manim
            print(f"Manim version {manim.__version__} is installed.")
        except ImportError:
            print("Manim is not installed. Please install it with 'pip install manim==0.17.3'")
            return False
            
        # Use subprocess to run the manim command with full path
        print(f"\nRendering Manim visualization using manim command...")
        try:
            # Replace with your actual path to manim.exe
            full_manim_path = r"C:\Users\Asus\AppData\Roaming\Python\Python312\Scripts\manim.exe"

            result = subprocess.run(
                [full_manim_path, "-pql", file_path, "ConceptVisualization"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Error rendering Manim code: {result.stderr}")
                print("\nTry running the command manually:")
                print(f"{full_manim_path} -pql {file_path} ConceptVisualization")
                return False
            else:
                print("Manim visualization rendered successfully!")
                print(result.stdout)
                return True
        except Exception as e:
            print(f"Error running manim command: {e}")
            print("\nTry running the command manually:")
            print(f"{full_manim_path} -pql {file_path} ConceptVisualization")
            return False
    
    except Exception as e:
        print(f"Error rendering Manim code: {e}")
        return False

def main():
    print("Welcome to the Manim Code Generator!")
    print("This tool will generate a Manim visualization for a Python problem.")
    print("You can enter a simple problem like 'explain addition' or a complex algorithm like 'flood fill'.")
    print("For complex problems, please provide a clear description of the algorithm and example inputs/outputs.")
    print("\n" + "="*80 + "\n")
    
    # Get the problem from the user
    prompt = input("Enter the problem you want to visualize: ")
    
    try:
        print("\nGenerating Python solution with explanation...")
        print("This may take a moment for complex problems...")
        solution_content = get_solution_code(prompt)
        
        print("\nGenerated Solution:")
        print(solution_content)
        
        print("\nGenerating Manim visualization code...")
        print("This may take a moment for complex problems...")
        manim_code = get_manim_code(solution_content)

        print("\nGenerated Manim Code:")
        print(manim_code)
        
        # Save the Manim code to a file
        output_file = "manim_visualization.py"
        with open(output_file, "w") as f:
            f.write(manim_code)
        
        print(f"\nManim code has been saved to '{output_file}'")
        
        # Ask the user if they want to render the visualization
        render_choice = input("\nDo you want to render the visualization? (y/n): ").strip().lower()
        should_render = render_choice == 'y' or render_choice == 'yes'
        
        if should_render:
            print("\nAttempting to render the Manim code...")
            print("WARNING: This requires sufficient disk space (at least 500MB free).")
            print("If you encounter 'No space left on device' errors, try clearing space first.")
            print("You can free space by running: rm -rf /Users/rushil/Documents/Manim_dev/media/")
            
            success = render_manim_code(output_file)
            if not success:
                print("\nRendering failed. You can try to render it manually with:")
                print(f"manim -pql {output_file} ConceptVisualization")
        else:
            print("\nSkipping rendering. To render the visualization later, run:")
            print(f"manim -pql {output_file} ConceptVisualization")
            print("\nNOTE: Rendering requires sufficient disk space and Manim to be installed.")
        
        return manim_code

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    main()
