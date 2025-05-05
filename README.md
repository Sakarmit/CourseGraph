# CourseGraph

## Project Overview
CourseGraph is an application that will show UNC Charlotte courses in an interactive node graph format.
Students will also be able to visualize:
- Degree requirements
- Course prerequisites
- Completed courses

In a manner which can help understand courses which they should attempt to complete as early as possible and courses which can be delayed.

## Setup Instructions
1. **Install [latest python version](https://www.python.org/downloads/).** 

2. **Clone the repository:**
    ```sh
    git clone https://github.com/Sakarmit/CourseGraph.git
    ```
3. **Navigate to the project directory:**
    ```sh
    cd CourseGraph
    ```
4. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
5. **Run the application:**
    ```sh
    python main.py
    ```

## Usage Details
- **View Detailed Degree Info:** Open uncached\file.json

(Following features will replace the files in the main release but a user interface has not yet been implemented)
- **Logging in:** On program start you are required to login in using your credentials.
- **Panning:** Hold left mouse button and drag to move around the map region.
- **Course Details:** Click on a specific course to highlight it's prerequisites and requisites it fulfills.
