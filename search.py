import subprocess
import pathlib
import sys
import re

def main():
    if 2 != len(sys.argv):
        print('Argument Error')
        return

    target_func = sys.argv[1]
    print('search: ' + target_func)
    show_call_func_list(target_func, 0)

def show_call_func_list(func_name, nest_count):
    call_list = global_rx(func_name)
    for call in call_list:
        if not call:
            break

        call_data = call.split(maxsplit=3)
        # print(call_data)

        # 検索結果が呼び出し箇所でない場合は次へ
        if not is_call_func(func_name, call_data[3]):
            continue

        prev_func = search_func_name(call_data[2], call_data[1])
        if not prev_func:
            pass
            # print('None')
        elif func_name == prev_func:
            # 検索結果が同じ関数名の場合は結果なしとして扱う(ガード処理)
            pass
            # print('None')
        else:
            print(' ' * nest_count + prev_func)
            show_call_func_list(prev_func, nest_count + 1)

def search_func_name(file_name, file_line):
    prev_func = ''
    func_list = global_f(file_name)
    for func in func_list:
        if not func:
            break

        # print(func)
        func_data = func.split(maxsplit=3)

        # 呼び出し元検索対象ファイルからヘッダーファイルを除外
        if is_header_file(func_data[2]):
            continue

        if int(file_line) > int(func_data[1]):
            prev_func = func_data[0]
        else:
            break

    return prev_func

def global_rx(func_name):
    CMD = 'global -rx ' + func_name
    return subprocess.check_output(CMD,shell=True).decode('utf-8').split('\n')

def global_f(file_name):
    CMD = 'global -f ' + file_name
    return subprocess.check_output(CMD,shell=True).decode('utf-8').split('\n')

def is_call_func(func_name, ref_code):
    pattern = f'{func_name}\s*\('
    if re.search(pattern, ref_code):
        return True
    else:
        return False

def is_header_file(file_path):
    p_file = pathlib.Path(file_path)
    # print(p_file.suffix)

    result = False
    if p_file.suffix == '.h' or p_file.suffix == '.hpp':
        result = True

    return result

if __name__ == '__main__':
    main()
