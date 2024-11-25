import os
import sys
import subprocess
import tempfile
from typing import List
from datetime import datetime


class GitVisualizer:
    def __init__(self, repo_url: str, output_file: str, commit_date: str):
        self.repo_url = repo_url
        self.commit_date = commit_date
        self.output_file = os.path.join(os.getcwd(), output_file)  # Файл сохраняется в текущей директории
        self.repo_path = self.clone_repository()

    def clone_repository(self) -> str:
        """
        Клонирует репозиторий по URL во временную папку.
        """
        temp_dir = tempfile.mkdtemp()
        try:
            print(f"Cloning repository from {self.repo_url} into {temp_dir}")
            subprocess.run(['git', 'clone', self.repo_url, temp_dir], check=True)
            return temp_dir
        except subprocess.CalledProcessError:
            print("Error: Failed to clone repository.")
            sys.exit(1)

    def get_commits(self) -> List[dict]:
        """
        Получает список коммитов из репозитория, начиная с указанной даты.
        """
        os.chdir(self.repo_path)
        try:
            cmd = [
                'git',
                'log',
                f'--since={self.commit_date}',
                '--name-only',
                '--pretty=format:%H|%s|%P'
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
            commits = []
            current_commit = None

            for line in result.stdout.strip().split('\n'):
                if line == '':
                    continue
                if '|' in line:  # Начало нового коммита
                    if current_commit:  # Сохраняем предыдущий коммит
                        commits.append(current_commit)
                    parts = line.split('|', 2)
                    commit_hash, message, parent_hashes = parts if len(parts) == 3 else (*parts, '')
                    parents = parent_hashes.strip().split()
                    current_commit = {
                        'hash': commit_hash,
                        'message': message,
                        'parents': parents,
                        'files': []
                    }
                else:
                    current_commit['files'].append(line.strip())  # Собираем связанные файлы

            if current_commit:  # Добавляем последний коммит
                commits.append(current_commit)

            return commits
        finally:
            os.chdir(os.getcwd())

    def build_graph(self, commits: List[dict]) -> str:
        """
        Строит граф в формате PlantUML, отображающий связи коммитов, файлов и папок.
        """
        graph = ['@startuml']
        graph.append('skinparam rectangle {')
        graph.append('   BackgroundColor #FDF6E3')
        graph.append('}')

        commit_defs = {}
        file_defs = {}

        for idx, commit in enumerate(reversed(commits)):
            commit_id = f'Commit{idx + 1}'
            commit_defs[commit['hash']] = commit_id
            graph.append(f'rectangle "{commit["message"]}" as {commit_id}')

            # Добавляем файлы и папки, связанные с этим коммитом
            for file_path in commit['files']:
                if file_path not in file_defs:
                    file_id = f'File{len(file_defs) + 1}'
                    file_defs[file_path] = file_id
                    graph.append(f'rectangle "{file_path}" as {file_id}')
                graph.append(f'{commit_id} --> {file_defs[file_path]}')

        # Добавляем связи между коммитами
        for commit in reversed(commits):
            child_id = commit_defs[commit['hash']]
            for parent_hash in commit['parents']:
                if parent_hash in commit_defs:
                    parent_id = commit_defs[parent_hash]
                    graph.append(f'{parent_id} <|-- {child_id}')

        graph.append('@enduml')
        return '\n'.join(graph)

    def save_output(self, content: str):
        """
        Сохраняет сгенерированный PlantUML-код в файл.
        """
        with open(self.output_file, 'w') as file:
            file.write(content)
        print(f"PlantUML code has been written to {self.output_file}")

    def run(self):
        commits = self.get_commits()
        graph_content = self.build_graph(commits)
        self.save_output(graph_content)


# Если скрипт запускается напрямую
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python main.py <repo_url> <output_file> <commit_date>")
        sys.exit(1)

    repo_url = sys.argv[1]
    output_file = sys.argv[2]
    commit_date = sys.argv[3]

    # Проверяем формат даты
    try:
        datetime.strptime(commit_date, "%Y-%m-%d")
    except ValueError:
        print("Error: commit_date must be in the format YYYY-MM-DD")
        sys.exit(1)

    visualizer = GitVisualizer(repo_url, output_file, commit_date)
    visualizer.run()
