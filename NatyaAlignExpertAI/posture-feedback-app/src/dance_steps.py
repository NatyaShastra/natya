import pickle
import os
import glob

def get_steps_from_raw_videos(raw_videos_dir='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/raw_videos'):
    """
    Get dance step names from the raw_videos directory structure
    
    Returns:
        A list of dance step names found in the raw_videos directory
    """
    steps = []
    try:
        # Get all immediate subdirectories of raw_videos
        subdirs = [d for d in os.listdir(raw_videos_dir) 
                  if os.path.isdir(os.path.join(raw_videos_dir, d))]
        steps.extend(subdirs)
        print(f"Found steps in raw_videos: {steps}")
    except Exception as e:
        print(f"Error getting steps from raw_videos: {e}")
    
    return steps

def get_available_dance_steps(model_path='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model.pkl', 
                             raw_videos_dir='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/datasets/raw_videos'):
    """
    Extract available dance steps from both the trained model and raw_videos directory
    
    Returns:
        A list of dance step names
    """
    steps = []
    
    # Get steps from the model
    try:
        with open(model_path, 'rb') as model_file:
            model_data = pickle.load(model_file)
            
        # Check if model has step_map (should be third element in tuple)
        if len(model_data) == 3 and model_data[2]:
            # Extract step names from step_map (use keys of the dict)
            steps.extend(list(model_data[2].keys()))
            print(f"Found steps in model: {steps}")
        else:
            # Add default steps if model doesn't have step information
            default_steps = ["Bharatanatyam Araimandi", "Adavu", "Nritta Hastas", "Natya Hastas"]
            steps.extend(default_steps)
            print(f"Using default steps: {default_steps}")
    except Exception as e:
        print(f"Error loading dance steps from model: {e}")
        # Add some defaults
        default_steps = ["Bharatanatyam Araimandi", "Adavu", "Nritta Hastas", "Natya Hastas"]
        steps.extend(default_steps)
    
    # Get steps from raw_videos directory
    raw_steps = get_steps_from_raw_videos(raw_videos_dir)
    
    # Combine all steps, remove duplicates, and sort
    all_steps = list(set(steps + raw_steps))
    all_steps.sort()
    
    print(f"Final combined step list: {all_steps}")
    return all_steps

def get_step_id_from_name(step_name, model_path='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model.pkl'):
    """
    Get the numeric step_id for a given step name from the model
    
    Args:
        step_name: The name of the dance step
        model_path: Path to the trained model
        
    Returns:
        The numeric step_id, or None if not found or if model doesn't support step_id
    """
    try:
        with open(model_path, 'rb') as model_file:
            model_data = pickle.load(model_file)
            
        # Check if model has step_map
        if len(model_data) == 3 and model_data[2]:
            # Get step_id from step_map
            return model_data[2].get(step_name, None)
        else:
            return None
    except Exception as e:
        print(f"Error getting step ID: {e}")
        return None