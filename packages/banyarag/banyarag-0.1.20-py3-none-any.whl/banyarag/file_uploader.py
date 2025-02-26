import os
import requests

def upload_files_to_server(api_key, user_email, file_paths, server_url="https://train.banya.ai/upload_user_files_lib/"):
    """
    Uploads multiple files to a server using a RESTful API.

    Args:
        api_key (str): The user's API key.
        user_email (str): The user's email address.
        file_paths (list): A list of file paths to upload.
        server_url (str): The URL of the server's upload endpoint.

    Returns:
        dict: A dictionary containing the server's JSON response. Returns None on error.
    """
    files = []
    try:
        # 파일 업로드를 위해 파일 목록 준비
        for file_path in file_paths:
            try:
                files.append(('files', (os.path.basename(file_path), open(file_path, 'rb'))))
            except FileNotFoundError:
                print(f"Error: File not found: {file_path}")
                return None

        # API key와 사용자 이메일을 데이터에 포함
        data = {
            'api_key': api_key,
            'user_email': user_email
        }

        # 파일 업로드 요청 전송
        response = requests.post(server_url, files=files, data=data)
        response.raise_for_status()  # 4xx, 5xx 에러 발생 시 예외 발생

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    finally:
        # 열린 파일 객체를 모두 닫기
        for _, file_tuple in files:
            if isinstance(file_tuple, tuple) and len(file_tuple) > 1:
                file_obj = file_tuple[1]
                if hasattr(file_obj, 'close'):
                    file_obj.close()

if __name__ == '__main__':
    # 예시 사용법:
    api_key = "aHV4RRFdsDvoZKJL"
    user_email = "tony@nxdf.io"
    file_paths = [
        "/Users/daib-01/Desktop/data/KakaoTalk_20250206_2025_57_726_group.txt",
        "/Users/daib-01/Desktop/data/KakaoTalk_20250206_2025_25_525_group.txt"
    ]
    server_url = "https://train.banya.ai/upload_user_files_lib/"

    # 테스트를 위한 더미 파일 생성
    for file_path in file_paths:
        with open(file_path, "w") as f:
            f.write("This is a test file.")

    response = upload_files_to_server(api_key, user_email, file_paths, server_url)

    if response:
        print("Upload successful!")
        print("Server response:", response)
        # 테스트 후 더미 파일 삭제
        for file_path in file_paths:
            os.remove(file_path)
    else:
        print("Upload failed.")
