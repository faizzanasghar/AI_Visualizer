AI Pathfinder: Uninformed Search Visualizer
An interactive Python application that visualizes how "blind" search algorithms navigate a grid environment. This tool demonstrates pathfinding from a user-defined Start Point (S) to a Target Point (T) while navigating around static obstacles. 

🚀 Features

Interactive Grid: Click to set the Start point, Target point, and draw walls. 


Step-by-Step Visualization: Watch the algorithm "flood" the grid in real-time. 
+1

Color-Coded Feedback:

Green: Start Node 
Blue: Target Node 
Red: Static Obstacles (-1) 
Cyan: Frontier Nodes (waiting to be explored) 
Orange: Explored Nodes 
Yellow: Final successful path 

🧠 Algorithms Implemented
This project implements six fundamental uninformed search strategies:


Breadth-First Search (BFS): Explores level by level to find the shortest path in unweighted grids. 


Depth-First Search (DFS): Dives deep into branches before backtracking. 

Uniform-Cost Search (UCS): Expands nodes based on path cost. 


Depth-Limited Search (DLS): A DFS variant with a predetermined depth limit. 


Iterative Deepening DFS (IDDFS): Repeatedly applies DLS with increasing limits to find the optimal goal. 


Bidirectional Search: Searches simultaneously from Start and Target to meet in the middle. 

🛠️ Movement Logic
The AI follows a strict Clockwise Movement Order including specific diagonals :
+1

Up 
Right 
Bottom 
Bottom-Right (Diagonal) 
Left 
Top-Left (Diagonal) 

💻 How to Run
Prerequisites: Ensure you have Python 3.x installed.

Clone the Repository:

Bash
git clone https://github.com/faizzanasghar/AI_A1_24F_0052.git
cd AI_A1_24F_0052
Run the Application:

Bash
python main.py
📋 Submission Details

Authors.
Muhammad Faizan Asghar
Ahmad Hassan 
