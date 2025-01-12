import re

def parse_readme_by_lines(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    firmware_data = []
    general_info = []
    current_firmware = {}
    section = None
    capturing_general_info = True

    for line in lines:
        line = line.strip()
        if capturing_general_info:
            if line.startswith("## ["):
                capturing_general_info = False
            else:
                general_info.append(line)
                continue

        if line.startswith("## [") and "](" in line:
            if current_firmware:
                firmware_data.append(current_firmware)
                current_firmware = {}

            name, link = re.findall(r"\[(.+?)\]\((.+?)\)", line)[0]
            current_firmware['name'] = f"[{name}]({link})"
            current_firmware['info'] = ""
            current_firmware['pros'] = ""
            current_firmware['cons'] = ""
        elif line.startswith("### Info:"):
            section = 'info'
        elif line.startswith("### Pros:"):
            section = 'pros'
        elif line.startswith("### Cons:"):
            section = 'cons'
        elif line.startswith("--------------------"):
            section = None
        elif section and line:
            current_firmware[section] += line + "<br>"

    if current_firmware:
        firmware_data.append(current_firmware)

    return general_info, firmware_data


def create_markdown_table_with_general_info(general_info, firmware_data, output_file):
    """Firmware bilgileriyle Markdown tablosu oluşturur ve genel bilgileri ekler."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in general_info:
            file.write(line + "\n")
        file.write("\n")

        file.write("| Firmware                | Info                                                                 | Pros                                                                | Cons                                    |\n")
        file.write("|:------------------------|:--------------------------------------------------------------------|:--------------------------------------------------------------------|:---------------------------------------|\n")  # Ortalanmış sütunlar

        # Tablo satırları
        for item in firmware_data:
            file.write(
                f"| {item['name']:<24} | {item['info'].strip():<70} | {item['pros'].strip():<70} | {item['cons'].strip():<40} |\n"
            )


def create_markdown_table_compare_with_general_info(general_info, firmware_data, output_file):
    """Firmware bilgileriyle Markdown tablosu oluşturur ve genel bilgileri ekler."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in general_info:
            file.write(line + "\n")
        file.write("\n")

        header = "| | "
        separator = "|:----|"
        pros = "| Pros | "
        cons = "| Cons | "

        for item in firmware_data:
            header += item['name'] + " |"
            separator += ":----|"
            pros += item['pros'] + " |"
            cons += item['cons'] + " |"
        
        file.write(header + "\n")
        file.write(separator + "\n")
        file.write(pros + "\n")
        file.write(cons + "\n")


if __name__ == "__main__":
    input_readme = "README.md"
    output_readme = "README_new.md"
    output_horizontal = "README_horizontal_table.md"
    general_info, firmware_data = parse_readme_by_lines(input_readme)
    create_markdown_table_with_general_info(general_info, firmware_data, output_readme)
    create_markdown_table_compare_with_general_info(general_info, firmware_data, output_horizontal)
