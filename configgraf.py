import argparse
import urllib.request
import json
from datetime import datetime, timedelta

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
        return dependencies, latest_version, package_data['time'][latest_version]

    except urllib.error.URLError as err:
        raise RuntimeError(f"Сетевая ошибка или неправильный URL: {err}")
    except json.JSONDecodeError:
        raise RuntimeError("Ошибка при анализе JSON ответа.")


def generate_graphviz_content(dependency_map):
    # Создает текстовое представление графа зависимостей в формате Graphviz.
    graph_lines = ["digraph Dependencies {"]
    processed_nodes = set()  # Хранение уже обработанных узлов

    for parent, data in dependency_map.items():
        version = data["version"]
        last_updated = data["last_updated"]
        children = data["dependencies"]

        # Определяем цвет узла на основе даты обновления
        last_update_date = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")
        color = "green" if last_update_date >= datetime.utcnow() - timedelta(days=60) else None

        if parent not in processed_nodes:
            if color:
                graph_lines.append(
                    f'    "{parent}" [label="{parent} ({version})", color={color}, style="filled,solid"];'
                )
            else:
                graph_lines.append(
                    f'    "{parent}" [label="{parent} ({version})", style="solid"];'
                )
            processed_nodes.add(parent)

        for child in children:
            child_data = dependency_map.get(child, {})
            child_version = child_data.get("version", "unknown")

            if "last_updated" in child_data:
                child_last_updated = datetime.strptime(child_data["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ")
                child_color = "green" if child_last_updated >= datetime.utcnow() - timedelta(days=60) else None
            else:
                child_color = None

            if child not in processed_nodes:
                if child_color:
                    graph_lines.append(
                        f'    "{child}" [label="{child} ({child_version})", color={child_color}, style="filled,solid"];'
                    )
                else:  # Узлы без заливки (только граница)
                    graph_lines.append(
                        f'    "{child}" [label="{child} ({child_version})", style="solid"];'
                    )
                processed_nodes.add(child)

            graph_lines.append(f'    "{parent}" -> "{child}";')

    graph_lines.append("}")
    return "\n".join(graph_lines)


def build_dependency_graph(pkg_name, api_url, graph=None, processed=None):
    # Построение графа зависимостей с учетом транзитивных зависимостей.
    if graph is None:
        graph = {}
    if processed is None:
        processed = {}

    if pkg_name in processed:
        return graph

    try:
        dependencies, latest_version, last_updated = fetch_package_dependencies(pkg_name, api_url)
        processed[pkg_name] = (latest_version, last_updated)  # Сохраняем версию и дату обновления
        graph[pkg_name] = {
            "dependencies": list(dependencies.keys()),
            "version": latest_version,
            "last_updated": last_updated,
        }

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
