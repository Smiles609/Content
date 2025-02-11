import os

# Define the project structure
project_structure = {
    'yoova': {
        'backend': {
            'models': ['ai_model.py', 'db_model.py'],
            'routes': ['content_routes.py', 'user_routes.py'],
            'services': ['script_service.py', 'thumbnail_service.py'],
            'database': ['database.db'],
            'utils': ['helpers.py'],
            'files': ['app.py', 'requirements.txt']
        },
        'frontend': {
            'public': ['index.html','script.js','style.css'],
            'src': {
                'assets': [],
                'components': [],
                'pages': ['HomePage.jsx', 'ResearchPage.jsx', 'ScriptPage.jsx', 'ThumbnailPage.jsx'],
                'services': ['api.js'],
                'files': ['App.js', 'index.js']
            },
            'files': ['package.json']
        },
        'docs': ['project_report.md'],
        'files': ['.gitignore', 'README.md', 'run.sh']
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for file in content:
                file_path = os.path.join(path, file)
                with open(file_path, 'w') as f:
                    pass

def main():
    create_structure('.', project_structure)
    print("Project structure for 'yoova' created successfully.")

if __name__ == "__main__":
    main()