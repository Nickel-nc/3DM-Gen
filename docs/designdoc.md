# Project Design Doc


### What do we want?
- Create app for dance movement generation on non-human joint systems in 3D space

### Why it is good for the world?
- Low datasets and experiments for utilizing non-humanoid models 
which can have practical meaning in 3-d computer vision development

### Stages
1. Research stage.
    - Search for SOTA in Human motion area
      - check feasibility
      - decompose and describe
      - repeat
      
    - -> Prepare Next Decomposed Tasklist
      
2. Env preparing
    - Public script for visualization
    - Internal script for dataset creating and changing

3. Data Preparation
    - In first-hand try to handle with limited dataset

4. Feature selection

5. Model preparation and fuse

### MVP expected functions
- GUI or streamlit web app
- Can load custom audio tracks
- Can grasp beat size from track and use it
- Exist feasible min dataset. ~50 samples for 2-3 genres
- Have trained model to generate dance sequences

### Further development
- pass

### Limitations
- can we handle good enough quality with few shot models?