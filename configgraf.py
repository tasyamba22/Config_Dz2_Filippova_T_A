import argparse
import urllib.request
import json

def fetch_package_dependencies(pkg_name, api_url):
    # Получение списка зависимостей для указанного пакета через предоставленный API.
    full_url = f"{api_url}/{pkg_name}"
    try:
        with urllib.request.urlopen(full_url) as response:
            if response.status != 200:
                raise ValueError(f"Ошибка: получен HTTP {response.status}")
            package_data = json.loads(response.read().decode())

        latest_version = package_data['dist-tags']['latest']
        dependencies = package_data['versions'][latest_version].get('dependencies', {})
        return dependencies

    except urllib.error.URLError as err:
        raise RuntimeError(f"Сетевая ошибка или неправильный URL: {err}")
    except json.JSONDecodeError:
        raise RuntimeError("Ошибка при анализе JSON ответа.")


def generate_graphviz_content(dependency_map):
    # Создает текстовое представление графа зависимостей в формате Graphviz.
    graph_lines = ["digraph Dependencies {"]
    for parent, children in dependency_map.items():
        for child in children:
            graph_lines.append(f'    "{parent}" -> "{child}";')
    graph_lines.append("}")
    return "\n".join(graph_lines)


def build_dependency_graph(pkg_name, api_url, graph=None, processed=None):
    # Построение графа зависимостей с учетом транзитивных зависимостей.
    if graph is None:
        graph = {}
    if processed is None:
        processed = set()

    if pkg_name in processed:
        return graph

    processed.add(pkg_name)

    try:
        dependencies = fetch_package_dependencies(pkg_name, api_url)
        graph[pkg_name] = list(dependencies.keys())

        for dependency in dependencies:
            build_dependency_graph(dependency, api_url, graph, processed)

    except Exception as err:
        print(f"Ошибка при обработке пакета {pkg_name}: {err}")

    return graph


def save_to_file(filepath, content):
    # Сохранение строки в указанный файл.
    try:
        with open(filepath, 'w') as file:
            file.write(content)
        print(f"Результат сохранен в файл: {filepath}")
    except IOError as error:
        print(f"Ошибка записи в файл: {error}")


def parse_arguments():
    # Обработка аргументов командной строки.
    parser = argparse.ArgumentParser(description="Создание графа зависимостей пакета")
    parser.add_argument("--graphviz-path", required=True, help="Путь к утилите Graphviz")
    parser.add_argument("--package-name", required=True, help="Имя пакета для анализа зависимостей")
    parser.add_argument("--output-path", required=True, help="Файл для сохранения результата")
    parser.add_argument("--repo-url", required=True, help="URL-адрес репозитория пакетов")
    return parser.parse_args()


def main():
    args = parse_arguments()
    pkg_name = args.package_name
    api_url = args.repo_url
    output_file = args.output_path

    print(f"Старт анализа зависимостей для пакета: {pkg_name}")
    dependency_graph = build_dependency_graph(pkg_name, api_url)

    print("Генерация кода для Graphviz...")
    graphviz_code = generate_graphviz_content(dependency_graph)
    print("Результат:")
    print(graphviz_code)

    print(f"Сохранение кода в файл {output_file}...")
    save_to_file(output_file, graphviz_code)
    print("Готово! Граф успешно построен и сохранен.")


if __name__ == "__main__":
    main()
