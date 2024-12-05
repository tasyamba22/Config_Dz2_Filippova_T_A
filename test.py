import unittest
from unittest.mock import patch, MagicMock
import json
from configgraf import (
    fetch_package_dependencies,
    generate_graphviz_content,
    build_dependency_graph,
    save_to_file
)

class TestDependencyVisualizer(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_fetch_package_dependencies(self, mock_urlopen):
        # Тестируем получение списка зависимостей из репозитория
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({
            "dist-tags": {"latest": "1.0.0"},
            "versions": {
                "1.0.0": {"dependencies": {"database": "^1.0.0", "auth": "^2.0.0"}}
            }
        }).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        # Вызов тестируемой функции
        dependencies = fetch_package_dependencies("express", "https://registry.npmjs.com")
        # Проверка результата
        self.assertEqual(dependencies, {"database": "^1.0.0", "auth": "^2.0.0"})

    def test_generate_graphviz_content(self):
        #Тестируем генерацию Graphviz-кода
        dependency_map = {
            "webapp": ["database", "auth"],
            "database": ["storage"]
        }
        expected_graphviz = (
            "digraph Dependencies {\n"
            '    "webapp" -> "database";\n'
            '    "webapp" -> "auth";\n'
            '    "database" -> "storage";\n'
            "}"
        )
        result = generate_graphviz_content(dependency_map)
        self.assertEqual(result, expected_graphviz)

    @patch("configgraf.fetch_package_dependencies")
    def test_build_dependency_graph(self, mock_fetch_dependencies):
        #Тестируем построение полного графа зависимостей.
        mock_fetch_dependencies.side_effect = lambda pkg_name, _: {
            "webapp": {"database": "^1.0.0", "auth": "^2.0.0"},
            "database": {"storage": "^1.0.0"},
            "auth": {},
            "storage": {}
        }.get(pkg_name, {})
        result = build_dependency_graph("webapp", "https://registry.npmjs.com")
        expected_graph = {
            "webapp": ["database", "auth"],
            "database": ["storage"],
            "auth": [],
            "storage": []
        }
        self.assertEqual(result, expected_graph)

    def test_save_to_file(self):
        # Тестируем сохранение данных в файл.
        test_content = "digraph Dependencies {\n}"
        test_path = "test_output.dot"
        try:
            save_to_file(test_path, test_content)

            with open(test_path, 'r') as file:
                self.assertEqual(file.read(), test_content)
        finally:
            import os
            if os.path.exists(test_path):
                os.remove(test_path)

if __name__ == "__main__":
    unittest.main()

