import pickle

model_paths = [
    '/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model_generated.pkl',
    '/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model.pkl'
]

for model_path in model_paths:
    print(f'Loading {model_path}')
    try:
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
            print(f'Model data type: {type(data)}')
            print(f'Model data length: {len(data) if isinstance(data, tuple) or isinstance(data, list) else 1}')
            if isinstance(data, tuple) and len(data) >= 2:
                print(f'Model type: {type(data[0])}')
                print(f'Label encoder type: {type(data[1])}')
                if len(data) >= 3:
                    print(f'Step map type: {type(data[2])}')
                    if isinstance(data[2], dict):
                        print(f'Step map: {data[2]}')
    except Exception as e:
        print(f'Error loading model: {e}')
    print('-' * 50)