GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

show_menu() {
    clear
    echo -e "${BLUE}╔═══════════════════════════════════╗${NC}"
    echo -e "${BLUE}║          TEXT SEARCHER            ║${NC}"
    echo -e "${BLUE}╠═══════════════════════════════════╣${NC}"
    echo -e "${BLUE}║${NC}  1. Запустить базу данных         ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  2. Запустить краулер             ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  3. Поиск по тексту               ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  4. Экспорт в CSV                 ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  5. Открыть pgweb                 ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  6. Остановить всё                ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  7. Очистить БД                   ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  8. Сгенерировать тестовые файлы  ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  0. Выйти                         ${BLUE}║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════╝${NC}"
}

while true; do
    show_menu
    read -p "Выберите действие: " choice
    
    case $choice in
        1)
            echo -e "${GREEN}Запуск базы данных...${NC}"
            docker compose up -d postgres pgweb
            echo -e "${GREEN}База готова!${NC}"
            echo -e "${GREEN}pgweb: http://localhost:8081${NC}"
            read -p "Нажмите Enter..."
            ;;
        2)
            echo -e "${GREEN}Запуск парсера...${NC}"
            docker compose run --rm app python run.py
            read -p "Нажмите Enter..."
            ;;
        3)
            read -p "Что ищем? " query
            echo -e "${GREEN}Поиск...${NC}"
            docker compose run --rm app python search.py "$query"
            read -p "Нажмите Enter..."
            ;;
        4)
            read -p "Имя CSV файла (export.csv): " filename
            [ -z "$filename" ] && filename="export.csv"
            docker compose run --rm app python export.py "$filename"
            echo -e "${GREEN}Экспортировано в $filename${NC}"
            read -p "Нажмите Enter..."
            ;;
        5)
            echo -e "${GREEN}Открываю pgweb...${NC}"
            docker compose up -d postgres pgweb
            xdg-open "http://localhost:8081" 2>/dev/null || open "http://localhost:8081" 2>/dev/null
            read -p "Нажмите Enter..."
            ;;
        6)
            echo -e "${GREEN}Остановка...${NC}"
            docker compose down
            read -p "Нажмите Enter..."
            ;;
        7)
            echo -e "${RED}Очистка БД удалит все данные!${NC}"
            read -p "Уверены? (y/N): " confirm
            if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
                docker compose down -v
                echo -e "${GREEN}База очищена${NC}"
            fi
            read -p "Нажмите Enter..."
            ;;
        8)
            echo -e "${GREEN}Генерирую тестовые файлы в test_data/...${NC}"
            docker compose run --rm app python generate_test_files.py
            echo -e "${GREEN}Тестовые файлы созданы в test_data/${NC}"
            read -p "Нажмите Enter..."
            ;;
        0)
            echo -e "${GREEN}До свидания!!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Неверный выбор${NC}"
            read -p "Нажмите Enter..."
            ;;
    esac
done