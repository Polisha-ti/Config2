import unittest
import os
import tempfile
import shutil
from datetime import datetime
from titova import GitVisualizer  # Замените "main" на имя файла, где находится ваш код


class TestGitVisualizer(unittest.TestCase):
    def setUp(self):
        """
        Создает временную папку для вывода результатов.
        """
        self.test_repo_url = "https://github.com/see12357/ConfigDZ-2.git"  # Пример публичного репозитория
        self.test_output_file = "test_output.puml"
        self.test_commit_date = "2024-11-15"
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = os.path.join(self.temp_dir, self.test_output_file)

    def tearDown(self):
        """
        Удаляет временную папку и все её содержимое.
        """
        shutil.rmtree(self.temp_dir)

    def test_clone_repository(self):
        """
        Тестирует клонирование репозитория.
        """
        visualizer = GitVisualizer(self.test_repo_url, self.output_path, self.test_commit_date)
        self.assertTrue(os.path.exists(visualizer.repo_path))
        self.assertTrue(os.path.isdir(visualizer.repo_path))

    def test_get_commits(self):
        """
        Тестирует получение списка коммитов.
        """
        visualizer = GitVisualizer(self.test_repo_url, self.output_path, self.test_commit_date)
        commits = visualizer.get_commits()
        self.assertIsInstance(commits, list)
        self.assertTrue(len(commits) > 0)
        self.assertIn('hash', commits[0])
        self.assertIn('message', commits[0])
        self.assertIn('files', commits[0])

    def test_build_graph(self):
        """
        Тестирует создание графа в формате PlantUML.
        """
        visualizer = GitVisualizer(self.test_repo_url, self.output_path, self.test_commit_date)
        commits = visualizer.get_commits()
        graph_content = visualizer.build_graph(commits)
        self.assertIsInstance(graph_content, str)
        self.assertTrue(graph_content.startswith("@startuml"))
        self.assertTrue(graph_content.endswith("@enduml"))

    def test_save_output(self):
        """
        Тестирует сохранение результата в файл.
        """
        visualizer = GitVisualizer(self.test_repo_url, self.output_path, self.test_commit_date)
        commits = visualizer.get_commits()
        graph_content = visualizer.build_graph(commits)
        visualizer.save_output(graph_content)
        self.assertTrue(os.path.exists(self.output_path))

        with open(self.output_path, 'r') as file:
            content = file.read()
        self.assertEqual(content, graph_content)


if __name__ == "__main__":
    unittest.main()
