# Project Design Doc

Note: this document is a subjective reference for key aspects of the whole development process

### Tags

- 3D point cloud sequence generation
- Skeletal 3D motion synthesis
- Non-humanoid motion control
- Audio processing
- Robotics

### What do we want?
- Create app for dance movement generation on non-human joint systems in 3D space

### Why is it good for the world?
- Low datasets and experiments for utilizing non-humanoid models 
- Can have practical meaning to perform action generation in apps that uses skeletal data, 
like 3D computer vision tasks, robotics, video games, cinematic and e.t.c

### Expected Architecture
- Monolith: math, logic, processing, model and app are working in modules 
that runs from main script as entering point
- CNN, RNN, GCN, GAN or Transformers?

### Subtasks
- Research: search and try appropriate architecture that suit dance motion generation for different joint systems
- Audio processing: Feature extraction for audio track: classify different phrases, extract bpm and other features (analyse new)
- Testing: run model on different tasks. Analyze its goodness and try to automate the process
- Involve model kinematics. Define key restriction for correct model movement and safe angles

### Stages
1. Research stage.
    - Search for SOTA in Human motion area
      - check feasibility
      - decompose and describe
      - repeat
      
    - -> Prepare Next Decomposed Tasklist
      
2. Env preparing
    - Public script for visualization
    - Internal script for dataset creating and processing

3. Data Preparation
    - Chosen paradigm: try to handle with limited dataset
    - Hand crafted dataset
    - use music genres with different rhythms (firstly 2-3)
    - data as small sequence samples for each music genre

4. Feature selection

5. Model preparation and fuse
6. Wrap model in web application
7. Create sustainable backend service
8. Formalize all the work and create final documentation


### Notes:
- Starting pose codes
- Extract music features
- Process pose and music in single pipeline. Or process pose and music in different models

### MVP expected functions
- Streamlit (or other) web app and further GUI app
- Can load custom audio tracks
- Can grasp beat size from track and use it
- Exist feasible min dataset. ~50 samples for 2-3 genres
- Have trained model to generate dance sequences

### Further development. Really won't expect in first scope
- Make generated moves available to modify and learn
- Increase moves for different genres
- Add subsplit for typical music phrases over genrres (reefs, horus, melodic e.t.c.)
- Scale model to fit different joint assets
- Apply 3D model (or models) to skeletal structure

### Risks and limitations
- Can we handle good enough quality with few shot models?
- Creating annotations for non-human motions from human motions is a separate great task
- Do we actually have sufficient human power for this project?
- SOTA is highly challenging due to spatial constraints of the body
- Need in custom processing of temporal coherency for various music genres and bits 
- Correctness of handling different time signatures (4/4, 3/4 and e.t.c) for the same BPM??