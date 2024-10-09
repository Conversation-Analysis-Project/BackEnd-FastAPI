import csv
import os

# 이름을 알파벳으로 매핑하는 딕셔너리
name_mapping = {}
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
current_index = 0

def get_masked_name(name):
    global current_index
    # 이미 이름이 알파벳으로 매핑되어 있는 경우 그대로 반환
    if name in name_mapping:
        return name_mapping[name]
    # 새로운 이름인 경우 알파벳으로 매핑
    if current_index < len(alphabet):
        masked_name = alphabet[current_index]
        name_mapping[name] = masked_name
        current_index += 1
        return masked_name
    else:
        raise ValueError("알파벳 A-Z가 모두 사용되었습니다.")

# CSV 파일에서 이름을 마스킹하는 함수
def mask_names_in_csv(input_csv_file):
    output_csv_file = os.path.splitext(input_csv_file)[0] + '_masked.csv'

    with open(input_csv_file, 'r', encoding='utf-8') as infile, open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        # 첫 줄은 헤더이므로 그대로 복사
        header = next(csv_reader)
        csv_writer.writerow(header)

        for row in csv_reader:
            # 2열(이름)에 해당하는 값을 알파벳으로 변환
            row[1] = get_masked_name(row[1])
            csv_writer.writerow(row)

    print(f"'{output_csv_file}' 파일이 생성되었습니다.")
    return output_csv_file
