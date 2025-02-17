import os
from dotenv import load_dotenv
from tasks import research_task, write_task
from agents import blog_researcher, blog_writer
from flask import Flask, render_template, request

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the crew
crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the topic from the user
        topic = request.form.get('topic')

        if not topic:
            return render_template('index.html', error="Please enter a topic.")

        try:
            # Execute the crew process to generate the blog
            result = crew.kickoff(inputs={'topic': topic})

            # Extract the blog content from the result
            blog_content = result.get('write_task_output', "Blog generation failed.")

            return render_template('index.html', topic=topic, blog_content=blog_content)

        except Exception as e:
            return render_template('index.html', error=f"An error occurred: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
